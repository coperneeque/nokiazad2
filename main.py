#! /usr/bin/env python3

from random import randint, randrange
from numpy import floor, log10
import sys
sys.path.append(".")
# from frac_search import frac_search
import unittest
from load_balancer import Load_balancer as lb


def time_test():
    NUM_RUNS = 1000
    balancer = lb()


# -------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------
def test_algos(algos, size_arr, max_range, num_tests):
    for algo in algos:
        print(f"======== Testing algorithm: {algo}\n\tnum_tetsts: {num_tests}\n\tmax_range: {max_range}\n\tsize_arr: {size_arr}")
        success = 0
        for i in range(num_tests):
            # arr = [randrange(1, max_range) for j in range(size_arr)]
            arr = lb.prep_buffer(size_arr, max_range)[0]
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
def test_stupid(size_arr: int, max_range: int, num_tests: int) -> None:
    print(f"  Testing algorithm: stupid\n\tnum_tetsts: {num_tests}\n\tmax_range: {max_range}\n\tsize_arr: {size_arr}")
    success = 0
    for i in range(num_tests):
        # arr = [randrange(1, max_range) for j in range(size_arr)]
        arr = lb.prep_buffer(size_arr, max_range)[0]
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
        # arr = [randrange(1, max_range) for j in range(size_arr)]
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

    buf, idx = lb.prep_buffer(SIZE_ARR, MAX_RANGE)
    print(buf)
    print(idx)


# -------------------------------------------------------------------------------------
if __name__ == '__main__':
    # main()
    # test_stupid(size_arr=30, max_range=10, num_tests=1)
    # test_smart(buf_len_magnitude=30, avg=10, num_tests=1)
    # test_algos([lb.stupid, lb.smart], size_arr=30, max_range=10, num_tests=1)
    time_test()
