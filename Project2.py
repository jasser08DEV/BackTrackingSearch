import copy
import json
import heapq
import sys
from operator import truediv

def Revise(Xi,Xj,domain,constraint):
    revised = False
    for i in list(domain[Xi]):
        satisfiable = False
        for j in domain[Xj]:
            if constraint == "all_different":
                if i != j:
                    satisfiable = True
                    break;
            elif constraint == "neq":
                if i != j:
                    satisfiable = True
                    break
            elif constraint == "eq":
                if i == j:
                    satisfiable = True
                    break
            elif constraint == "lt":
                if i < j:
                    satisfiable = True
                    break
            elif constraint == "lte":
                if i <= j:
                    satisfiable = True
                    break
            elif constraint == "gt":
                if i > j:
                    satisfiable = True
                    break
            elif constraint == "gte":
                if i >= j:
                    satisfiable = True
                    break
        if not satisfiable:
            domain[Xi].remove(i)
            revised = True
    return revised
def Neighbors(CSP):
    neighbors ={}
    type_map={}
    for variable in CSP["variables"]:
        neighbors[variable]=set()
    for constraint in CSP["constraints"]:
        ctype = constraint["type"]
        vars = constraint.get("vars")
        for var1 in vars:
            for var2 in vars:
                if var1!=var2:
                    neighbors[var1].add(var2)
                    type_map[(var1,var2)]=ctype
    return neighbors, type_map

def AC3(CSP):
    domain = CSP["domains"]
    neighbors,type_map=Neighbors(CSP)
    queue=[]
    for (var1,var2),ctype in type_map.items():
        queue.append((var1,var2,ctype))
    while queue:
        var1,var2,type= queue.pop(0)
        revised = Revise(var1,var2,domain,type)
        if revised:
            if len(domain[var1]) == 0:
                return False
            for neighbor in neighbors[var1]:
                if neighbor != var2:
                    ctype=type_map[(neighbor,var1)]
                    queue.append((neighbor,var1,ctype))
    return True



if __name__ == '__main__':
    json_name = sys.argv[1]

    with open(json_name+".json") as json_file:
        CSP = json.load(json_file)

    print(CSP)
    print(CSP['variables']) #List
    print(CSP['constraints']) #List of Constraints
    print(CSP['domains']) #Map: str->List

    #TODO: The project!

    with open(json_name+"_Solution.json", 'w') as f:
        json.dump(CSP, f, indent=4)
