import random

k = 4
k2 = k * k


def int2list(n: int):
    res = []
    for _ in range(k2):
        res.append(n % k2)
        n //= k2
    return res[::-1]


def list2int(l):
    res = 0
    for num in l:
        res *= k2
        res += num
    return res


def heuristic(state, goal) -> int:
    h = 0
    state_list = int2list(state)
    goal_list = int2list(goal)
    for i in range(1, k2):
        state_index = state_list.index(i)
        goal_index = goal_list.index(i)
        h += abs(state_index % k - goal_index % k)
        h += abs(state_index // k - goal_index // k)
    return h


def movement_generator(state):
    state_list = int2list(state)
    zero_index = state_list.index(0)
    if zero_index >= k:
        next_state = state_list[:]
        next_state[zero_index] = state_list[zero_index - k]
        next_state[zero_index - k] = 0
        yield list2int(next_state)
    if zero_index < k2 - k:
        next_state = state_list[:]
        next_state[zero_index] = state_list[zero_index + k]
        next_state[zero_index + k] = 0
        yield list2int(next_state)
    if zero_index % k > 0:
        next_state = state_list[:]
        next_state[zero_index] = state_list[zero_index - 1]
        next_state[zero_index - 1] = 0
        yield list2int(next_state)
    if zero_index % k < k - 1:
        next_state = state_list[:]
        next_state[zero_index] = state_list[zero_index + 1]
        next_state[zero_index + 1] = 0
        yield list2int(next_state)


def print_state(state):
    state_list = int2list(state)
    for i in range(0, k2, k):
        print(state_list[i:i+k])


def main():
    init_state = list2int(random.sample(range(k2), k2))
    print('init')
    print_state(init_state)
    print('-' * 10)
    goal_state = list2int(list(range(k2)))
    for max_f in range(100):
        print(max_f)
        h = heuristic(init_state, goal_state)
        stack = [(0, -1, init_state)]
        while stack:
            g, p, state = stack.pop()
            if state == goal_state:
                print('OK.', g)
                for (g, p, state) in stack:
                    if state < 0:
                        print('-' * 10)
                        print_state(~state)
                print('-' * 10)
                print_state(goal_state)
                break
            if state < 0:
                continue
            stack.append((g, p, ~state))
            for next_state in movement_generator(state):
                if next_state == p:
                    continue
                next_g = g + 1
                next_h = heuristic(next_state, goal_state)
                if next_g + next_h <= max_f:
                    stack.append((next_g, state, next_state))
        else:
            continue
        break
    else:
        print('NG')


if __name__ == '__main__':
    main()
