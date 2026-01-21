import sys
import os
from byte_tables import CRC_TABLE
import obfuscation_algo


# This is more or less a copy of a bms script from this disscussion https://zenhax.com/viewtopic.php@t=673.html rewritten in python as I couldn't figure out how to write de-obfuscation algorithm that the game uses in the bms language.
# How to use: Just drop .BIN files you get from your copy of elminage. Seems to work with Elminage for PS2 and Elminage 2 for PSP.
def main():
    for arg in sys.argv[1:]:
        try:
            infile = open(arg, 'rb')
        except:
            print("Failed to open " + arg)
            continue
        if infile.read(4) != b'Mps2':
            print("Not Mps2.")
            continue
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
                path = "extracted/" + os.path.basename(arg).rsplit('.', 1)[0] + "/" + file_name
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'wb') as outfile:
                    infile.seek(offset)
                    outfile.write(obfuscation_algo.main(offset, size, file_name, bytearray(infile.read(size))))
        infile.close()        
    input("Press Enter to close.")
    sys.exit()


if __name__ == '__main__':
    main()
