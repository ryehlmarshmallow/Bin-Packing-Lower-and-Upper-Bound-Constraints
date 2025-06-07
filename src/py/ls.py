import random
import time
import sys

N, K = map(int, input().split())
items = [tuple(map(int, input().split())) for _ in range(N)]
trucks = [tuple(map(int, input().split())) for _ in range(K)]


def is_valid_state(N, K, state, items, trucks):
    weight = [0] * K

    # Tính tổng trọng lượng mỗi xe
    for i in range(N):
        if state[i] != 0:  # xét những đơn hàng đã được xếp
            weight[state[i] - 1] += items[i][0]

    # check upper, lower bound
    for j in range(K):
        if weight[j] > 0:  # chỉ check những xe có hàng
            if weight[j] < trucks[j][0] or weight[j] > trucks[j][1]:
                return False
    
    return True

def get_value(state, items):
    value = 0
    for i in range(len(items)):
        if state[i] != 0:
            value += items[i][1]
    return value

def generate_initial_state_greedy_random(N, K, items, trucks, perturb_rate=0.2):

    # Bước 1: Tạo trạng thái ban đầu theo Greedy
    state = [0] * N  # Khởi tạo trạng thái ban đầu (chưa phân bổ vật)
    weights = [0] * K  # Tổng trọng lượng của mỗi xe

    items_sorted = sorted(range(N), key=lambda x: items[x][1], reverse=True)
    
    for i in items_sorted:
        for j in range(K):
            if weights[j] + items[i][0] <= trucks[j][1]:  # Thỏa mãn upper bound
                state[i] = j + 1
                weights[j] += items[i][0]
                break

    # Bước 2: Điều chỉnh ngẫu nhiên
    num_random_changes = int(perturb_rate * N)  # Số lượng vật cần thay đổi
    for _ in range(num_random_changes):
        item_index = random.randint(0, N - 1)  # Chọn ngẫu nhiên một vật
        new_truck = random.randint(0, K)  # Gán vật đó cho xe khác (hoặc bỏ không)
        
        # Cập nhật trạng thái nếu hợp lệ
        if new_truck == 0 or (new_truck <= K and weights[new_truck - 1] + items[item_index][0] <= trucks[new_truck - 1][1]):
            if state[item_index] != 0:  # Gỡ trọng lượng khỏi xe cũ
                weights[state[item_index] - 1] -= items[item_index][0]
            state[item_index] = new_truck
            if new_truck != 0:  # Thêm trọng lượng vào xe mới
                weights[new_truck - 1] += items[item_index][0]

    return state

def generate_neighbors(N, K, current_state, items, trucks):
    neighbors = []
    for i in range(N):
        # Chỉ xét các đơn hàng chưa được gán xe
        if current_state[i] == 0:
            for j in range(1, K + 1):  # Chọn xe từ 1 đến K
                neighbor = current_state[:]
                neighbor[i] = j
                if is_valid_state(N, K, neighbor, items, trucks):
                    neighbors.append(neighbor)
    return neighbors

def Solve_Iterated_Local_Search(N, K, items, trucks, time_limit=5.0):
    start = time.time()
    current_state = generate_initial_state_greedy_random(N, K, items, trucks, perturb_rate=0.2)
    best_state = current_state[:]
    best_value = get_value(best_state, items) if is_valid_state(N, K, current_state, items, trucks) else 0
    max_value = sum(item[1] for item in items)

    while time.time() - start < time_limit:
    # for iteration in range(iterations):
        neighbors = generate_neighbors(N, K, current_state, items, trucks)
        if not neighbors:  # Nếu không tìm được hàng xóm
            current_state = generate_initial_state_greedy_random(N, K, items, trucks, perturb_rate=0.2)
            continue

        # Chọn hàng xóm
        best_neighbor = max(neighbors, key=lambda state: get_value(state, items))
        best_neighbor_value = get_value(best_neighbor, items)

        # Update state
        if best_neighbor_value >= best_value:
            best_state = best_neighbor
            best_value = best_neighbor_value
            current_state = best_neighbor
        else:
        # Restart
            current_state =  generate_initial_state_greedy_random(N, K, items, trucks, perturb_rate=0.2)

        # Dừng sớm nếu đạt được max
        if best_value == max_value:
            break
        # if iteration== iterations:
        #     best_value= get_value(best_state,items)
    end = time.time()
    exe_time = end- start
    return best_value, best_state , exe_time

time_limit = 5.0  # Default time limit
if len(sys.argv) > 1:
    time_limit = float(sys.argv[1])

value, state, time_ = Solve_Iterated_Local_Search(N, K, items, trucks, time_limit=time_limit)

if is_valid_state(N, K, state, items, trucks):
    ans = sum(1 for x in state if x > 0)
    print(ans)
    for i in range(N):
        if state[i] > 0:
            print(i+1,state[i])
else: 
    print(0)