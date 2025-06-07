import sys
import os
original_stdout = sys.stdout # Suppress load messages from ortools
sys.stdout = open(os.devnull, 'w')
from ortools.linear_solver import pywraplp
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

solver = pywraplp.Solver.CreateSolver('BOP')

x = {(i, j): solver.BoolVar(f'x_{i}_{j}') for i in range(n) for j in range(k)}
for i in range(n):
    solver.Add(solver.Sum(x[i, j] for j in range(k)) <= 1)
for j in range(k):
    solver.Add(solver.Sum(x[i, j] * d[i] * 2 for i in range(n)) >= l[j] * 2 - 1)
    solver.Add(solver.Sum(x[i, j] * d[i] * 2 for i in range(n)) <= r[j] * 2 + 1)
    
solver.Maximize(solver.Sum(x[i, j] * c[i] for i in range(n) for j in range(k)))

if TIME_LIMIT is not None:
    solver.set_time_limit(int(TIME_LIMIT * 1000))

status = solver.Solve()
if status == pywraplp.Solver.OPTIMAL:
    assignment = []
    for i in range(n):
        for j in range(k):
            if x[i, j].solution_value() == 1:
                assignment.append((i + 1, j + 1))
    
    print(len(assignment))
    for i, j in assignment:
        print(i, j)
else:
    print(-1)