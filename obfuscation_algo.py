from byte_tables import BYTE_TABLE


# Two steps that are missing from bms script
def main(offset : int, size : int, name : str, data : bytearray):
    # First we get xor value by NOR'ing offset of the file in archive with 0 and and adding its size 
    xor_value = (-offset - 1) + size
    # Then we XOR 4 byte chuncks with this value and subtract 997 from the value for the next chunk
    for i in range(0, 32, 4):
        data[i:i+4]= (int(data[i:i+4][::-1].hex(), 16) ^ xor_value).to_bytes(8, byteorder='little', signed=True)[0:4]
        xor_value -= 997
    # Second we use chars in file name to get offsets and values where we XOR a single byte
    for char in name:
        char_value = ord(char)
        if (BYTE_TABLE[char_value] & 2) != 0:
            char_value -= 32
        offset = ((char_value << 3) - char_value) + 32
        if offset > size:
            # I don't know if this is inteded behaviour but seems to work fine
            continue
        xor_value = (-char_value - 1) & 255
        data[offset] = data[offset] ^ xor_value
    return data


if __name__ == '__main__':
    main()
