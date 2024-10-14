def can_sum(target_sum, numbers):
    if target_sum == 0:
        return True
    if target_sum < 0 or not numbers:
        return False
    peek = numbers[-1]
    f1 = can_sum(target_sum - peek, numbers)
    if f1:
        return True
    return can_sum(target_sum, numbers[:-1])
