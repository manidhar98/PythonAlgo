import time
import resource

base_string = "ACGT"


class normal:
    def __init__(self, strings):
        x = strings[0]
        y = strings[1]
        # mismatch_penalty_matrix = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]
        # gap_penalty_value = 30
        #
        # start = time.process_time()
        # self.get_minimum_penalty(x, y, mismatch_penalty_matrix, gap_penalty_value)
        # print("\n\nTime taken by get_minimum_penalty method: ", time.process_time() - start)
        # print("Memory used by the program: ", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

    def get_minimum_penalty(self, str1, str2, mismatch_penalty, gap_penalty):
        str1_length = len(str1)
        str2_length = len(str2)
        max_length = str1_length + str2_length

        dp = [[0 for i in range(str2_length + 1)] for j in range(str1_length + 1)]

        for i in range(0, str1_length + 1):
            dp[i][0] = i * gap_penalty
        for i in range(0, str2_length + 1):
            dp[0][i] = i * gap_penalty

        for i in range(1, str1_length + 1):
            for j in range(1, str2_length + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    mismatch_penalty_value = mismatch_penalty[base_string.index(str1[i - 1])][
                        base_string.index(str2[j - 1])]
                    dp[i][j] = min(dp[i - 1][j - 1] + mismatch_penalty_value,
                                   dp[i - 1][j] + gap_penalty,
                                   dp[i][j - 1] + gap_penalty)

        i = str1_length
        j = str2_length

        x_position = max_length
        y_position = max_length

        x_answer = [0 for i in range(max_length + 1)]
        y_answer = [0 for i in range(max_length + 1)]

        while not (i == 0 or j == 0):
            mismatch_penalty_value = mismatch_penalty[base_string.index(str1[i - 1])][base_string.index(str2[j - 1])]
            if str1[i - 1] == str2[j - 1]:
                x_answer[x_position] = ord(str1[i - 1])
                y_answer[y_position] = ord(str2[j - 1])
                x_position = x_position - 1
                y_position = y_position - 1
                i = i - 1
                j = j - 1
            elif dp[i - 1][j - 1] + mismatch_penalty_value == dp[i][j]:
                x_answer[x_position] = ord(str1[i - 1])
                y_answer[y_position] = ord(str2[j - 1])
                x_position = x_position - 1
                y_position = y_position - 1
                i = i - 1
                j = j - 1
            elif dp[i - 1][j] + gap_penalty == dp[i][j]:
                x_answer[x_position] = ord(str1[i - 1])
                y_answer[y_position] = ord('_')
                x_position = x_position - 1
                y_position = y_position - 1
                i = i - 1
            elif dp[i][j - 1] + gap_penalty == dp[i][j]:
                x_answer[x_position] = ord('_')
                y_answer[y_position] = ord(str2[j - 1])
                x_position = x_position - 1
                y_position = y_position - 1
                j = j - 1

        while x_position > 0:
            if i > 0:
                x_answer[x_position] = ord(str1[i - 1])
                x_position = x_position - 1
                i = i - 1
            else:
                x_answer[x_position] = ord('_')
                x_position = x_position - 1

        while y_position > 0:
            if j > 0:
                y_answer[y_position] = ord(str2[j - 1])
                y_position = y_position - 1
                j = j - 1
            else:
                y_answer[y_position] = ord('_')
                y_position = y_position - 1

        index = 1
        for i in range(max_length, 1, -1):
            if chr(y_answer[i]) == '_' and chr(x_answer[i]) == '_':
                index = i + 1
                break

        print("Minimum Penalty in aligning the sequences:")
        print(dp[str1_length][str2_length])
        print("The aligned genes are:")

        for i in range(index, max_length + 1):
            print(chr(x_answer[i]), end='')

        print()

        for i in range(index, max_length + 1):
            print(chr(y_answer[i]), end='')
