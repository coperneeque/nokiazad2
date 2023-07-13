#! /usr/bin/env python3

from random import randint, randrange
from timeit import default_timer as timer
from numpy import floor, log10
import sys
sys.path.append(".")
# from frac_search import frac_search
from load_balancer import Load_balancer as lb, Load_balancer
from test_load_balancer import TestLoad_balancer
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


# -------------------------------------------------------------------------------------
def time_test(num_runs = 10, magnitudes = [2, 3, 4, 5]):
    BASE = 10
    AVERAGE = 5

    balancer: Load_balancer = lb()

    times_stupid = []
    times_smart = []
    t1t2_alike = 0
    t1t2_diff = 0

    # for different amounts of data:
    for magnitude in magnitudes:
        print(f"=== {magnitude = }")
        times_stupid_magnitude = []
        times_smart_magnitude = []
        # for each amount perform number of tests
        for rn in range(num_runs):
            print(f"{rn = }", end="")
            arr = []
            idxs = None
            # randomly decide whether to test on a totally random array or a "good" one
            if randint(0, 2**31) % 2 == 0:
                print(", array: good")
                arr, idxs = TestLoad_balancer.prep_buffer(BASE**magnitude)
            else:
                print(", array: random")
                arr = [randrange(1, AVERAGE) for j in range(BASE**magnitude)]
            start_stupid = timer()
            t1t2_stupid = balancer.stupid(arr)
            stop_stupid = timer()
            start_smart = timer()
            t1t2_smart = balancer.smart(arr)
            stop_smart = timer()
            if t1t2_stupid == t1t2_smart:
                t1t2_alike += 1
                times_stupid_magnitude.append(stop_stupid - start_stupid)
                times_smart_magnitude.append(stop_smart - start_smart)
            else:
                print("!!! results don't match")
                t1t2_diff += 1
        times_stupid.append(sum(times_stupid_magnitude) / len(times_stupid_magnitude))
        times_smart.append(sum(times_smart_magnitude) / len(times_smart_magnitude))

    assert len(magnitudes) == len(times_stupid)
    assert len(magnitudes) == len(times_smart)

    # df = pd.DataFrame(columns=["size", "time_stupid", "time_smart"])
    df = pd.DataFrame.from_dict({ \
        "size": [BASE**m for m in magnitudes], \
        "time_stupid" : times_stupid, \
        "time_smart" : times_smart
        })
    print(magnitudes)
    print("size:\ttime stupid:\ttime smart:")
    for i in range(len(magnitudes)):
        print(BASE**magnitudes[i], "\t", times_stupid[i], "\t", times_smart[i])
    print(df)
    print("Done")

    return df


# -------------------------------------------------------------------------------------
def test_algos(algos: list, buf_len_magnitude: int, avg: int, num_tests: int) -> None:
    for algo in algos:
        print(f"======== Testing algorithm: {algo}\n\tnum_tetsts: {num_tests}\n\tmax_range: {avg}\n\tsize_arr: {buf_len_magnitude}")
        success = 0
        for i in range(num_tests):
            # arr = [randrange(1, avg) for j in range(buf_len_magnitude)]
            arr = lb.prep_buffer(buf_len_magnitude, avg)[0]
            ij = algo(arr)
            if ij:
                success += 1
                print(f"i : {ij[0]}\t\tj : {ij[1]}")
                print(arr)
                print(arr[:ij[0]])
                print(arr[ij[0] + 1:ij[1]])
                print(arr[ij[1] + 1:])
        print(f"Success: {success}/{num_tests}")


# -------------------------------------------------------------------------------------
def test_stupid(buf_len_magnitude: int, avg: int, num_tests: int) -> None:
    print(f"  Testing algorithm: stupid\n\tnum_tetsts: {num_tests}\n\tmax_range: {avg}\n\tsize_arr: {buf_len_magnitude}")
    success = 0
    for i in range(num_tests):
        # arr = [randrange(1, avg) for j in range(buf_len_magnitude)]
        arr = lb.prep_buffer(buf_len_magnitude, avg)[0]
        ij = lb.stupid(arr)
        if ij:
            success += 1
            print(f"i : {ij[0]}\t\tj : {ij[1]}")
            print(arr)
            print(arr[:ij[0]])
            print(arr[ij[0] + 1:ij[1]])
            print(arr[ij[1] + 1:])
    print(f"Success: {success}/{num_tests}")


# -------------------------------------------------------------------------------------
def test_smart(buf_len_magnitude: int, avg: int, num_tests: int) -> None:
    print(f"Testing algorithm: smart\n\t{num_tests = }\n\t{avg = }\n\t{buf_len_magnitude = }")
    success = 0
    for i in range(num_tests):
        # arr = [randrange(1, avg) for j in range(buf_len_magnitude)]
        arr = lb.prep_buffer(buf_len_magnitude, avg)[0]
        ij = lb.stupid(arr)
        if ij:
            success += 1
            print(f"i : {ij[0]}\t\tj : {ij[1]}")
            print(arr)
            print(arr[:ij[0]])
            print(arr[ij[0] + 1:ij[1]])
            print(arr[ij[1] + 1:])
    print(f"Success: {success}/{num_tests}")


# -------------------------------------------------------------------------------------
def main():
    MAX_RANGE = 10
    NUM_TESTS = 1000
    SIZE_ARR = 30

    # buf, idx = lb.prep_buffer(SIZE_ARR, MAX_RANGE)
    # print(buf)
    # print(idx)

    df = time_test(magnitudes=[2,3,4])
    ax = plt.axes()
    plt.yscale("log")
    ax.plot(df["size"], df["time_stupid"], color="red")
    ax.plot(df["size"], df["time_smart"], color="blue")
    plt.show()


# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
    # test_stupid(buf_len_magnitude=30, avg=10, num_tests=1)
    # test_smart(buf_len_magnitude=30, avg=10, num_tests=1)
    # test_algos([lb.stupid, lb.smart], buf_len_magnitude=30, avg=10, num_tests=1)
    # time_test(magnitudes=[2,3])
