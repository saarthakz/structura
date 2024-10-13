def kadane(arr):

    max = -(10**9)
    flag = False
    for idx, elem in enumerate(arr):
        if elem > 0:
            flag = True
            break
        if elem > max:
            max = elem

    if not flag:
        return max

    max_sum = 0
    curr_sum = 0
    for idx, elem in enumerate(arr):
        curr_sum += arr[idx]
        if curr_sum < 0:
            curr_sum = 0
        if curr_sum > max_sum:
            max_sum = curr_sum
    return max_sum
