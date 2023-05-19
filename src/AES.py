# This is the file that encrypts messages into AES
import binascii
from collections import deque
import numpy as x

s_box_vertical = {
    '0': [0x63, 0xca, 0xb7, 0x04, 0x09, 0x53, 0xd0, 0x51, 0xcd, 0x60, 0xe0, 0xe7, 0xba, 0x70, 0xe1, 0x8c],
    '1': [0x7c, 0x82, 0xfd, 0xc7, 0x83, 0xd1, 0xef, 0xa3, 0x0c, 0x81, 0x32, 0xc8, 0x78, 0x3e, 0xf8, 0xa1],
    '2': [0x77, 0xc9, 0x93, 0x23, 0x2c, 0x00, 0xaa, 0x40, 0x13, 0x4f, 0x3a, 0x37, 0x25, 0xb5, 0x98, 0x89],
    '3': [0x7b, 0x7d, 0x26, 0xc3, 0x1a, 0xed, 0xfb, 0x8f, 0xec, 0xdc, 0x0a, 0x6d, 0x2e, 0x66, 0x11, 0x0d],
    '4': [0xf2, 0xfa, 0x36, 0x18, 0x1b, 0x20, 0x43, 0x92, 0x5f, 0x22, 0x49, 0x8d, 0x1c, 0x48, 0x69, 0xbf],
    '5': [0x6b, 0x59, 0x3f, 0x96, 0x6e, 0xfc, 0x4d, 0x9d, 0x97, 0x2a, 0x06, 0xd5, 0xa6, 0x03, 0xd9, 0xe6],
    '6': [0x6f, 0x47, 0xf7, 0x05, 0x5a, 0xb1, 0x33, 0x38, 0x44, 0x90, 0x24, 0x4e, 0xb4, 0xf6, 0x8e, 0x42],
    '7': [0xc5, 0xf0, 0xCC, 0x9a, 0xa0, 0x5b, 0x85, 0xf5, 0x17, 0x88, 0x5c, 0xa9, 0xc6, 0x0e, 0x94, 0x68],
    '8': [0x30, 0xad, 0x34, 0x07, 0x52, 0x6a, 0x45, 0xbc, 0xc4, 0x46, 0xc2, 0x6c, 0xe8, 0x61, 0x9b, 0x41],
    '9': [0x01, 0xd4, 0xa5, 0x12, 0x3b, 0xcb, 0x19, 0xb6, 0xa7, 0xee, 0xd3, 0x56, 0xdd, 0x35, 0x1e, 0x99],
    'a': [0x67, 0xa2, 0xe5, 0x80, 0xd6, 0xbe, 0x02, 0xda, 0x7e, 0xb8, 0xac, 0xf4, 0x74, 0x57, 0x87, 0x2d],
    'b': [0x2b, 0xaf, 0xf1, 0xe2, 0xb3, 0x39, 0x7f, 0x21, 0x3d, 0x14, 0x62, 0xea, 0x1f, 0xb9, 0xe9, 0x0f],
    'c': [0xfe, 0x9c, 0x71, 0xeb, 0x29, 0x4a, 0x50, 0x10, 0x64, 0xde, 0x91, 0x65, 0x4b, 0x86, 0xce, 0xb0],
    'd': [0xd7, 0xa4, 0x89, 0x27, 0xe3, 0x4c, 0x3c, 0xff, 0x5d, 0x5e, 0x95, 0x7a, 0xbd, 0xc1, 0x55, 0x54],
    'e': [0xab, 0x72, 0x31, 0xb2, 0x2f, 0x58, 0x9f, 0xf3, 0x19, 0x0b, 0xe4, 0xae, 0x8b, 0x1d, 0x28, 0xbb],
    'f': [0x76, 0xC0, 0x15, 0x75, 0x84, 0xcf, 0xa8, 0xd2, 0x73, 0xdb, 0x79, 0x08, 0x8a, 0x9e, 0xdf, 0x16]
}

