from typing import List


def most_common_bit(numbers: List[str], index: int) -> str:
    bits = [number[index] for number in numbers]
    number_of_zeros = len(list(filter(lambda x: x == '0', bits)))
    number_of_ones = len(list(filter(lambda x: x == '1', bits)))
    if number_of_zeros > number_of_ones:
        return '0'
    else:
        return '1'


def least_common_bit(numbers: List[str], index: int) -> str:
    most_common = most_common_bit(numbers, index)
    if most_common == '0':
        return '1'
    else:
        return '0'


def gamma(numbers: List[str]) -> int:
    bit_length = len(numbers[0])
    gamma = ''
    for i in range(0, bit_length):
        gamma += most_common_bit(numbers, i)
    return int(gamma, 2)


def epsilon(numbers: List[str]) -> int:
    bit_length = len(numbers[0])
    epsilon = ''
    for i in range(0, bit_length):
        epsilon += least_common_bit(numbers, i)
    return int(epsilon, 2)


def oxygen(numbers: List[str]) -> int:
    bit_length = len(numbers[0])
    for i in range(0, bit_length):
        bit_criterion = most_common_bit(numbers, i)
        numbers = list(filter(lambda x: x[i] == bit_criterion, numbers))
        if len(numbers) == 1:
            break
    return int(numbers[0], 2)


def co2(numbers: List[str]) -> int:
    bit_length = len(numbers[0])
    for i in range(0, bit_length):
        bit_criterion = least_common_bit(numbers, i)
        numbers = list(filter(lambda x: x[i] == bit_criterion, numbers))
        if len(numbers) == 1:
            break
    return int(numbers[0], 2)


numbers = [number.strip() for number in open('3.in', 'r').readlines()]

print(gamma(numbers) * epsilon(numbers))
print(oxygen(numbers) * co2(numbers))
