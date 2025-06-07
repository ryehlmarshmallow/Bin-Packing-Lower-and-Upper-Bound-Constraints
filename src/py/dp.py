def bin_packing_dp(n, k, orders, vehicles):
    assigned = [False] * n
    assignments = []

    for v_id in range(k):
        c1, c2 = vehicles[v_id]
        capacity_limit = c2
        dp = [(-1, []) for _ in range(capacity_limit + 1)]
        dp[0] = (0, []) 

        for i in range(n):
            if assigned[i]:
                continue
            d_i, c_i = orders[i]
            for w in range(capacity_limit, d_i - 1, -1):
                prev_cost, prev_list = dp[w - d_i]
                if prev_cost != -1:
                    new_cost = prev_cost + c_i
                    if new_cost > dp[w][0]:
                        dp[w] = (new_cost, prev_list + [i])

        best_w = -1
        best_cost = -1
        best_orders = []

        for w in range(c1, c2 + 1):
            cost, order_list = dp[w]
            if cost > best_cost:
                best_cost = cost
                best_w = w
                best_orders = order_list

        if best_cost == -1:
            continue 

        for i in best_orders:
            assignments.append((i + 1, v_id + 1)) 
            assigned[i] = True

    print(len(assignments))
    assignments.sort(key = lambda x: x[0])
    for a in assignments:
        print(a[0], a[1])
n,k = map(int, input().split())
orders = []
for i in range(n):
    j1,j2 = map(int,input().split())
    orders.append((j1,j2))
vehicles = []
for i in range(k):
    j1,j2 = map(int, input().split())
    vehicles.append((j1,j2))
bin_packing_dp(n, k, orders, vehicles)