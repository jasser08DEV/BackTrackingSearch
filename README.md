# CSP-Backtracking-Solver

This repository contains a **Constraint Satisfaction Problem (CSP)** solver implemented in Python. The project utilizes the **Backtracking Search** algorithm enhanced by **AC-3 (Arc Consistency)** and heuristic optimizations to efficiently find solutions for complex logic problems.

---

## ## Features

### ### Core Algorithm
* **Backtracking Search**: A recursive depth-first search that explores possible variable assignments.
* **AC-3 (Arc Consistency)**: An inference algorithm used to prune the search space by ensuring all variables satisfy constraints relative to their neighbors.

### ### Heuristics for Optimization
* **Minimum Remaining Values (MRV)**: Selects the variable with the fewest remaining legal values to fail fast.
* **Degree Heuristic**: Used as a tie-breaker for MRV, selecting the variable involved in the largest number of constraints on other unassigned variables.
* **Least Constraining Value (LCV)**: Orders values by their impact on neighboring variables, prioritizing those that leave the most options open.

---

## ## Technical Implementation

* **Constraint Handling**: Supports a variety of rules including `neq` (all-different), `eq`, `lt` (less than), `lte`, `gt`, `gte`, and `sum_eq`.
* **Domain Pruning**: Dynamically updates variable domains during search using a `Revise` function and constraint orientation.
* **Input/Output**: Processes standard JSON formatted CSP files and outputs the final solution or the reduced domains in a `_Solution.json` file.

---

## ## Usage

The solver requires a JSON file containing `variables`, `domains`, and `constraints`.

### ### How to Run
Run the solver from the command line by providing the name of your JSON file (without the `.json` extension):

```bash
python Project2.py <your_json_filename>
```

### ### Example Workflow
1.  **Input**: `problem.json`
2.  **Execution**: `python Project2.py problem`
3.  **Output**: `problem_Solution.json` containing the solved state.

---

## ## Author
**Jasser Hammami**
* **Course**: Computer Science
* **Version**: 1.0
