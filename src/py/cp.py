import sys
import os
original_stdout = sys.stdout # Suppress load messages from ortools
sys.stdout = open(os.devnull, 'w')
from ortools.sat.python import cp_model
sys.stdout = original_stdout

TIME_LIMIT = None
if len(sys.argv) > 1:
    TIME_LIMIT = float(sys.argv[1])

n, k = map(int, sys.stdin.readline().split())
d, c, l, r = [], [], [], []
for _ in range(n):
    x, y = map(int, sys.stdin.readline().split())
    d.append(x)
    c.append(y)
for _ in range(k):
    x, y = map(int, sys.stdin.readline().split())
    l.append(x)
    r.append(y)
    
model = cp_model.CpModel()

x = {(i, j): model.NewBoolVar(f'x_{i}_{j}') for i in range(n) for j in range(k)}

for i in range(n):
    model.AddAtMostOne(x[i, j] for j in range(k))
for j in range(k):
    model.AddLinearConstraint(sum(x[i, j] * d[i] for i in range(n)), l[j], r[j])

model.Maximize(sum(x[i, j] * c[i] for i in range(n) for j in range(k)))

solver = cp_model.CpSolver()

if TIME_LIMIT is not None:
    solver.parameters.max_time_in_seconds = TIME_LIMIT
solver.parameters.num_search_workers = 16
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    assignment = []
    for i in range(n):
        for j in range(k):
            if solver.Value(x[i, j]) == 1:
                assignment.append((i + 1, j + 1))
                
    print(len(assignment))
    for i, j in assignment:
        print(i, j)
else:
    print(-1)