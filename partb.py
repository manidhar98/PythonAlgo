
delta = 30

chars = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}

mismatch_cost = [
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
]


min_cost = 0
final_seq_x = ''
final_seq_y = ''

def reconstruct_sequence_alignment(dp, X, Y):
    i = len(X)
    j = len(Y)

    X1 = ""
    Y1 = ""

    global min_cost
    while i!=0 and j !=0:

        if dp[i][j] == delta + dp[i][j-1]:
            X1 += '_'
            Y1 += Y[j-1]
            j -= 1
            min_cost += delta
        elif dp[i][j] == dp[i-1][j] + delta:
            X1 += X[i-1]
            Y1 += '_'
            i -= 1
            min_cost += delta
        else:
            X1 += X[i-1]
            Y1 += Y[j-1]
            i -= 1
            j -= 1 
            min_cost += mismatch_cost[chars[X[i]]][chars[Y[j]]]
    
    while i!=0:
        X1 += X[i]
        Y1 += "_"

        i -= 1
        min_cost += delta

    while j != 0:
        Y1 += Y[j]
        X1 += "_"

        j -= 1
        min_cost += delta

    # print(X1[::-1])
    # print(Y1[::-1])

    return (X1[::-1], Y1[::-1])


def alignment(X, Y):

    m = len(X)+1
    n = len(Y)+1

    dp = [ [0 for i in range(n)] for i in range(m)]

    for i in range(m):
        dp[i][0] = i*delta
    
    for i in range(n):
        dp[0][i] = i*delta

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + delta
            dp[i][j] = min(dp[i][j], dp[i][j-1]+delta)
            dp[i][j] = min(dp[i][j], dp[i-1][j-1]+mismatch_cost[chars[X[i-1]]][chars[Y[j-1]]])

    
    # with open('output.txt', 'wt') as f:
    #     # for i in range(n-1):
    #     #     f.write(str(Y[i])+ ',')
    #     # f.write(' \n')
    #     for i in range(m):
    #         # f.write(str(X[i])+',')
    #         for j in range(n):
    #             f.write(str(dp[i][j]))
    #             f.write(',')

    #         f.write(' \n')
    
    return reconstruct_sequence_alignment(dp, X, Y)

def space_efficient_alignment(X, Y):
    
    m = len(X)+1
    n = len(Y)+1

    # print('serving for:', X, Y)
    dp = [[0 for i in range(n)] for i in range(2)]


    for j in range(n):
        dp[0][j] = j*delta

    for i in range(1,m):
        dp[i%2][0] = i*delta

        for j in range(1,n):
            dp[i%2][j] = dp[i%2][j-1] + delta
            dp[i%2][j] = min(dp[i%2][j], dp[(i-1)%2][j] + delta)
            dp[i%2][j] = min(dp[i%2][j], dp[(i-1)%2][j-1] + mismatch_cost[chars[X[i-1]]][chars[Y[j-1]]])

            # print(i%2, j-1, '-' , (i-1)%2, j, '-',(i-1)%2, j-1)

            
        # print(dp)

    # print(dp[(m-1)%2][n-1])
    return dp[(m-1)%2]



def divide_conquer_alignment(X, Y):
    
    m = len(X)
    n = len(Y)

    if m<=2 or n <=2:
       X1, Y1 =  alignment(X, Y)

       global final_seq_x, final_seq_y
       final_seq_x += X1
       final_seq_y += Y1
       return

    x_split_pos = m//2

    y1_seq = space_efficient_alignment(X[:x_split_pos], Y)
    y2_seq = space_efficient_alignment(X[:x_split_pos - 1:-1], Y[::-1])[::-1]

    y_split_pos = 0
    min_seq = y1_seq[0] + y2_seq[0]
    for i in range(1, n):
        temp = y1_seq[i] + y2_seq[i]
        if (y1_seq[i] + y2_seq[i]) < min_seq:
            y_split_pos = i
            min_seq = y1_seq[i] + y2_seq[i]

    # global min_cost
    # min_cost += min_seq
    divide_conquer_alignment(X[:x_split_pos], Y[:y_split_pos])
    divide_conquer_alignment(X[x_split_pos: ], Y[y_split_pos:])


if __name__ == '__main__':

    X = "ACACTGACTACTGACTGGTGACTACTGACTGG"
    Y = "TATTATACGCTATTATACGCGACGCGGACGCG"

    # X = "TCAC"
    # Y = "TACCCCA"

    divide_conquer_alignment(X, Y)
    # alignment(X, Y)
    # space_efficient_alignment(X, Y)

    print('min cost: ', min_cost)
    print('seq1: ', final_seq_x)
    print('seq2: ', final_seq_y)


# ACACACTGAC_TACTGACTGGTG_ACTACTG_ACT_G_GACTGAC_TACT TAT_TA_TTATACG_CTA_TTATACG_CGACGCGGACGC_G_T_ATACG_
# CTACTG_ACT_G_GACTGAC_TACTGACTGGTG_ACTACTG_ACT_G_G_ G_CGACGCGGACGC_G_T_ATACG_CTA_TTATACG_CGACGCGGACGCG
# 0.224
# 31532