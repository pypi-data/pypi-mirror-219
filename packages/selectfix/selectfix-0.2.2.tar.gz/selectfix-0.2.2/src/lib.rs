use indexmap::IndexMap;
use pyo3::prelude::*;
use pyo3::types::PyBytes;

use anyhow::Result;
use bincode::{deserialize, serialize};
use ordered_float::OrderedFloat;
use serde::{Deserialize, Serialize};
use std::cmp;
use std::collections::HashMap;

/// A selector for the fixed value.
/// This class selects the variables which are closest to the fixed value.
#[derive(Serialize, Deserialize)]
#[pyclass(module = "selectfix")]
struct Selector {
    #[pyo3(get)]
    n_select: usize,
    #[pyo3(get)]
    candidates: Vec<String>,
    #[pyo3(get)]
    exclude_free: Vec<Vec<String>>,
    #[pyo3(get)]
    fixed_val: f64,
    #[pyo3(get)]
    ranges: HashMap<String, (f64, f64)>,
    #[pyo3(get)]
    eps: f64,
}

impl Selector {
    fn is_excluded(&self, names: Vec<&String>) -> bool {
        self.exclude_free
            .iter()
            .any(|ex| ex.iter().all(|e| names.contains(&e)))
    }
    fn search_free(
        &self,
        open_idxs: Vec<usize>,
        names: &Vec<String>,
        close_idxs: Vec<usize>,
    ) -> (Vec<usize>, bool) {
        if open_idxs.len() <= self.n_select {
            return ([close_idxs, open_idxs].concat(), true);
        }
        for (i, &k) in open_idxs.iter().enumerate() {
            let close_idxs_k = [close_idxs.clone(), vec![k]].concat();
            if self.is_excluded(close_idxs_k.iter().map(|&j| &names[j]).collect::<Vec<_>>()) {
                continue;
            }
            let mut tmp_open_idxs = open_idxs.clone();
            tmp_open_idxs.remove(i);
            let (tmp_searched, res) = self.search_free(tmp_open_idxs, names, close_idxs_k);
            if res {
                return (tmp_searched, res);
            }
        }
        (close_idxs, false)
    }
    fn compute_indices(
        &self,
        xdic: &IndexMap<String, f64>,
    ) -> Result<(Vec<usize>, Vec<OrderedFloat<f64>>)> {
        let xdic_new = if self.candidates.is_empty() {
            xdic.clone()
        } else {
            // Extract the candidates from xdic.
            self.candidates
                .iter()
                .map(|can| (can.clone(), xdic[can]))
                .collect::<IndexMap<_, _>>()
        };
        let violations = xdic_new
            .iter()
            .map(|(_, &x)| {
                cmp::min(
                    OrderedFloat(-(x - self.fixed_val).abs() + self.eps),
                    OrderedFloat(0.0),
                )
            })
            .collect::<Vec<_>>();
        let mut indices = (0..violations.len()).collect::<Vec<_>>();
        indices.sort_by(|&i, &j| violations[i].cmp(&violations[j]));
        if self.exclude_free.len() > 0 {
            let (searched, res) =
                self.search_free(indices.clone(), &xdic_new.keys().cloned().collect(), vec![]);
            if !res {
                return Err(anyhow::anyhow!(
                    "Not found the selections with the given exclude_free.",
                ));
            }
            indices = searched;
        }
        indices.reverse();
        Ok((indices, violations))
    }
}

