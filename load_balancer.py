class Load_balancer :
    def __init__(self):
        pass

    # -------------------------------------------------------------------------------------
    def frac_search(self, F, fraction):
        '''
        Binary search index of element dividing the integral in two at given ratio.
        The ratio is as close as int division allows.
        :param F: integral of array to search through
        :param fraction: fraction of integral to look for
        :return: index of fraction
        '''
        target = F[-1] * fraction
        lower = 0
        upper = len(F)
        mid = upper // 2
        found = False
        while not found:
            # check if index is found:
            # F is strong monotonic
            if F[mid] >= target and F[mid - 1] < target:
                found = True
                break
            # if index is not found then check left-right:
            if F[mid] > target:  # go left:
                upper = mid
            else:  # go right:
                lower = mid
            mid = (upper + lower) // 2

        return mid

    # -------------------------------------------------------------------------------------
    def stupid(self, arr):
        '''
        Greedy bruteforce - check all possible pairs of indexes.
        :param arr: array to partition into 3 partitions
        :return: two indexes that partition the array or False
        '''
        assert len(arr) >= 5

        arr_integral = [arr[0]]
        for i in range(1, len(arr)):
            arr_integral.append(arr_integral[i - 1] + arr[i])
        assert len(arr_integral) == len(arr)

        idx = self.frac_search(arr_integral, 1 / 3)
        # print(arr)
        # print(arr_integral)
        # print(idx, '\n')

        # O(N^2)
        for t1 in range(1, len(arr) - 3):
            for t2 in range(len(arr) - 2, t1 + 1, -1):
                if arr_integral[t1 - 1] == arr_integral[-1] - arr_integral[t2]:  # 1st buffer equals 3rd buffer
                    if arr_integral[t2 - 1] - arr_integral[t1] == arr_integral[t1 - 1]:  # check 1st and 2nd buffer
                        return t1, t2  # match

        return False

    # -------------------------------------------------------------------------------------
    def smart(self, arr):
        if len(arr) < 5:
            return False

        # integrate arr:                      O(N)
        arr_integral = [arr[0]]
        for i in range(1, len(arr)):
            arr_integral.append(arr_integral[i - 1] + arr[i])
        assert len(arr_integral) == len(arr)

        # find candidates:                  O(log N)
        t1 = self.frac_search(arr_integral, 1 / 3)
        t2 = self.frac_search(arr_integral, 2 / 3)

        # verify t1 and t2:                 O(1)
        # w1_load = arr_integral[t1 - 1]
        # w3_load = arr_integral[-1] - arr_integral[t2]
        # w2_load = arr_integral[t2 - 1] - arr_integral[t1]
        # if w1_load == w2_load and w2_load == w3_load:
        #     return t1, t2

        # try shifting by a few steps:      O(N)
        w2_load_temp = arr_integral[t2 - 1] - arr_integral[t1]
        t1_shifted = t1
        # shifting left:
        while w2_load_temp <= arr_integral[-1] * 1 / 3:
            t1_shifted -= 1
            w2_load_temp = arr_integral[t2 - 1] - arr_integral[t1_shifted]

        w2_load_temp = arr_integral[t2 - 1] - arr_integral[t1]
        t2_shifted = t2
        # shifting right:
        while w2_load_temp <= arr_integral[-1] * 1 / 3:
            t2_shifted += 1
            w2_load_temp = arr_integral[t2_shifted - 1] - arr_integral[t1]

        # check all possibilities between t1_shifted - t1 and t2 - t2_shifted:      O(N^2)
        # start from top - better chance of getting a hit (i think):
        for t1i in range(t1, t1_shifted - 1, -1):
            w1_load = arr_integral[t1i - 1]
            for t2j in range(t2, t2_shifted + 1):
                w3_load = arr_integral[-1] - arr_integral[t2j]
                w2_load = arr_integral[t2j - 1] - arr_integral[t1i]
                if w1_load == w2_load and w2_load == w3_load:
                    return t1i, t2j

        return False

