from pulp import LpVariable, lpSum

from multiobjective_lp.model.multi_objective_lp import MultiObjectiveLpProblem
from solvers.summed.SummedObjectivesLpSolver import SummedObjectivesLpSolver

if __name__ == "__main__":
    # we are building only one warehouse
    warehouses_to_build = 1

    # define the costs for the warehouse choices
    warehouse_fixed_costs = [100, 120, 80]
    cost_per_km = [3, 3, 3]
    distances = [20, 30, 45]
    transport_costs = [cost * dist for cost, dist in zip(cost_per_km, distances)]
    warehouses = ["1", "2", "3"]

    model = MultiObjectiveLpProblem(name="warehouse")

    build_warehouse_flag = LpVariable.matrix(
        "build", warehouses, cat="Binary", lowBound=0
    )

    model += lpSum(build_warehouse_flag) == warehouses_to_build

    # cost to be minimized
    trans_obj = lpSum(
        [
            trans_cost * flag
            for trans_cost, flag in zip(transport_costs, build_warehouse_flag)
        ]
    )
    fix_obj = lpSum(
        [
            fix_cost * flag
            for fix_cost, flag in zip(warehouse_fixed_costs, build_warehouse_flag)
        ]
    )

    model.setObjectives([trans_obj, fix_obj])
    model.solve(solver=SummedObjectivesLpSolver(False))
