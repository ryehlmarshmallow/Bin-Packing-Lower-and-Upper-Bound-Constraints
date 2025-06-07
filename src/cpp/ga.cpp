#include <bits/stdc++.h>

using namespace std;

double time_limit = 1.0;

int n, k;
int d[1000], c[1000], l[100], r[100];

chrono::high_resolution_clock::time_point start;

class genetic_algorithm
{
    const size_t POPULATION_SIZE;
    const double CROSSOVER_RATE;
    const double MUTATION_RATE;
    const size_t TOURNAMENT_SIZE;

    const size_t ELITISM_SIZE;
    
    struct individual
    {
        vector<int> assignment;
        int fitness;

        individual() : assignment(n, -1), fitness(0) {}

        friend bool operator<(const individual &lhs, const individual &rhs)
        {
            return lhs.fitness > rhs.fitness;
        }

        individual &operator=(const individual &other)
        {
            if (this != &other)
            {
                assignment = other.assignment;
                fitness = other.fitness;
            }
            return *this;
        }
    };

    vector<individual> population;
    mt19937 rng;

public:
    genetic_algorithm(size_t population_size, double crossover_rate, double mutation_rate, double elitism_rate, size_t tournament_size, uint64_t seed)
        : POPULATION_SIZE(population_size), CROSSOVER_RATE(crossover_rate), MUTATION_RATE(mutation_rate), TOURNAMENT_SIZE(tournament_size), ELITISM_SIZE(static_cast<size_t>(population_size * elitism_rate)), rng(seed)
    {
        population.resize(POPULATION_SIZE);
    }

    void generate_random_individual(individual &ind)
    {
        vector<int> order_indices(n), vehicle_indices(k);
        iota(order_indices.begin(), order_indices.end(), 0);
        iota(vehicle_indices.begin(), vehicle_indices.end(), 0);
        shuffle(order_indices.begin(), order_indices.end(), rng);
        shuffle(vehicle_indices.begin(), vehicle_indices.end(), rng);
        while (true)
        {
            bool is_changed = false;
            for (int vehicle : vehicle_indices)
            {
                int total_quantity = 0;
                vector<int> potential_orders;
                for (int order : order_indices)
                    if (ind.assignment[order] == -1 && total_quantity + d[order] <= r[vehicle])
                    {
                        total_quantity += d[order];
                        potential_orders.push_back(order);
                    }
                if (total_quantity >= l[vehicle])
                {
                    for (int order : potential_orders)
                        ind.assignment[order] = vehicle;
                    is_changed = true;
                }
            }
            if (!is_changed)
                break;
        }
    }

    int calculate_fitness(individual &ind)
    {
        int fitness = 0;
        vector<int> cost(k, 0), quantity(k, 0);
        for (int i = 0; i < n; ++i)
            if (ind.assignment[i] != -1)
            {
                quantity[ind.assignment[i]] += d[i];
                cost[ind.assignment[i]] += c[i];
            }
        for (int j = 0; j < k; ++j)
            if (quantity[j] >= l[j] && quantity[j] <= r[j])
                fitness += cost[j];
        return fitness;
    }

    void initialize()
    {
        for (auto &ind : population)
        {
            generate_random_individual(ind);
            ind.fitness = calculate_fitness(ind);
        }
    }

    individual crossover(const individual &parent1, const individual &parent2)
    {
        individual child;
        if (uniform_real_distribution<double>(0.0, 1.0)(rng) < CROSSOVER_RATE)
        {
            for (int i = 0; i < n; ++i)
            {
                if (uniform_real_distribution<double>(0.0, 1.0)(rng) < 0.5)
                    child.assignment[i] = parent1.assignment[i];
                else
                    child.assignment[i] = parent2.assignment[i];
            }
        }
        else
            child = parent1;
        return child;
    }

    void mutate(individual &ind)
    {
        if (uniform_real_distribution<double>(0.0, 1.0)(rng) < MUTATION_RATE)
        {
            int num_mutations = std::uniform_int_distribution<int>(1, std::max(1, n / 5))(rng);

            for (int m = 0; m < num_mutations; m++)
            {
                int order_idx = std::uniform_int_distribution<int>(0, n - 1)(rng);
                int new_assignment = std::uniform_int_distribution<int>(-1, k - 1)(rng);
                ind.assignment[order_idx] = new_assignment;
            }
        }
    }

    size_t tournament_selection()
    {
        size_t best_index = uniform_int_distribution<int>(0, POPULATION_SIZE - 1)(rng);
        for (size_t i = 1; i < TOURNAMENT_SIZE; ++i)
        {
            int index = uniform_int_distribution<int>(0, POPULATION_SIZE - 1)(rng);
            if (population[index] < population[best_index])
                best_index = index;
        }
        return best_index;
    }

    void evolve()
    {
        vector<individual> new_population;
        new_population.reserve(POPULATION_SIZE);
        nth_element(population.begin(), population.begin() + ELITISM_SIZE, population.end());

        for (size_t i = 0; i < ELITISM_SIZE; ++i)
            new_population.push_back(population[i]);
        while (new_population.size() < POPULATION_SIZE)
        {
            size_t parent1_index = tournament_selection();
            size_t parent2_index = tournament_selection();
            individual child = crossover(population[parent1_index], population[parent2_index]);
            mutate(child);
            child.fitness = calculate_fitness(child);
            new_population.push_back(child);
        }

        population = move(new_population);
    }

    void print_individual(const individual &ind)
    {
        vector<int> quantity(k, 0);
        vector<bool> valid(k, false);
        for (int i = 0; i < n; ++i)
            if (ind.assignment[i] != -1)
                quantity[ind.assignment[i]] += d[i];
        for (int j = 0; j < k; ++j)
            if (quantity[j] >= l[j] && quantity[j] <= r[j])
                valid[j] = true;

        cout << count_if(ind.assignment.begin(), ind.assignment.end(),
                         [&](int x)
                         { return (int)valid[x]; })
             << '\n';
        for (int i = 0; i < n; ++i)
            if (ind.assignment[i] != -1 && valid[ind.assignment[i]])
                cout << i + 1 << ' ' << ind.assignment[i] + 1 << '\n';
    }

    void run()
    {
        initialize();
        while (chrono::duration<double>(chrono::high_resolution_clock::now() - start).count() < time_limit)
            evolve();
        print_individual(*min_element(population.begin(), population.end()));
    }
};

int main(int argc, char *argv[])
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    if (argc > 1)
        time_limit = atof(argv[1]);

    start = chrono::high_resolution_clock::now();
    cin >> n >> k;
    for (int i = 0; i < n; ++i)
        cin >> d[i] >> c[i];
    for (int i = 0; i < k; ++i)
        cin >> l[i] >> r[i];

    genetic_algorithm ga(500, 0.5, 0.1, 0.1, 3, chrono::high_resolution_clock::now().time_since_epoch().count());
    ga.run();

    return 0;
}