import unittest

import numpy as np

import selectfix

class TestSelectfix(unittest.TestCase):
    def test_selectfix_basic(self):
        sel = selectfix.Selector(2, [], [], 0.0, {}, 0.0)
        val = sel({"x1": 10, "x2": 10, "x3": 0, "x4": 0})
        assert val == 0
        val = sel({"x1": 10, "x2": 10, "x3": 10, "x4": 0})
        assert val == -10
        val = sel({"x1": 10, "x2": 10, "x3": 10, "x4": 10})
        assert val == -20

    def test_selectfix_jacobian(self):
        sel = selectfix.Selector(1, ["x1", "x2", "x3"], [], 0.0, {}, 0.0)
        val = sel({"x1": 10, "x2": 10, "x3": 0, "x4": 0})
        assert val == 0
        val = sel({"x1": 10, "x2": 10, "x3": 10, "x4": 0})
        assert val == -10
        val = sel({"x1": 10, "x2": 10, "x3": 10, "x4": 10})
        assert val == -10
        np.testing.assert_array_equal(sel.jacobian({"x1": 10, "x2": 10, "x3": 10, "x4": 0}), np.array([0, 0, 1, 0]))
        np.testing.assert_array_equal(sel.jacobian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.array([0, 0, 1, 0]))
        np.testing.assert_array_equal(sel.hessian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.zeros((4, 4)))

    def test_selectfix_using_exclude_free(self):
        sel = selectfix.Selector(1, ["x1", "x2", "x3"], [["x1", "x2"]], 0.0, {}, 0.0)
        val = sel({"x1": 10, "x2": 10, "x3": 0, "x4": 0})
        assert val == -10
        np.testing.assert_array_equal(sel.jacobian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.array([0, 1, 0, 0]))
        np.testing.assert_array_equal(sel.hessian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.zeros((4, 4)))

        sel = selectfix.Selector(1, ["x1", "x2", "x3"], [["x1", "x2"], ["x2", "x3"]], 0.0, {}, 0.0)
        val = sel({"x1": 10, "x2": 11, "x3": 12, "x4": 0})
        assert val == -11
        np.testing.assert_array_equal(sel.jacobian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.array([0, 1, 0, 0]))
        np.testing.assert_array_equal(sel.hessian({"x1": 10, "x2": 10, "x3": 0, "x4": 0}), np.zeros((4, 4)))

        sel = selectfix.Selector(
            2, ["x1", "x2", "x3", "x4", "x5"], [["x1", "x2"], ["x1", "x3"], ["x1", "x4"]], 0.0, {}, 0.0
        )
        val = sel({"x1": 14, "x2": 13, "x3": 12, "x4": 11, "x5": 10})
        assert val == -24
        np.testing.assert_array_equal(
            sel.jacobian({"x1": 14, "x2": 13, "x3": 12, "x4": 11, "x5": 10}), np.array([1, 0, 0, 0, 1])
        )
        np.testing.assert_array_equal(sel.hessian({"x1": 14, "x2": 13, "x3": 12, "x4": 11, "x5": 10}), np.zeros((5, 5)))

    def test_selectfix_using_range_penalty(self):
        sel = selectfix.Selector(1, ["x1", "x2", "x3"], [], 0.0, {"x1": (20, 30)}, 0.0)
        val = sel({"x1": 10, "x2": 10, "x3": 0})
        assert val == -10
        np.testing.assert_array_equal(sel.jacobian({"x1": 10, "x2": 10, "x3": 0}), np.array([1, 0, 1]))


if __name__ == "__main__":
    unittest.main()
