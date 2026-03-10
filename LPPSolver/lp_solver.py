from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, GLPK

# =============================
# Interactive LP Solver
# =============================

def interactive_lp_solver():
    print("=== Linear Programming Solver ===")
    
    # 1. Objective type
    obj_type = input("Enter objective type (max/min): ").strip().lower()
    if obj_type not in ['max', 'min']:
        print("Invalid objective type, defaulting to max.")
        obj_type = 'max'
    
    # Create problem
    prob = LpProblem("LP_Problem", LpMaximize if obj_type=='max' else LpMinimize)
    
    # 2. Number of variables
    n_vars = int(input("Enter number of variables: "))
    
    # 3. Create variables
    variables = {}
    for i in range(1, n_vars+1):
        name = f"x{i}"
        variables[name] = LpVariable(name, lowBound=0)
    
    # 4. Objective function
    print("Enter coefficients for objective function:")
    coeffs = {}
    for i in range(1, n_vars+1):
        coeffs[f"x{i}"] = float(input(f"Coefficient for x{i}: "))
    prob += sum(coeffs[name]*variables[name] for name in coeffs)
    
    # 5. Constraints
    n_constraints = int(input("Enter number of constraints: "))
    for j in range(1, n_constraints+1):
        print(f"Constraint {j}:")
        constraint_coeffs = {}
        for i in range(1, n_vars+1):
            constraint_coeffs[f"x{i}"] = float(input(f"Coefficient for x{i}: "))
        sense = input("Sense (<=, >=, =): ").strip()
        rhs = float(input("RHS value: "))
        expr = sum(constraint_coeffs[name]*variables[name] for name in constraint_coeffs)
        if sense == '<=':
            prob += (expr <= rhs)
        elif sense == '>=':
            prob += (expr >= rhs)
        elif sense == '=':
            prob += (expr == rhs)
        else:
            print("Invalid sense, skipping this constraint.")
    
    # 6. Solve
    prob.solve(GLPK(msg=False))
    
    # 7. Print results
    print("\n=== Solution ===")
    status_dict = {1:"Optimal", 0:"Not Solved/Infeasible", -1:"Unbounded"}
    print("Status:", status_dict.get(prob.status, prob.status))
    for var in variables.values():
        print(var.name, "=", var.value())
    print("Optimal Z =", prob.objective.value())

# Run the solver
interactive_lp_solver()
