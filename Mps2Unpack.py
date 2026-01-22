import sys
import os
from ByteTables import CRC_TABLE
from Obfuscation import obfuscation_algo


# This is more or less a copy of a bms script from this disscussion https://zenhax.com/viewtopic.php@t=673.html
# Rewritten in python as I couldn't figure out how to write de-obfuscation algorithm that the game uses in the bms language
# If you know how to write obfuscation algorithm in bms scripts language please let me know! I would like to see it.
# Tested with Elminage for PS2 and Elminage 2 for PSP both unpack correctly so it might work for the rest
# How to use: just drop .BIN files you get from your copy of elminage on the py script
def unpack(path):
    try:
        infile = open(path, 'rb')
    except:
        return os.path.abspath(path) + " failed to open."
    if infile.read(4) != b'Mps2':
        infile.close()
        return os.path.abspath(path) + " not Mps2."
    else:
        file_num = int(infile.read(4)[::-1].hex(), 16)
        infile.read(16)
        infile_pointer = infile.tell()
        for i in range(file_num):
            infile.seek(infile_pointer)
            xor_value = ""
            for j in range(4):
                xor_value = ("%X" % CRC_TABLE[(infile_pointer % 1024)]).zfill(2) + xor_value
                infile_pointer += 1
            offset = int(infile.read(4)[::-1].hex(), 16) ^ int(xor_value, 16)
            xor_value = ""
            for j in range(4):
                xor_value = ("%X" % CRC_TABLE[(infile_pointer % 1024)]).zfill(2) + xor_value
                infile_pointer += 1
            size = int(infile.read(4)[::-1].hex(), 16) ^ int(xor_value, 16)
            file_name = bytearray()
            for j in range(0, 16, 4):
                xor_value = ""
                for k in range(4):
                    xor_value = ("%X" % CRC_TABLE[(infile_pointer % 1024)]).zfill(2) + xor_value
                    infile_pointer += 1
                file_name += (int(infile.read(4)[::-1].hex(), 16) ^ int(xor_value, 16)).to_bytes(8, byteorder='little', signed=True)[0:4]
            file_name = file_name.decode().rstrip("\x00")
            outpath = "extracted/" + os.path.basename(path).rsplit('.', 1)[0] + "/" + file_name
            os.makedirs(os.path.dirname(outpath), exist_ok=True)
            with open(outpath, 'wb') as outfile:
                infile.seek(offset)
                outfile.write(obfuscation_algo(offset, size, file_name, bytearray(infile.read(size))))
        infile.close()
        return os.path.abspath(path) + " done."

        
def main():
    for arg in sys.argv[1:]:
        print(unpack(arg))             
    input("Press Enter to close.")
    sys.exit()


if __name__ == '__main__':
    main()
