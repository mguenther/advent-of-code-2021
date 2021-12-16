from typing import Any, List


mapping = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

operators = {
    0: 'sum',
    1: 'product',
    2: 'min',
    3: 'max',
    5: 'gt',
    6: 'lt',
    7: 'eq'
}


def read(filename: str = '16.in') -> str:
    return open(filename, 'r').readline().strip()


def as_binary(hexadecimal: str) -> str:
    return ''.join([mapping[h] for h in hexadecimal])


def parse_header(binary: str) -> tuple[int, int, int]:
    version = int(binary[0:3], 2)
    type = int(binary[3:6], 2)
    return version, type, 6


def parse_literal(binary: str) -> tuple[str, int]:
    segments = []
    i = 0
    while len(binary[i:]) >= 5:
        segment = binary[i:i+5]
        if segment.startswith('0'):
            segments.append(segment[1:])
            i += 5
            break
        else:
            segments.append(segment[1:])
            i += 5
    value = int(''.join(segments), 2)
    return value, i


def parse_operator(binary: str) -> tuple[List[tuple[str, int, Any]], int]:
    length_type = int(binary[0], 2)
    if length_type == 0:
        length = int(binary[1:16], 2)
        data = binary[16:16+length]
        packets, bits_parsed = parse(data)
        return packets, 1 + 15 + bits_parsed
    else:
        number_of_packets = int(binary[1:1+11], 2)
        data = binary[12:]
        packets, bits_parsed = parse(data, number_of_packets)
        return packets, 1 + 11 + bits_parsed


def parse(binary: str, max_number_of_packets: int = None) -> tuple[List[tuple[str, int, Any]], int]:
    packets = []
    i = 0
    while binary[i:] != '':
        if len(packets) == max_number_of_packets: break
        if int(binary[i:], 2) == 0: break
        version, type, bits_parsed = parse_header(binary[i:])
        i += bits_parsed
        data = binary[i:]
        if type == 4:
            value, bits_parsed = parse_literal(data)
            packets.append(('literal', version, value))
            i += bits_parsed
        else:
            value, bits_parsed = parse_operator(data)
            packets.append((operators[type], version, value))
            i += bits_parsed
    return packets, i


def sum_of_versions(packets: List[tuple[str, int, Any]]) -> int:
    s = 0
    for packet in packets:
        type, version, data = packet
        if type == 'literal':
            s += version
        else:
            s += version + sum_of_versions(data)
    return s


def eval(packets: List[tuple[str, int, Any]]) -> List[int]:
    res = []
    for packet in packets:
        type, _, data = packet
        if type == 'literal':
            res.append(data)
        else:
            values = eval(data)
            if type == 'max':
                res.append(max(values))
            elif type == 'min':
                res.append(min(values))
            elif type == 'sum':
                res.append(sum(values))
            elif type == 'product':
                p = 1
                for v in values:
                    p *= v
                res.append(p)
            elif type == 'gt':
                l, r = values
                if l > r: res.append(1)
                else: res.append(0)
            elif type == 'lt':
                l, r = values
                if l < r: res.append(1)
                else: res.append(0)
            elif type == 'eq':
                l, r = values
                if l == r: res.append(1)
                else: res.append(0)
    return res


packets, _ = parse(as_binary(read('16.in')))

print(sum_of_versions(packets))
print(eval(packets)[0])