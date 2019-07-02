def number_printer(n):
    new_n = [int(i) for i in str(n)]
    for nums in new_n:
        new_n[nums] += 1
    new_n = int(''.join(map(str, new_n)))
    return new_n

print(number_printer(998))
