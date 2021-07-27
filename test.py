import unittest
from InstructionDecoder import *
import Mem
import Cpu
import Screen
import main
import pygame
from pygame import *
import sys
from Assembler import assemble_byte
import keyboard
import random
import tempfile



class CpuTest(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.outfile = open(tempfile.mkstemp()[1])
        self.cpu = Cpu.Cpu(Mem.Mem(), self.outfile, Screen.Screen(64, 32), None)

    def tearDown(self):
        self.outfile.close()

    def test_cls(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xE0
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        for i in range(64):
            for j in range(32):
                self.assertEqual(self.cpu.scr.get_pixel(i, j), 0)

    def test_ret(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xEE
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.mem.push(0x250)
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, 0x250)

    def test_jp(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x1F
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, 0xFFF)

    def test_call(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x2F
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        # we want to land at the next instruction after call
        self.assertEqual(self.cpu.mem.pop(), self.cpu.mem.PROG_START + 2)
        self.assertEqual(self.cpu.mem.PC, 0xFFF)

    def test_se(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x30
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 4)

    def test_sne(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x40
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 2)

    def test_se_1(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.V[1] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x50
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x10
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 4)

    def test_ld(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x60
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 0xFF)

    def test_add(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x70
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 1)
        self.assertEqual(self.cpu.mem.V[0], 0xFE)

    def test_ld_1(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x81
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x00
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[1], 0xFF)

    def test_or(self):
        self.cpu.mem.V[0] = 0xF0
        self.cpu.mem.V[1] = 0x0F
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x11
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 0xFF)

    def test_and(self):
        self.cpu.mem.V[0] = 0xF0
        self.cpu.mem.V[1] = 0x0F
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x12
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 0x00)

    def test_xor(self):
        self.cpu.mem.V[0] = 0xF0
        self.cpu.mem.V[1] = 0x0F
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x13
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 0xFF)

    def test_add_1(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.V[1] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x14
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 0x1)
        self.assertEqual(self.cpu.mem.V[0], 0xFE)

    def test_sub(self):
        self.cpu.mem.V[0] = 0x00
        self.cpu.mem.V[1] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x15
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 0x1)
        self.assertEqual(self.cpu.mem.V[0], 0x1)

    def test_shr(self):
        self.cpu.mem.V[0] = 0x11
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x16
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 0x1)
        self.assertEqual(self.cpu.mem.V[0], 0x8)

    def test_subn(self):
        self.cpu.mem.V[0] = 0x00
        self.cpu.mem.V[1] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x81
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x07
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 0x1)
        self.assertEqual(self.cpu.mem.V[1], 0x1)

    def test_shl(self):
        self.cpu.mem.V[0] = 0xC0
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x80
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x1E
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[15], 0x1)
        self.assertEqual(self.cpu.mem.V[0], 0x80)

    def test_sne_1(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.V[1] = 0xFF
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0x90
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x10
        self.cpu.mem.PC = self.cpu.mem.PROG_START
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 2)

    def test_ld_i(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xAF
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.I, 0xFFF)

    def test_jp_v0(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xB0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.mem.V[0] = 0x50
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, 0x0FF + 0x50)

    def test_rnd(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xC0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xFF
        self.cpu.execute()
        self.assertLessEqual(self.cpu.mem.V[0], 0xFF)
        self.assertGreaterEqual(self.cpu.mem.V[0], 0)

    def test_drw(self):
        self.cpu.mem.V[0] = 10
        self.cpu.mem.V[1] = 10
        self.cpu.mem.I = self.cpu.mem.HEXFONT
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xD0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x15
        self.cpu.execute()

        zero_font = [0xF0, 0x90, 0x90, 0x90, 0xF0]

        for y in range(5):
            for decal in range(8):
                target_c = (zero_font[y] >> (7 - decal)) & 1
                extract = self.cpu.scr.get_pixel(10+decal, 10+y)
                self.assertEqual(target_c, extract)

    def test_skp(self):
        self.cpu.mem.V[0] = 10
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xE0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x9E
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode="a", key=pygame.K_a,
                                      mod=pygame.KMOD_NONE)  # create the event
        self.cpu.key_pressed += [newevent]
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 4)
        self.assertEqual(self.cpu.key_pressed, [])

    def test_sknp(self):
        self.cpu.mem.V[0] = 10
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xE0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0xA1
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode="a", key=pygame.K_a,
                                      mod=pygame.KMOD_NONE)  # create the event
        self.cpu.key_pressed += [newevent]
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.PC, self.cpu.mem.PROG_START + 2)
        self.assertEqual(self.cpu.key_pressed, [])

    def test_ld_timer(self):
        self.cpu.mem.DT = 10
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x07
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 10)

    def test_ld_keypress(self):
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x0A
        newevent = pygame.event.Event(pygame.KEYDOWN, unicode="a", key=pygame.K_a,
                                      mod=pygame.KMOD_NONE)  # create the event
        pygame.event.post(newevent)  # add the event to the queue
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.V[0], 0xA)

    def test_ld_settimer(self):
        self.cpu.mem.V[0] = 10
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x15
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.DT, 10)

    def test_ld_setsoundtimer(self):
        self.cpu.mem.V[0] = 10
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x18
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.ST, 10)

    def test_add_i(self):
        self.cpu.mem.I = 0xFE
        self.cpu.mem.V[0] = 1
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x1E
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.I, 0xFF)

    def test_ld_sprite(self):
        self.cpu.mem.V[0] = 0xA
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x29
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.I, self.cpu.mem.HEXFONT + self.cpu.mem.V[0] * self.cpu.mem.SPRITE_SIZE)

    def test_ld_bcd(self):
        self.cpu.mem.V[0] = 0xFF
        self.cpu.mem.I = 0
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF0
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x33
        self.cpu.execute()
        self.assertEqual(self.cpu.mem.mem[self.cpu.mem.I], 0x2)
        self.assertEqual(self.cpu.mem.mem[self.cpu.mem.I + 1], 0x5)
        self.assertEqual(self.cpu.mem.mem[self.cpu.mem.I + 2], 0x5)

    def test_dumpregs(self):
        regs_test_value = [random.randrange(0, 255) for i in range(8)]
        for idx, randval in enumerate(regs_test_value):
            self.cpu.mem.V[idx] = randval
        self.cpu.mem.I = 0
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF8
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x55
        self.cpu.execute()
        for idx, randval in enumerate(regs_test_value):
            self.assertEqual(self.cpu.mem.mem[self.cpu.mem.I + idx], randval)

    def test_loadregs(self):
        regs_test_value = [random.randrange(0, 255) for i in range(8)]
        for idx, randval in enumerate(regs_test_value):
            self.cpu.mem.mem[self.cpu.mem.I + idx] = randval
        self.cpu.mem.I = 0
        self.cpu.mem.mem[self.cpu.mem.PROG_START] = 0xF8
        self.cpu.mem.mem[self.cpu.mem.PROG_START + 1] = 0x65
        self.cpu.execute()
        for idx, randval in enumerate(regs_test_value):
            self.assertEqual(self.cpu.mem.V[idx], randval)




class MemTest(unittest.TestCase):

    def setUp(self):
        self.mem = Mem.Mem()

    def test_push(self):
        old_sp_value = self.mem.SP
        self.mem.push(1337)
        self.assertEqual(self.mem.SP, old_sp_value+1)
        self.assertEqual(self.mem.stack[self.mem.SP - 1], 1337)

    def test_pop(self):
        self.mem.push(1337)
        old_sp_value = self.mem.SP
        self.assertEqual(self.mem.pop(), 1337)
        self.assertEqual(self.mem.SP, old_sp_value - 1)

class InstructionDecoderTest(unittest.TestCase):

    def test_opcodemap(self):
        self.assertEqual(OpcodeMap[nibble_split_byte(0x00, 0xE0)], ("cls", None))
        self.assertEqual(OpcodeMap[nibble_split_byte(0x00, 0xEE)], ("ret", None))
        self.assertEqual(OpcodeMap[nibble_split_byte(0x10, 0xEE)], ("jp", decode_nnn))
        self.assertEqual(OpcodeMap[nibble_split_byte(0x20, 0xEE)], ("call", decode_nnn))


if __name__ == '__main__':
    unittest.main()
