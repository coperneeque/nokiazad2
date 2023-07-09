from random import randrange
from numpy import floor, log10
from unittest import TestCase
from load_balancer import Load_balancer


class TestLoad_balancer(TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.balancer = Load_balancer()
        self.arr, self.idxs = self.prep_buffer(buf_len_magnitude=100000, avg=10000)
        self.idxs = tuple(self.idxs)

        # -------------------------------------------------------------------------------------
    def prep_buffer(buf_len_magnitude, avg=5, divs=3):
        '''
        Fill the buffer in a way that for sure can be partitioned into divs partitions.
        Each cell contains on average avg units.

        :param divs: number of partitions
        :param buf_len_magnitude:   magnitude of the total length of the buffer will be calculated as 10 ** floor( log10(buf_len_magnitude)).
                                    to create a partitionable buffer, the length might need to be adjusted.
                                    the length will be equal to the calculated magnitude or exceeding by as little as possible.
                                    eg: buf_len_magnitude == 55 -> log10(55) == 1.74 floor(...) == 1.0; 10 ** 1.0 == 10
                                        resulting buffer will be of length 10 or slightly larger.
        :param avg:     average number of units in each cell.
        :return:        filled buffer, partition indexes.
        '''

        BASE = 10
        BUF_LEN_MIN = 10
        CHUNK_LEN_MIN = 3

        buf_len_estimate = BASE ** int(floor(log10(buf_len_magnitude)))  # maybe add log base control
        chunk_len_estimate = buf_len_estimate // divs
        # we don't want to play with too small numbers:
        assert buf_len_estimate >= BUF_LEN_MIN
        assert chunk_len_estimate >= CHUNK_LEN_MIN

        # print(f"{buf_len_estimate = }")
        # print(f"{chunk_len_estimate = }")

        buf_result = []
        part_idxs = []
        chunk_load = (avg) * chunk_len_estimate

        for div in range(divs):
            to_load = chunk_load
            chunk = []
            while to_load > 2 * avg:
                x = randrange(1, 2 * avg + 1)
                chunk.append(x)
                to_load -= x
            chunk.append(to_load)
            assert sum(chunk) == chunk_load
            # this chunk is ready:
            buf_result.extend(chunk)
            # the dropped request - as per task description:
            buf_result.append(randrange(1, 2 * avg + 1))
            part_idxs.append(len(buf_result) - 1)
            # print(f"{len(chunk) = }")

        buf_result.pop()
        part_idxs.pop()

        # print(f"{buf_result = }")
        # print(f"{len(buf_result) = }")

        return buf_result, part_idxs

    def test_stupid(self):
        t1t2 = self.balancer.stupid(self.arr)
        self.assertTupleEqual(tuple1=t1t2, tuple2=self.idxs, msg="Indexes not match")

    def test_smart(self):
        t1t2 = self.balancer.smart(self.arr)
        self.assertTupleEqual(tuple1=t1t2, tuple2=self.idxs, msg="Indexes not match")
