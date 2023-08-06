from __future__ import annotations

import jijmodeling as jm


def bin_packing():
    w = jm.Placeholder("w", ndim=1)
    num_items = jm.Placeholder("n")
    c = jm.Placeholder("c")

    # y[j]: bin j を使用するかしないか
    y = jm.BinaryVar("y", shape=(num_items,))
    # x[i][j]: item i を bin j に入れるとき1
    x = jm.BinaryVar("x", shape=(num_items, num_items))

    # i: itemの添字
    i = jm.Element("i", belong_to=num_items)
    # j: binの添字
    j = jm.Element("j", belong_to=num_items)

    problem = jm.Problem("bin-packing")

    # objective function
    obj = y[:]
    problem += obj

    # Constraint1: 各itemをちょうど1つのbinにぶち込む
    const1 = jm.Constraint("onehot-constraint", jm.sum(j, x[i, j]) - 1 == 0, forall=i)
    problem += const1

    # Constraint2: knapsack制約
    const2 = jm.Constraint(
        "knapsack-constraint", jm.sum(i, w[i] * x[i, j]) - y[j] * c <= 0, forall=j
    )
    problem += const2

    return problem
