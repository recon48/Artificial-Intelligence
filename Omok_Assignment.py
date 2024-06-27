import math
import time


def print_board(board):
    print(" ", end=" ")
    for i in range(len(board)):
        print(chr(ord('a') + i), end=" ")
    print()
    for i in range(len(board)):
        print(i + 1, end="")
        if i < 9:
            print(end=" ")
        for j in range(len(board[i])):
            print(board[i][j], end=" ")
        print()


def place_stone(board, row, col, stone):
    if board[row][col] == ' ':
        board[row][col] = stone
        return True
    else:
        print("이미 둔 자리입니다!")
        return False


def check_winner(board, stone):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == stone:
                for d in directions:
                    count = 1
                    for i in range(1, 5):
                        if 0 <= row + d[0] * i < len(board) and 0 <= col + d[1] * i < len(board[row]):
                            if board[row + d[0] * i][col + d[1] * i] == stone:
                                count += 1
                            else:
                                break
                        else:
                            break
                    if count >= 5:
                        return True
    return False


def possible_moves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                if has_adjacent_stone(board, i, j):
                    moves.append((i, j))

    return moves


def has_adjacent_stone(board, row, col):
    stone = board[row][col]

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            r = row + dr
            c = col + dc
            if 0 <= r < len(board) and 0 <= c < len(board[r]) and (board[r][c] == 'O' or board[r][c] == 'X'):
                return True
    return False


def omok_game(size=19):

    board = [[' ' for _ in range(size)] for _ in range(size)]
    if user_turn == 1:
        while True:
            stone = 'X'
            print_board(board)
            print(f"{stone}의 차례입니다")
            start_time = time.time()
            move = input("착수할 곳을 입력해주세요(e.g., 'a3'): ")

            if time.time() - start_time > time_limit:
                print("시간 초과로 패배했습니다.")
                break
            if len(move) >= 2 and move[0].isalpha() and move[1:].isdigit():
                alpha = move[0]
                digit = move[1:]
                col = ord(alpha) - ord('a')
                row = int(digit) - 1
                if 0 <= row < size and 0 <= col < size:
                    if place_stone(board, row, col, stone):
                        if check_winner(board, stone):
                            print_board(board)
                            print(f"경기 종료. {stone}가 승리했습니다.")
                            break
                        stone = 'O'
                        ai_time = time.time()
                        depth = 1
                        i, j = 0, 0
                        while True:
                            _, i, j = alpha_beta(board, stone, depth, -math.inf, math.inf, True, ai_time)
                            if time.time() - ai_time > time_limit - 1:
                                break
                            depth += 1

                        if place_stone(board, i, j, stone):
                            if check_winner(board, stone):
                                print_board(board)
                                print(f"경기 종료. {stone}가 승리했습니다.")
                                break
                else:
                    print("바둑판 범위 밖입니다.")
            else:
                print("착수할 곳의 입력값이 올바르지 않습니다.")

    else:
        first = 1
        while True:
            stone = 'X'
            ai_time = time.time()
            depth = 1
            i, j = 0, 0
            if first == 1:
                i, j = 9, 9
                first = 2
            else:
                while True:
                    _, i, j = alpha_beta(board, stone, 2, -math.inf, math.inf, True, ai_time)  # AI의 수를 계산
                    if time.time() - ai_time > time_limit - 1:
                        break
                    depth += 1

            if place_stone(board, i, j, stone):
                if check_winner(board, stone):
                    print_board(board)
                    print(f"경기 종료. {stone}가 승리했습니다.")
                    break
            stone = 'O'
            print_board(board)
            print(f"{stone}의 차례입니다")
            start_time = time.time()
            move = input("착수할 곳을 입력해주세요(e.g., 'a3'): ")
            if time.time() - start_time > time_limit:
                print("시간 초과로 패배했습니다.")
                break

            if len(move) >= 2 and move[0].isalpha() and move[1:].isdigit():
                alpha = move[0]
                digit = move[1:]
                col = ord(alpha) - ord('a')
                row = int(digit) - 1
                if 0 <= row < size and 0 <= col < size:
                    if place_stone(board, row, col, stone):
                        if check_winner(board, stone):
                            print_board(board)
                            print(f"경기 종료. {stone}가 승리했습니다.")
                            break
                else:
                    print("바둑판 범위 밖입니다.")
            else:
                print("착수할 곳의 입력값이 올바르지 않습니다.")


