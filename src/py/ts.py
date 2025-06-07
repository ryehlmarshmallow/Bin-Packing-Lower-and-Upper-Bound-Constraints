import random
import time
import sys

class Order:
    def __init__(self, id, quantity, cost):
        self.id = id
        self.quantity = quantity
        self.cost = cost
        self.ratio = cost / quantity if quantity > 0 else 0

class Vehicle:
    def __init__(self, id, low_capacity, up_capacity):
        self.id = id
        self.low_capacity = low_capacity
        self.up_capacity = up_capacity

class Solution:
    def __init__(self, N, K, orders, vehicles):
        self.N = N
        self.K = K
        self.orders = orders
        self.vehicles = vehicles
        self.assignment = [0] * (N + 1)
        self.vehicle_loads = [0] * (K + 1)
        self.total_cost = 0

    def calculate_cost_and_loads(self):
        self.vehicle_loads = [0] * (self.K + 1)
        self.total_cost = 0
        for i in range(1, self.N + 1):
            v = self.assignment[i]
            if v != 0:
                self.vehicle_loads[v] += self.orders[i-1].quantity
                self.total_cost += self.orders[i-1].cost

    def get_fitness(self, alpha, beta):
        self.calculate_cost_and_loads()
        penalty = 0
        for k in range(1, self.K + 1):
            load = self.vehicle_loads[k]
            low_cap = self.vehicles[k-1].low_capacity
            up_cap = self.vehicles[k-1].up_capacity
            if load > 0 and load < low_cap:
                penalty += alpha * (low_cap - load)
            elif load > up_cap:
                penalty += beta * (load - up_cap)
        return self.total_cost - penalty

    def is_feasible(self):
        self.calculate_cost_and_loads()
        for k in range(1, self.K + 1):
            load = self.vehicle_loads[k]
            low = self.vehicles[k-1].low_capacity
            up = self.vehicles[k-1].up_capacity
            if load > 0 and (load < low or load > up):
                return False
        return True

def initial_greedy_solution(N, K, orders, vehicles):
    sol = Solution(N, K, orders, vehicles)
    unassigned = set(range(1, N + 1))
    sorted_orders = sorted(orders, key=lambda o: o.ratio, reverse=True)
    for vehicle in vehicles:
        load = 0
        for order in sorted_orders:
            if order.id in unassigned and load + order.quantity <= vehicle.up_capacity:
                sol.assignment[order.id] = vehicle.id
                load += order.quantity
                unassigned.remove(order.id)
                if load >= vehicle.low_capacity:
                    break
    sol.calculate_cost_and_loads()
    return sol

def generate_neighbors(current, orders, vehicles, N, K, alpha, beta, iteration, tabu_list, tabu_tenure, best_fitness):
    neighbors = []
    candidate_ids = random.sample(range(1, N + 1), min(20, N))
    for oid in candidate_ids:
        from_v = current.assignment[oid]
        for to_v in [0] + random.sample(range(1, K + 1), min(3, K)):
            if to_v == from_v:
                continue
            neighbor = Solution(N, K, orders, vehicles)
            neighbor.assignment = current.assignment[:]
            neighbor.assignment[oid] = to_v
            move = (oid, from_v, to_v)
            is_tabu = any(m[0] == oid and m[1] == to_v and m[2] == from_v and m[3] > iteration for m in tabu_list)
            fitness = neighbor.get_fitness(alpha, beta)
            if is_tabu and fitness <= best_fitness:
                continue
            neighbors.append((neighbor, fitness, move))
    return neighbors

def tabu_search(N, K, orders, vehicles, time_limit, tabu_tenure, alpha, beta):
    current = initial_greedy_solution(N, K, orders, vehicles)
    current_fitness = current.get_fitness(alpha, beta)
    best = current
    best_fitness = current_fitness
    best_feasible = current if current.is_feasible() else None
    tabu_list = []

    #print(f"Initial fitness: {current_fitness:.2f}, Feasible: {current.is_feasible()}")
    start = time.time()
    it = 0
    while time.time() - start < time_limit:
        neighbors = generate_neighbors(current, orders, vehicles, N, K, alpha, beta, it, tabu_list, tabu_tenure, best_fitness)
        if not neighbors:
            continue
        neighbors.sort(key=lambda x: x[1], reverse=True)
        next_sol, next_fitness, move = neighbors[0]
        current = next_sol
        current_fitness = next_fitness
        tabu_list.append((move[0], move[2], move[1], it + tabu_tenure))
        tabu_list = [m for m in tabu_list if m[3] > it]

        if current_fitness > best_fitness:
            best = current
            best_fitness = current_fitness

        if current.is_feasible() and (best_feasible is None or current.total_cost > best_feasible.total_cost):
            best_feasible = current
            
        it += 1

    #print("\n--- Tabu Search Result ---")
    if best_feasible:
        #print(f"Feasible Solution Found, Total Cost: {best_feasible.total_cost}")
        assigned = [(i, best_feasible.assignment[i]) for i in range(1, N+1) if best_feasible.assignment[i] != 0]
        print(len(assigned))
        for i, v in assigned:
            print(i, v)
    else:
        # print("No feasible solution found.")
        print(0)

def read_input():
    N, K = map(int, input().split())
    orders = [Order(i + 1, *map(int, input().split())) for i in range(N)]
    vehicles = [Vehicle(k + 1, *map(int, input().split())) for k in range(K)]
    return N, K, orders, vehicles

if __name__ == "__main__":
    time_limit = 5.0
    if len(sys.argv) > 1:
        time_limit = float(sys.argv[1])
    
    N, K, orders, vehicles = read_input()
    tabu_search(N, K, orders, vehicles, time_limit=time_limit, tabu_tenure=17, alpha=100, beta=100)