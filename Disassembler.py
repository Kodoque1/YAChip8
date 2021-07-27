import argparse
import struct
import functools


def nibble_split(word):
    n0 = word & 0xf
    n1 = (word & 0xf0) >> 4
    n2 = (word & 0xf00) >> 8
    n3 = (word & 0xf000) >> 12
    return n3, n2, n1, n0


def nibble_split_byte(byte1, byte0):
    n0 = byte0 & 0xf
    n1 = (byte0 & 0xf0) >> 4
    n2 = byte1 & 0xf
    n3 = (byte1 & 0xf0) >> 4
    return n3, n2, n1, n0


def decode_nnn(word):
    return hex(word & 0xFFF)


def decode_xy(word):
    return "V" + hex((word & 0xF00) >> 8)[2:] + ", " + "V" + hex((word & 0xF0) >> 4)[2:]


def decode_xkk(word):
    return "V" + hex((word & 0xF00) >> 8)[2:] + ", " + hex(word & 0xFF)


def decode_xyn(word):
    return "V" + hex((word & 0xF00) >> 8)[2:] + ", V" + hex((word & 0xF0) >> 4)[2:] + ", " + hex(word & 0xF)


def decode_x(word):
    return "V" + hex((word & 0xF00) >> 8)[2:]


class OpcodeDict(dict):
    def __getitem__(self, key):
        if super().__contains__(key):
            return super().__getitem__(key)

        # print(key)

        for k in self.keys():
            comparisons = [e == k[idx] or k[idx] == 0x10 for (idx, e) in enumerate(key)]
            matched = functools.reduce(lambda a, b: a and b, comparisons)
            if matched:
                return super().__getitem__(k)


OpcodeMap = OpcodeDict({
    (0x0, 0x0, 0xE, 0x0): ("cls", None),
    (0x0, 0x0, 0xE, 0xE): ("ret", None),
    (0x0, 0x10, 0x10, 0x10): ("sys", decode_nnn),
    (0x1, 0x10, 0x10, 0x10): ("jp", decode_nnn),
    (0x0, 0x10, 0x10, 0x10): ("sys", decode_nnn),
    (0x2, 0x10, 0x10, 0x10): ("call", decode_nnn),
    (0x3, 0x10, 0x10, 0x10): ("se", decode_xkk),
    (0x4, 0x10, 0x10, 0x10): ("sne", decode_xkk),
    (0x5, 0x10, 0x10, 0x0): ("se_1", decode_xy),
    (0x6, 0x10, 0x10, 0x10): ("ld", decode_xkk),
    (0x7, 0x10, 0x10, 0x10): ("add", decode_xkk),
    (0x8, 0x10, 0x10, 0x0): ("ld_1", decode_xy),
    (0x8, 0x10, 0x10, 0x1): ("or_", decode_xy),
    (0x8, 0x10, 0x10, 0x2): ("and_", decode_xy),
    (0x8, 0x10, 0x10, 0x3): ("xor", decode_xy),
    (0x8, 0x10, 0x10, 0x4): ("add_1", decode_xy),
    (0x8, 0x10, 0x10, 0x5): ("sub", decode_xy),
    (0x8, 0x10, 0x10, 0x6): ("shr", decode_xy),
    (0x8, 0x10, 0x10, 0x7): ("subn", decode_xy),
    (0x8, 0x10, 0x10, 0xE): ("shl", decode_xy),
    (0x9, 0x10, 0x10, 0x0): ("sne_1", decode_xy),
    (0xA, 0x10, 0x10, 0x10): ("ld_i", decode_nnn),
    (0xB, 0x10, 0x10, 0x10): ("jp_v0", decode_nnn),
    (0xC, 0x10, 0x10, 0x10): ("rnd", decode_xkk),
    (0xD, 0x10, 0x10, 0x10): ("drw", decode_xyn),
    (0xE, 0x10, 0x9, 0xE): ("skp", decode_x),
    (0xE, 0x10, 0xA, 0x1): ("sknp", decode_x),
    (0xF, 0x10, 0x0, 0x7): ("ld_timer", decode_x),
    (0xF, 0x10, 0x0, 0xA): ("ld_keypress", decode_x),
    (0xF, 0x10, 0x1, 0x5): ("ld_settimer", decode_x),
    (0xF, 0x10, 0x1, 0x8): ("ld_setsoundtimer", decode_x),
    (0xF, 0x10, 0x1, 0xE): ("add_i", decode_x),
    (0xF, 0x10, 0x2, 0x9): ("ld_sprite", decode_x),
    (0xF, 0x10, 0x3, 0x3): ("ld_bcd", decode_x),
    (0xF, 0x10, 0x5, 0x5): ("ld_dumpregs", decode_x),
    (0xF, 0x10, 0x6, 0x5): ("ld_loadregs", decode_x),
})


def main():
    parser = argparse.ArgumentParser(description='Chip 8 Emulator.')
    parser.add_argument('rom', type=str, help='Path to the rom')
    args = parser.parse_args()

    with open(args.rom, "rb") as f:
        line_number = 0x200
        while byte := f.read(2):
            rom_word = struct.unpack('>H', byte)[0]
            decoding = OpcodeMap[nibble_split(rom_word)]
            if decoding:
                opcode, decoder = decoding
                if decoder:
                    print(hex(line_number) + ": " + opcode + " " + decoder(rom_word))
                else:
                    print(hex(line_number) + ": " + opcode)
            else:
                print(hex(line_number) + ": " + hex(rom_word) + " unrecognized instruction")
            line_number += 2


if __name__ == '__main__':
    main()
