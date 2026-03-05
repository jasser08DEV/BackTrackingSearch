import copy
import json
import sys

def satisfies(val_n, val_lowest, constraint):
    rule = constraint["type"]
    if rule in ["neq", "all_different"]: return val_n != val_lowest
    if rule == "eq": return val_n == val_lowest
    if rule == "lt": return val_n < val_lowest
    if rule == "lte": return val_n <= val_lowest
    if rule == "gt": return val_n > val_lowest
    if rule == "gte": return val_n >= val_lowest
    if rule == "sum_eq":
        target = constraint["value"]
        return val_n + val_lowest == target
    return True
def Revise(var1, var2, domain, constraint):
    revised = False
    for i in list(domain[var1]):
        if not any(satisfies(i, j, constraint) for j in domain[var2]):
            domain[var1].remove(i)
            revised = True
    return revised

INVERSE = {"lt": "gt", "gt": "lt", "lte": "gte", "gte": "lte"}

def orient_constraint(constraint, var1, var2):

    ctype = constraint["type"]
    if ctype not in INVERSE:
        return constraint
    original_vars = constraint["vars"]
    if original_vars[0] == var1:
        return constraint
    return {**constraint, "type": INVERSE[ctype]}

def Neighbors(CSP):
    neighbors = {}
    type_map = {}
    for variable in CSP["variables"]:
        neighbors[variable] = set()
    for constraint in CSP["constraints"]:
        vars = constraint.get("vars")
        for var1 in vars:
            for var2 in vars:
                if var1 != var2:
                    neighbors[var1].add(var2)
                    if (var1, var2) not in type_map:
                        type_map[(var1, var2)] = []
                    oriented = orient_constraint(constraint, var1, var2)
                    if oriented not in type_map[(var1, var2)]:
                        type_map[(var1, var2)].append(oriented)
    return neighbors, type_map

def AC3(CSP):
    domain = CSP["domains"]
    neighbors, type_map = Neighbors(CSP)
    queue = []
    for (var1, var2), constraints in type_map.items():
        for constraint in constraints:
            queue.append((var1, var2, constraint))
    while queue:
        var1, var2, constraint = queue.pop(0)
        revised = Revise(var1, var2, domain, constraint)
        if revised:
            if len(domain[var1]) == 0:
                return False
            for neighbor in neighbors[var1]:
                if neighbor != var2:
                    for c in type_map[(neighbor, var1)]:
                        queue.append((neighbor, var1, c))
    return True



def BackTrackingSearch(CSP):
    domains = CSP["domains"]
    vars = CSP["variables"]
    for v in vars:
        if len(domains[v]) == 0:
            return False
    if all(len(domains[v]) == 1 for v in vars):
        return CSP
    unassigned = [v for v in vars if len(domains[v]) > 1]
    neighbors, type_map = Neighbors(CSP)
    lowest = unassigned[0]
    for u in unassigned:
        if u == lowest:
            continue
        elif len(domains[u]) < len(domains[lowest]):
            lowest = u
        elif len(domains[u]) == len(domains[lowest]):
            if len(neighbors[u]) > len(neighbors[lowest]):
                lowest = u

    def get_lcv_score(val):
        conflicts = 0
        for n in neighbors[lowest]:
            if len(domains[n]) > 1:
                for constraint in type_map[(n, lowest)]:
                    for n_val in domains[n]:
                        if not satisfies(n_val, val, constraint):
                            conflicts += 1
        return conflicts

    ordered_values = sorted(domains[lowest], key=get_lcv_score)

    for value in ordered_values:
        local_csp = CSP.copy()
        local_csp["domains"] = copy.deepcopy(CSP["domains"])
        local_csp["domains"][lowest] = [value]
        if AC3(local_csp):
            result = BackTrackingSearch(local_csp)
            if result is not False:
                return result
    return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python solver.py <json_filename_without_extension>")
        sys.exit(1)
    json_name = sys.argv[1]

    with open(json_name + ".json") as json_file:
        CSP = json.load(json_file)

    print(CSP)
    print(CSP['variables'])   # List
    print(CSP['constraints']) # List of Constraints
    print(CSP['domains'])     # Map: str->List

    initial_check = AC3(CSP)

    if not initial_check:
        print("No solution possible (Initial AC3 failed).")
        solution_csp = False
    else:
        solution_csp = BackTrackingSearch(CSP)

    if solution_csp:
        output_data = solution_csp
        print(f"Solution saved to {json_name}_Solution.json")
    else:
        output_data = CSP
        print(f"No solution found. Saving reduced domains to {json_name}_Solution.json")

    with open(json_name + "_Solution.json", 'w') as f:
        json.dump(output_data, f, indent=4)