s_box_horizontal = {
    '0': [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    '1': [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    '2': [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    '3': [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    '4': [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    '5': [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    '6': [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    '7': [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    '8': [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    '9': [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    'a': [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    'b': [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    'c': [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    'd': [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    'e': [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    'f': [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
}


# divides the message up into 16 byte blocks
def data_divider(message):
    chunks = []

    while message:
        if len(message) < 16:
            n = len(message)
        else:
            n = 16

        chunks.append(message[0:n])

        if len(message) > 0:
            message = message[n:]
        else:
            message = None

    return chunks


# translates a single block into hexadecimal
def hex_translate(chunk):
    i = 0
    ord_chunk = []
    hex_chunk = []

    for i in range(len(chunk)):
        ord_chunk.append(ord(chunk[i]))
        i += 1

    i = 0

    for i in range(len(ord_chunk)):
        hex_chunk.append(hex(ord_chunk[i]))
        i += 1

    return hex_chunk


# converts all blocks to hexadecimal
def full_translate(chunks):
    i = 0

    for i in range(len(chunks)):
        chunks[i] = hex_translate(chunks[i])
        i += 1

    return chunks


# creates a dictionary with each column of the block
def make_columns(chunks):
    columns = {
        1: [],
        2: [],
        3: [],
        4: []
    }

    # adds 4 at a time unless there isn't 4 left
    if len(chunks) > 4:
        columns[1] = chunks[:4]
    else:
        columns[1] = chunks[0:]

    if len(chunks) > 8:
        columns[2] = chunks[4:8]
    else:
        columns[2] = chunks[4:]

    if len(chunks) > 12:
        columns[3] = chunks[8:12]
    else:
        columns[3] = chunks[8:]

    if len(chunks) >= 16:
        columns[4] = chunks[12:16]
    else:
        columns[4] = chunks[12:]

    return columns


def make_key(keyword):
    if len(keyword) == 16:
        keyword = data_divider(keyword)
        keyword = full_translate(keyword)
    else:
        raise Exception("Keyword must be 16 characters")
    return keyword


def add_round_key(key, chunk):
    key_sum = []
    i = 0
    for i in range(len(key)):
        key_sum.append(hex(int(key[i], 16) ^ int(chunk[i], 16)))
    return key_sum


def key_sum_format(key_sum):
    i = 0
    for i in range(len(key_sum)):
        if len(key_sum[i]) < 4:
            start = key_sum[i][:2]
            end = key_sum[i][2:]
            key_sum[i] = start + '0' + end
    return key_sum


def sub_bytes(formatted_key_sum):
    i = 0
    for i in range(len(formatted_key_sum)):
        sub_hex = formatted_key_sum[i].split("x")
        sub_hex = sub_hex[1]

        horizontal_array = s_box_horizontal[sub_hex[1]]
        vertical_array = s_box_vertical[sub_hex[0]]

        sub_hex = set(horizontal_array) & set(vertical_array)
        formatted_key_sum[i] = hex(sub_hex.pop())

    return formatted_key_sum


def shift_rows(columns):
    column2 = deque(columns[2])
    column3 = deque(columns[3])
    column4 = deque(columns[4])

    column2.rotate(-1)
    column3.rotate(-2)
    column4.rotate(-3)

    columns[2] = list(column2)
    columns[3] = list(column3)
    columns[4] = list(column4)

    return columns


def mix_columns(columns):
    i = 1

    while i <= 4:
        columns[i] = to_int(columns[i])

        a = columns[i][0]
        b = columns[i][1]
        c = columns[i][2]
        d = columns[i][3]

        # code used from https://stackoverflow.com/questions/66115739/aes-mixcolumns-with-python

        columns[i][0] = gmul(a, 2) ^ gmul(b, 3) ^ gmul(c, 1) ^ gmul(d, 1)

        columns[i][1] = gmul(a, 1) ^ gmul(b, 2) ^ gmul(c, 3) ^ gmul(d, 1)

        columns[i][2] = gmul(a, 1) ^ gmul(b, 1) ^ gmul(c, 2) ^ gmul(d, 3)

        columns[i][3] = gmul(a, 3) ^ gmul(b, 1) ^ gmul(c, 1) ^ gmul(d, 2)

        columns[i] = to_hex(columns[i])

        i += 1

    return columns


def to_int(arr):
    for i in range(len(arr)):
        arr[i] = int(arr[i], 16)

    return arr


def to_hex(arr):
    i = 0
    for i in range(len(arr)):
        arr[i] = hex(arr[i])

    return arr


def gmul(a, b):
    # code used from https://stackoverflow.com/questions/66115739/aes-mixcolumns-with-python
    if b == 1:
        return a
    tmp = (a << 1) & 0xff
    if b == 2:
        return tmp if a < 128 else tmp ^ 0x1b
    if b == 3:
        return gmul(a, 2) ^ a


def make_round(cipher, round):
    w0 = cipher[:4]
    w1 = cipher[4:8]
    w2 = cipher[8:12]
    w3 = cipher[12:]

    w3 = rot_word(w3)
    w3 = sub_bytes(w3)
    w3 = rcon(w3, round)

    w4 = xor(w0, w3)
    w5 = xor(w1, w4)
    w6 = xor(w2, w5)
    w7 = xor(w3, w6)

    return w4, w5, w6, w7


def rot_word(word):
    word = deque(word)
    word.rotate(-1)
    word = list(word)

    return word


def rcon(word, round):
    rc = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    word[0] = int(word[0], 16)

    word[0] = rc[round] ^ word[0]
    word[0] = hex(word[0])

    return word


def xor(list1, list2):
    output = []
    i = 0
    while i < len(list1):
        sums = int(list1[i], 16) ^ int(list2[i], 16)
        output.append(hex(sums))
        i += 1

    return output
