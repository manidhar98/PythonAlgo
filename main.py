# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import re
import resource
import time
import tracemalloc

import memory_profiler
import dp_normal
import partb

class StringGenerator:
    X = ""
    Y = ""
    indices_x = []
    indices_y = []
    final_x = ""
    final_y = ""

    def __init__(self, strings):
        self.X = strings[0]
        self.Y = strings[1]

    def inputStringGenerator(self, str, indices):
        cummulative = str
        for x in indices:
            s = str[0:x + 1]
            s = s + cummulative
            s = s + str[x + 1:len(str)]
            str = s
            cummulative = s

        return str


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    strings = []
    indices_x = []
    indices_y = []
    index = 1
    pattern = re.compile("[A-Za-z]+")
    file = open('input.txt', 'r');
    data = file.readlines()
    strings.append(data[0].replace("\n", ""))
    check = False
    for x in range(1, len(data)):
        temp = data[x].replace("\n", "")
        if pattern.fullmatch(temp) is not None:
            strings.append(temp)
            check = True
        elif not check:
            indices_x.append(int(temp))
        else:
            indices_y.append(int(temp))
    print(strings)
    sg = StringGenerator(strings)
    final = [sg.inputStringGenerator(strings[0], indices_x), sg.inputStringGenerator(strings[1], indices_y)]

    print(final)
    n = dp_normal.normal(final)

    mismatch_penalty_matrix = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
    gap_penalty_value = 30


    x = final[0]
    y = final[1]
    tracemalloc.start()
    start = time.process_time()
    n.get_minimum_penalty(x, y, mismatch_penalty_matrix, gap_penalty_value)
    print("\n\nTime taken by get_minimum_penalty method: ", time.process_time() - start)
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    tracemalloc.stop()

    part_bO = partb.Optimised()
    # tracemalloc.start()
    # start = time.process_time()
    # part_bO.divide_conquer_alignment(x, y)
    # print('min_cost: ', part_bO.min_cost)
    # print("seq1: ", part_bO.final_seq_x)
    # print("seq2: ", part_bO.final_seq_y)
    # print("\nTime taken by get_minimum_penalty method: ", time.process_time() - start)
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    # tracemalloc.stop()

