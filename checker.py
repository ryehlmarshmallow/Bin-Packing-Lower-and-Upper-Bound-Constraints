import os
import sys
import argparse
import subprocess
import time
import psutil
import numpy as np
import pandas as pd


def process_output(output: str, input_data: tuple[int, int, list[int], list[int], list[int], list[int]]) -> int | None:
    lines = output.strip().split('\n')
    if not lines or len(lines) < 1:
        raise ValueError('Output is empty or malformed')

    m = int(lines[0])
    if m == -1:
        return None
    if len(lines) != m + 1:
        raise ValueError(
            f'Output m = {m} does not match the expected number of assignments, which is {len(lines) - 1}')

    assignment = []
    for line in lines[1:]:
        if not line.strip():
            raise ValueError('Empty line in output')
        order, vehicle = map(int, line.split())
        assignment.append((order, vehicle))

    n, k, d, c, l, r = input_data
    quantity = [0] * k
    total_cost = 0
    for order, vehicle in assignment:
        if order < 1 or order > n or vehicle < 1 or vehicle > k:
            raise ValueError(
                f'Invalid assignment: order {order}, vehicle {vehicle}')
        quantity[vehicle - 1] += d[order - 1]
        total_cost += c[order - 1]
    for j in range(k):
        if (quantity[j] < l[j] or quantity[j] > r[j]) and quantity[j] != 0:
            raise ValueError(
                f'vehicle {j + 1} has quantity {quantity[j]} out of bounds [{l[j]}, {r[j]}]')
    return total_cost


def process_input(input_filepath: str) -> tuple[int, int, list[int], list[int], list[int], list[int]]:
    with open(input_filepath, 'r') as file:
        n, k = map(int, file.readline().split())
        d, c, l, r = [], [], [], []
        for _ in range(n):
            x, y = map(int, file.readline().split())
            d.append(x)
            c.append(y)
        for _ in range(k):
            x, y = map(int, file.readline().split())
            l.append(x)
            r.append(y)
    return n, k, d, c, l, r


def execute(program_path: str, input_filepath: str, time_limit: float = 5.0) -> tuple[str, float, int]:
    args = ['python', program_path, str(time_limit)] if program_path.endswith(
        '.py') else [program_path, str(time_limit)]
    with open(input_filepath, 'r') as input_file:
        start = time.time()
        process = subprocess.Popen(
            args,
            stdin=input_file,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            text=True,
        )

        ps_process = psutil.Process(process.pid)
        memory_usage = 0
        while process.poll() is None:
            memory_usage = max(memory_usage, ps_process.memory_info().rss)

        end = time.time()
        duration = end - start
        stdout, stderr = process.communicate()
        return stdout, duration, memory_usage


def benchmark(program_path: str, input_filepath: str, time_limit: float = 5.0) -> tuple[str | None, float | None, int | None]:
    input_data = process_input(input_filepath)

    output, duration, memory_usage = execute(
        program_path, input_filepath, time_limit)
    try:
        processed_output = process_output(output, input_data)
        if not processed_output:
            return None, duration, memory_usage
    except ValueError as e:
        raise ValueError(
            f'Invalid output from program {program_path} with input file {input_filepath}: {str(e)}')

    return output, duration, memory_usage


def convert_memory_usage(memory_usage: int | None) -> str | None:
    if memory_usage is None:
        return None
    if memory_usage < 1024:
        return f'{memory_usage} B'
    elif memory_usage < 1024 * 1024:
        return f'{memory_usage / 1024:.2f} KB'
    elif memory_usage < 1024 * 1024 * 1024:
        return f'{memory_usage / (1024 * 1024):.2f} MB'
    else:
        return f'{memory_usage / (1024 * 1024 * 1024):.2f} GB'


def main() -> None:
    programs_folder = 'dist'
    tests_folder = 'test'

    # os.system('make all')

    programs = os.listdir(programs_folder)
    test_types = ['judge', 'random', 'close', 'tight']
    tests = ['{}_{:02d}.inp'.format(type, i)
             for type in test_types for i in range(1, 11)]
    print('Test list: ', tests)

    for program in programs:
        if not os.path.isfile(os.path.join(programs_folder, program)):
            raise FileNotFoundError(
                f'Program file {program} not found in {programs_folder}. Please check the file path.')
    for test in tests:
        if not os.path.isfile(os.path.join(tests_folder, test)):
            raise FileNotFoundError(
                f'Test file {test} not found in {tests_folder}. Please check the file path.')

    test_parameters = []
    for test in tests:
        with open(os.path.join(tests_folder, test), 'r') as f:
            n, k = map(int, f.readline().split())
            test_parameters.append((test.split('.')[0], n, k))

    index = pd.MultiIndex.from_tuples(
        test_parameters, names=['Test', 'N', 'K'])

    stats = ['Result', 'Time', 'Memory']

    columns = pd.MultiIndex.from_product(
        [[program.split('.')[0] for program in programs], stats])

    if os.path.exists(pickle_file):
        print(f'Loading existing data from {pickle_file}...')
        df = pd.read_pickle(pickle_file)
        if not df.index.equals(index) or not df.columns.equals(columns):
            raise ValueError(
                'The structure of the DataFrame does not match the expected structure.')
    else:
        df = pd.DataFrame(columns=columns, index=index)

    for program in programs:
        for test_index, test in enumerate(tests):
            program_name = program.split('.')[0]
            if not pd.isna(df.at[test_parameters[test_index], (program_name, stats[0])]):
                print(f'Skipping {program} on {test}, already executed.')
                continue

            output, duration, memory_usage = benchmark(
                os.path.join(programs_folder, program),
                os.path.join(tests_folder, test),
                time_limit=TIME_LIMIT,
            )

            Result = process_output(output, process_input(
                os.path.join(tests_folder, test))) if output else None
            Time = duration if Result is not None else None
            Memory = convert_memory_usage(
                memory_usage) if Result is not None else None
            for stat in stats:
                df.at[test_parameters[test_index], (program_name, stat)] = locals()[
                    stat]
            df.to_pickle(pickle_file)
            print(f'{program} on {test} is executed.',
                  'No output.' if not Result else f'{Time} seconds, {Memory} memory.')

    df = df.convert_dtypes()
    print(df)

    column_format = '|' + 'c' * \
        len(test_parameters[0]) + ('|' + 'c' *
                                   len(stats)) * len(programs) + '|'
    with open('data.tex', 'w') as f:
        f.write(df.to_latex(sparsify=True, escape=True, longtable=True, column_format=column_format,
                float_format='%.3f', multicolumn_format='c|', multirow=False, na_rep='N/A'))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Benchmark programs against test cases.')
    parser.add_argument('-t', '--time_limit', type=float, default=5.0,
                        help='Time limit for each program execution in seconds.')
    parser.add_argument('-r', '--reset', action='store_true', default=False,
                        help='Reset the data file before running benchmarks.')

    args = parser.parse_args()

    TIME_LIMIT = args.time_limit

    pickle_file = 'data.pkl'
    if args.reset:
        if os.path.exists(pickle_file):
            os.remove(pickle_file)
            print('Data file reset.')
        else:
            print('No data file to reset.')

    main()
