#include <bits/stdc++.h>

using namespace std;

int n, k;
int d[1000], c[1000], l[100], r[100];
int best_cost = 0;
vector<int> best_assignment(n, -1);

vector<int> greedy(const vector<int> order_indices)
{
    vector<int> assignment(n, -1);
    vector<bool> vehicle_used(k, false);
    while (true)
    {
        bool is_changed = false;
        for (int j = 0; j < k; ++j)
        {
            if (vehicle_used[j])
                continue;
            int total_quantity = 0;
            vector<int> potential_orders;
            for (int i : order_indices)
                if (assignment[i] == -1 && total_quantity + d[i] <= r[j])
                {
                    total_quantity += d[i];
                    potential_orders.push_back(i);
                }
            if (total_quantity >= l[j])
            {
                is_changed = true;
                vehicle_used[j] = true;
                for (int i : potential_orders)
                    assignment[i] = j;
            }
        }
        if (!is_changed)
            break;
    }
    return assignment;
}

void check(const vector<int> &assignment)
{
    int cost = 0;
    for (int i = 0; i < n; ++i)
        if (assignment[i] != -1)
            cost += c[i];
    if (cost > best_cost)
    {
        best_cost = cost;
        best_assignment = assignment;
    }
}

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    cin >> n >> k;
    for (int i = 0; i < n; ++i)
        cin >> d[i] >> c[i];
    for (int i = 0; i < k; ++i)
        cin >> l[i] >> r[i];

    vector<int> order_indices(n);
    iota(order_indices.begin(), order_indices.end(), 0);
    sort(order_indices.begin(), order_indices.end(),
         [](int x, int y)
         { return c[x] > c[y]; });
    check(greedy(order_indices));
    sort(order_indices.begin(), order_indices.end(),
         [](int x, int y)
         { return (double)c[x] / d[x] > (double)c[y] / d[y]; });
    check(greedy(order_indices));

    cout << count_if(best_assignment.begin(), best_assignment.end(),
             [](int x)
             { return x != -1; }) << '\n';
    for (int i = 0; i < n; ++i)
        if (best_assignment[i] != -1)
            cout << i + 1 << ' ' << best_assignment[i] + 1 << '\n';

    return 0;
}