#[pymethods]
impl Selector {
    /// Create a new selector.
    ///
    /// # Arguments
    /// * `n_select` - The number of variables to be selected to fix.
    /// * `candidates` - Candidates for selection.
    /// * `exclude_free` - Combinations you want to exclude among non-fixed variables.
    /// * `fixed_val` - Target value of variable to be fixed.
    /// * `ranges` - Range to be set on unfixed variables.
    /// * `eps` - Tolerance for fixed variables and fixed_val.
    #[new]
    fn new(
        n_select: usize,
        candidates: Vec<String>,
        exclude_free: Vec<Vec<String>>,
        fixed_val: f64,
        ranges: HashMap<String, (f64, f64)>,
        eps: f64,
    ) -> Self {
        Selector {
            n_select: n_select,
            candidates: candidates,
            exclude_free: exclude_free,
            fixed_val: fixed_val,
            ranges: ranges,
            eps: eps,
        }
    }
    fn __call__(&self, xdic: IndexMap<String, f64>) -> PyResult<f64> {
        let (indices, violations) = self
            .compute_indices(&xdic)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        // Compute the additional penalty.
        // This is the penalty for the variables which are not selected.
        // The penalty is the minimum of the distance from the fixed value to the lower and upper bounds.
        let additional: f64 = if self.candidates.is_empty() || self.ranges.is_empty() {
            0.0
        } else {
            (self.n_select..indices.len())
                .map(|i| {
                    let key = &self.candidates[indices[i]];
                    if let (Some(range), Some(x)) = (self.ranges.get(key), xdic.get(key)) {
                        if range.0 <= *x && *x <= range.1 {
                            0.0
                        } else {
                            cmp::min(
                                OrderedFloat((range.0 - x).abs()),
                                OrderedFloat((range.1 - x).abs()),
                            )
                            .0
                        }
                    } else {
                        0.0
                    }
                })
                .sum()
        };
        Ok((0..self.n_select)
            .map(|i| f64::from(violations[indices[i]]))
            .sum::<f64>()
            - additional)
    }
    fn jacobian(&self, xdic: IndexMap<String, f64>) -> PyResult<Vec<f64>> {
        let ndim = xdic.len();
        let (indices, _) = self
            .compute_indices(&xdic)
            .map_err(|e| pyo3::exceptions::PyValueError::new_err(e.to_string()))?;
        let mut jac = vec![0.0; ndim];
        for i in 0..self.n_select {
            jac[indices[i]] = 1.0;
        }
        if self.candidates.is_empty() || self.ranges.is_empty() {
            return Ok(jac);
        }
        for i in self.n_select..indices.len() {
            let key = &self.candidates[indices[i]];
            if let (Some(range), Some(x)) = (self.ranges.get(key), xdic.get(key)) {
                if range.0 <= *x && *x <= range.1 {
                    jac[indices[i]] = 0.0;
                } else {
                    jac[indices[i]] = if range.0 < *x { -1.0 } else { 1.0 };
                }
            } else {
                jac[indices[i]] = 0.0;
            }
        }
        Ok(jac)
    }
    fn hessian(&self, xdic: IndexMap<String, f64>) -> PyResult<Vec<Vec<f64>>> {
        Ok(vec![vec![0.0; xdic.len()]; xdic.len()])
    }
    fn __setstate__(&mut self, _py: Python, state: &PyBytes) -> PyResult<()> {
        *self = deserialize(state.as_bytes()).unwrap();
        Ok(())
    }
    fn __getstate__<'py>(&self, py: Python<'py>) -> PyResult<&'py PyBytes> {
        Ok(PyBytes::new(py, &serialize(&self).unwrap()))
    }
    pub fn __getnewargs__(&self) -> PyResult<(usize, Vec<String>, Vec<Vec<String>>, f64, f64)> {
        Ok((
            self.n_select,
            self.candidates.clone(),
            self.exclude_free.clone(),
            self.fixed_val,
            self.eps,
        ))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn selectfix(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Selector>()?;
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_is_excluded() {
        use super::*;
        let selector = Selector::new(
            2,
            vec![
                "a".to_string(),
                "b".to_string(),
                "c".to_string(),
                "d".to_string(),
            ],
            vec![vec!["a".to_string(), "b".to_string()]],
            0.0,
            HashMap::new(),
            0.0,
        );
        assert_eq!(
            selector.is_excluded(vec![&"a".to_string(), &"b".to_string()]),
            true
        );
        assert_eq!(selector.is_excluded(vec![&"a".to_string()]), false);
        assert_eq!(
            selector.is_excluded(vec![&"a".to_string(), &"c".to_string()]),
            false
        );
    }

    #[test]
    fn test_search_free() {
        use super::*;
        let selector = Selector::new(
            2,
            vec![
                "a".to_string(),
                "b".to_string(),
                "c".to_string(),
                "d".to_string(),
            ],
            vec![vec!["a".to_string(), "b".to_string()]],
            0.0,
            HashMap::new(),
            0.0,
        );
        let (searched, res) = selector.search_free(
            vec![0, 1, 2, 3],
            &vec![
                "a".to_string(),
                "b".to_string(),
                "c".to_string(),
                "d".to_string(),
            ],
            vec![],
        );
        assert_eq!(res, true);
        assert_eq!(searched, vec![0, 2, 1, 3]);
    }
}