def alpha_beta(board, turn, depth, alpha, beta, maximizing_player, ai_time):
    if time.time() - ai_time > time_limit - 1:
        return heuristic(board, 'X'), None, None

    if depth == 0 or check_winner(board, 'X') or check_winner(board, 'O'):
        return heuristic(board, turn), None, None
    anti_turn= 'O' if turn == 'X' else 'X'
    best_row = None
    best_col = None

    if maximizing_player:
        value = -math.inf
        for move in possible_moves(board):
            place_stone(board, move[0], move[1], turn)
            child_value, _, _ = alpha_beta(board, anti_turn, depth - 1, alpha, beta, False, ai_time)
            board[move[0]][move[1]] = ' '
            if child_value > value:
                value = child_value
                best_row = move[0]
                best_col = move[1]
            alpha = max(alpha, child_value)
            if alpha >= beta:
                break
        return value, best_row, best_col
    else:
        value = math.inf
        for move in possible_moves(board):
            place_stone(board, move[0], move[1], turn)
            child_value, _, _ = alpha_beta(board, anti_turn, depth - 1, alpha, beta, True, ai_time)
            board[move[0]][move[1]] = ' '
            if child_value < value:
                value = child_value
                best_row = move[0]
                best_col = move[1]
            beta = min(beta, child_value)
            if beta <= alpha:
                break
        return value, best_row, best_col


def heuristic(board, turn):
    if user_turn == 1:

        my_stone = 'O'
        opponent_stone = 'X'
        my_score = measure(board, my_stone)
        op_score = measure(board, opponent_stone)

        return my_score - op_score
    else:
        my_stone='X'
        opponent_stone='O'
        my_score = measure(board, my_stone)
        op_score = measure(board, opponent_stone)

        return my_score - op_score


def measure(board, stone):
    op = 'O' if stone == 'X' else 'X'
    my = stone
    result=[]
    for i in range(len(board)):
        for j in range(len(board)):

            if j <= len(board[i]) - 4:
                score=0
                count = 0
                while j + count < len(board[i]) and board[i][j + count] == my:
                    count += 1
                if count >= 1:
                    score += count ** 3
                    left_block = 0
                    right_block = 0

                    if j > 0 and board[i][j - 1] == op:
                        left_block += 1
                    if j + count < len(board[i]) and board[i][j + count] == op:
                        right_block += 1
                    if left_block == 1 and right_block == 1:
                        score *= 0
                    elif left_block == 1 or right_block == 1:

                        score *= 1
                    else:

                        score *= 2
                    result.append(score)

            if i <= len(board) - 4:
                score = 0
                count = 0
                while i + count < len(board) and board[i + count][j] == my:
                    count += 1
                if count >= 1:
                    score += count ** 3
                    up_block = 0
                    down_block = 0
                    if i > 0 and board[i - 1][j] == op:
                        up_block += 1
                    if i + count < len(board) and board[i + count][j] == op:
                        down_block += 1
                    if up_block == 1 and down_block == 1:
                        score *= 0
                    elif up_block == 1 or down_block == 1:

                        score *= 1
                    else:

                        score *= 2
                    result.append(score)

            if i <= len(board) - 4 and j <= len(board[i]) - 4:
                score = 0
                count = 0
                while i + count < len(board) and j + count < len(board[i]) and board[i + count][
                    j + count] == my:
                    count += 1
                if count >= 1:
                    score += count ** 3
                    left_up_block = 0
                    right_down_block = 0
                    if i > 0 and j > 0 and board[i - 1][j - 1] == op:
                        left_up_block += 1
                    if i + count < len(board) and j + count < len(board[i]) and board[i + count][
                        j + count] == op:
                        right_down_block += 1
                    if left_up_block == 1 and right_down_block == 1:
                        score *= 0
                    elif left_up_block == 1 or right_down_block == 1:

                        score *= 1
                    else:

                        score *= 2
                    result.append(score)

            if i <= len(board) - 4 and j >= 3:
                score = 0
                count = 0
                while i + count < len(board) and j - count >= 0 and board[i + count][j - count] == my:
                    count += 1
                if count >= 1:
                    score += count ** 3
                    right_up_block = 0
                    left_down_block = 0
                    if i > 0 and j < len(board[i]) - 1 and board[i - 1][j + 1] == op:
                        right_up_block += 1
                    if i + count < len(board) and j - count >= 0 and board[i + count][j - count] == op:
                        left_down_block += 1
                    if right_up_block == 1 and left_down_block == 1:
                        score *= 0
                    elif right_up_block == 1 or left_down_block == 1:

                        score *= 1
                    else:
                        score *= 2
                    result.append(score)

    return max(result)


time_limit = int(input("착수 제한 시간을 입력해주세요(초)"))
user_turn = int(input("선공과 후공을 선택해주세요.\n 1. 선공 2. 후공"))
omok_game()

