from ByteTables import BYTE_TABLE


# Two steps that are missing from bms script
# First step: to get xor value we NOR offset of the file within archive with 0 and add files size
# Then we XOR 4 byte chunks in a loop with this value and subtract 997 from the value for the next chunk
# Second step: we use chars in file name to get offsets and values where we XOR a single byte
# Hopefully second step is self explanatory as I can't describe it in words
# Aslo I don't know if continuing if offset is larger the size is intended but it works
def obfuscation_algo(offset : int, size : int, name : bytearray, data : bytearray):
    xor_value = (-offset - 1) + size
    for i in range(0, 32, 4):
        data[i:i + 4]= (int(data[i:i + 4][::-1].hex(), 16) ^ xor_value).to_bytes(8, byteorder='little', signed=True)[0:4]
        xor_value -= 997
    for char in name:
        char_value = char
        if (BYTE_TABLE[char_value] & 2) != 0:
            char_value -= 32
        offset = ((char_value << 3) - char_value) + 32
        if offset > size:  
            continue
        xor_value = (-char_value - 1) & 255
        data[offset] = data[offset] ^ xor_value
    return data


