# This is the global alignment.
# Author: Hao Li
CONFIG_PATH = '/Users/saw008/Studies/CWRU/2019.Fall/EECS_458-Intro to Bioinformatics/Homework/W2/test_config.txt'


def read_config(file_path):
    with open(file_path) as file:
        file_content = []
        for line in file.readlines():
            line = line.strip('\n')
            file_content.append(line)
    alignment_type = file_content[0]
    score_assignment = file_content[1].split(' ')
    match_score = score_assignment[0]
    mismatch_score = score_assignment[1]
    # gap_score here means insertion/deletion score
    gap_score = score_assignment[2]
    sequence_1 = file_content[2]
    sequence_2 = file_content[3]
    if alignment_type == 'g':
        gl_al(match_score, mismatch_score, gap_score, sequence_1, sequence_2)
    elif alignment_type == 'l':
        lo_al(match_score, mismatch_score, gap_score, sequence_1, sequence_2)
    else:
        print('Cannot recognize alignment type, please check your config file.')
        exit(0)


def gl_al(match_score, mismatch_score, gap_score, sequence_1, sequence_2):
    no_of_columns = len(sequence_1) + 1
    no_of_rows = len(sequence_2) + 1
    route_all = []
    real_route = []
    output_s1 = ''
    output_s2 = ''

    # no_of_columns = 4
    # no_of_rows = 5

    # note: i is a number, gap_score is a character.
    match_score = int(match_score)
    mismatch_score = int(mismatch_score)
    gap_score = int(gap_score)
    # the first parameter indicates columns, and the second indicates rows
    score_matrix = [[0] * no_of_columns for _ in range(no_of_rows)]
    # print(score_matrix)

    for i in range(no_of_columns):
        score_matrix[0][i] = i * gap_score
    for i in range(no_of_rows):
        score_matrix[i][0] = i * gap_score

    # i is row #, j is column #
    for i in range(no_of_rows):
        for j in range(no_of_columns):
            if i == 0 or j == 0:
                pass
            else:
                temp_up = score_matrix[i - 1][j] + gap_score
                temp_left = score_matrix[i][j - 1] + gap_score
                tmp = match_score if sequence_1[j - 1] == sequence_2[i - 1] else mismatch_score
                temp_diagonal = score_matrix[i - 1][j - 1] + tmp
                score_matrix[i][j] = max(temp_up, temp_left, temp_diagonal)
                # the following is to note down the route of assigning new values.
                if temp_up == max(temp_up, temp_left, temp_diagonal):
                    route_all.append('u')
                elif temp_left == max(temp_up, temp_left, temp_diagonal):
                    route_all.append('l')
                else:
                    route_all.append('d')
    # the following part is to find the path

    last_bit_index = len(route_all) - 1
    current_bit = last_bit_index
    while current_bit >= 0:
        if route_all[current_bit] == 'u':
            current_bit = current_bit - no_of_columns + 1
            real_route.append('u')
        elif route_all[current_bit] == 'l':
            current_bit = current_bit - 1
            real_route.append('l')
        else:
            current_bit = current_bit - no_of_columns
            real_route.append('d')

    #    for i in range(no_of_rows):
    #        print(score_matrix[i])

    index_s1 = len(sequence_1) - 1
    index_s2 = len(sequence_2) - 1
    for i in range(len(real_route)):
        if real_route[i] == 'u':
            output_s1 = '-' + output_s1
            output_s2 = sequence_2[index_s2] + output_s2
            index_s2 -= 1
        elif real_route[i] == 'l':
            output_s1 = sequence_1[index_s1] + output_s1
            output_s2 = '-' + output_s2
            index_s1 -= 1
        else:
            output_s1 = sequence_1[index_s1] + output_s1
            output_s2 = sequence_2[index_s2] + output_s2
            index_s1 -= 1
            index_s2 -= 1
    # output_s1 = output_s1[::-1]
    # output_s2 = output_s2[::-1]

    print('Now it\'s <Global Alignment>. Match score: <' + str(match_score) + '>, Mismatch score: <' +
          str(mismatch_score) + '>, Gap penalty: <' + str(gap_score) + '>.')
    print('--------')
    print('Optimal score is: ' + str(score_matrix[no_of_rows - 1][no_of_columns - 1]))
    print('--------')
    print(output_s1)
    print(output_s2)


def lo_al(match_score, mismatch_score, gap_score, sequence_1, sequence_2):
    no_of_columns = len(sequence_1) + 1
    no_of_rows = len(sequence_2) + 1
    route_all = []
    output_s1 = ''
    output_s2 = ''

    # note: i is a number, gap_score is a character.
    match_score = int(match_score)
    mismatch_score = int(mismatch_score)
    gap_score = int(gap_score)
    # the first parameter indicates columns, and the second indicates rows
    score_matrix = [[0] * no_of_columns for _ in range(no_of_rows)]
    # print(score_matrix)

    for i in range(no_of_columns):
        score_matrix[0][i] = 0
    for i in range(no_of_rows):
        score_matrix[i][0] = 0

    # i is row #, j is column #
    for i in range(no_of_rows):
        for j in range(no_of_columns):
            if i == 0 or j == 0:
                pass
            else:
                temp_up = score_matrix[i - 1][j] + gap_score
                temp_left = score_matrix[i][j - 1] + gap_score
                tmp = match_score if sequence_1[j - 1] == sequence_2[i - 1] else mismatch_score
                temp_diagonal = score_matrix[i - 1][j - 1] + tmp
                score_matrix[i][j] = max(0, temp_up, temp_left, temp_diagonal)
                # the following is to note down the route of assigning new values.
                if temp_up == score_matrix[i][j]:
                    route_all.append('u')
                elif temp_left == score_matrix[i][j]:
                    route_all.append('l')
                elif temp_diagonal == score_matrix[i][j]:
                    route_all.append('d')
                else:
                    route_all.append('0')
    '''
    # the following loop is to print the score matrix
    for i in range(no_of_rows):
        print(score_matrix[i])
    # the following loop is to print the route-all matrix
    for i in range(0, len(route_all), no_of_columns - 1):
        temp_str = ''
        for j in range(0, no_of_columns - 1):
            temp_str += str(route_all[j + i]) + ' '
        print(temp_str)
    '''
    maximum = max(map(max, score_matrix))
    max_location = []
    for i in range(no_of_rows):
        for j in range(no_of_columns):
            if score_matrix[i][j] == maximum:
                max_location.append((j, i))
    # j above indicates column#, i indicates row#, and both of them are indexes, not real #.

    no_of_columns -= 1
    no_of_rows -= 1
    for m in range(len(max_location)):
        j = max_location[m][0]
        k = max_location[m][1]
        while route_all[(k - 1) * no_of_columns + j-1] != str(0):
            output_s1 = sequence_1[j-1] + output_s1
            output_s2 = sequence_1[j-1] + output_s2
            j -= 1
            k -= 1
        output_s1 = '  |  ' + output_s1
        output_s2 = '  |  ' + output_s2
    output_s1 = output_s1[len('  |  '):]
    output_s2 = output_s2[len('  |  '):]
    print('Now it\'s <Local Alignment>. Match score: <' + str(match_score) + '>, Mismatch score: <' +
          str(mismatch_score) + '>, Gap penalty: <' + str(gap_score) + '>.')
    print('--------')
    print('Optimal score is: ' + str(maximum))
    print('--------')
    print('There are <' + str(len(max_location)) + '> optimal solutions as follows.')
    print(output_s1)
    print(output_s2)


# main program below
read_config(CONFIG_PATH)
print('--Program End Here--')
