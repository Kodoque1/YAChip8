from InstructionDecoder import *
from random import randrange
import pygame
import struct

hexfont = \
    [0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
     0x20, 0x60, 0x20, 0x20, 0x70,  # 1
     0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
     0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
     0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
     0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
     0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
     0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
     0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
     0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
     0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
     0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
     0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
     0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
     0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
     0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
     ]

TIMER = pygame.USEREVENT + 1


class Cpu:
    def __init__(self, mem, rom, scr, sample):
        self.scr = scr
        self.mem = mem
        self.operand0 = 0
        self.operand1 = 0
        self.operand2 = 0
        self.key_pressed = []
        self.running = True
        if sample:
            self.soundObj = pygame.mixer.Sound(sample)

        idx = 0
        while byte := rom.read(1):
            self.mem.mem[self.mem.PROG_START + idx] = struct.unpack('B', byte)[0]

            idx += 1

        for idx, byte in enumerate(hexfont):
            self.mem.mem[self.mem.HEXFONT + idx] = byte

    def execute(self):
        if self.mem.ST > 0:
            #self.soundObj.play()
            pass

        opcode, decoder = OpcodeMap[nibble_split_byte(self.mem.mem[self.mem.PC], self.mem.mem[self.mem.PC + 1])];
        if decoder:
            decoder((self.mem.mem[self.mem.PC] << 8) + self.mem.mem[self.mem.PC + 1], self)
        # print(opcode)
        # We increment the program counter before the execution of an instruction as some of them modify the PC register
        self.mem.PC += 2
        getattr(self, opcode)()

    def decrement_counters(self):
        # We update the timer and sound register, we assume that the execute function is executed at a 60 Hz rate
        if self.mem.DT > 0:
            self.mem.DT -= 1

        if self.mem.ST > 0:
            self.mem.ST -= 1

    def sys(self):
        # opcode used in old system, should be ignored
        pass

    def cls(self):
        self.scr.clear()

    def ret(self):
        self.mem.PC = self.mem.pop()

    def jp(self):
        self.mem.PC = self.operand0

    def call(self):
        self.mem.push(self.mem.PC)  # PC is preincremented
        self.mem.PC = self.operand0

    def se(self):
        if self.mem.V[self.operand0] == self.operand1:
            self.mem.PC += 2

    def sne(self):
        if self.mem.V[self.operand0] != self.operand1:
            self.mem.PC += 2

    def se_1(self):
        if self.mem.V[self.operand0] == self.mem.V[self.operand1]:
            self.mem.PC += 2

    def ld(self):
        self.mem.V[self.operand0] = self.operand1

    def add(self):
        acc = self.mem.V[self.operand0] + self.operand1
        if acc > 255:
            self.mem.V[15] = 1
        else:
            self.mem.V[15] = 0
        self.mem.V[self.operand0] = acc & 0xFF

    def ld_1(self):
        self.mem.V[self.operand0] = self.mem.V[self.operand1]

    def or_(self):
        self.mem.V[self.operand0] |= self.mem.V[self.operand1]

    def and_(self):
        self.mem.V[self.operand0] &= self.mem.V[self.operand1]

    def xor(self):
        self.mem.V[self.operand0] ^= self.mem.V[self.operand1]

    def add_1(self):
        acc = self.mem.V[self.operand0] + self.mem.V[self.operand1]
        if acc > 255:
            self.mem.V[15] = 1
        else:
            self.mem.V[15] = 0
        self.mem.V[self.operand0] = acc & 0xFF

    def sub(self):
        acc = self.mem.V[self.operand0] - self.mem.V[self.operand1]
        if acc < 0:
            self.mem.V[15] = 1
            self.mem.V[self.operand0] = 256 + acc
        else:
            self.mem.V[15] = 0
            self.mem.V[self.operand0] = acc

    def shr(self):
        self.mem.V[15] = self.mem.V[self.operand0] & 1
        self.mem.V[self.operand0] >>= 1

    def subn(self):
        acc = self.mem.V[self.operand1] - self.mem.V[self.operand0]
        if acc < 0:
            self.mem.V[15] = 1
            self.mem.V[self.operand0] = 256 + acc
        else:
            self.mem.V[15] = 0
            self.mem.V[self.operand0] = acc

    def shl(self):
        self.mem.V[15] = (self.mem.V[self.operand0] & 0x80) >> 7
        acc = (self.mem.V[self.operand0] << 1) & 0xFF
        self.mem.V[self.operand0] = acc

    def sne_1(self):
        if self.mem.V[self.operand0] != self.mem.V[self.operand1]:
            self.mem.PC += 2

    def ld_i(self):
        self.mem.I = self.operand0

    def jp_v0(self):
        self.mem.PC = self.operand0 + self.mem.V[0]

    def rnd(self):
        self.mem.V[self.operand0] = randrange(0, 255) & self.operand1

    def drw(self):
        x = self.mem.V[self.operand0]
        y = self.mem.V[self.operand1]
        sprite = []
        for i in range(self.operand2):
            # breakpoint()
            sprite += [self.mem.mem[self.mem.I + i]]
        self.mem.V[15] = self.scr.draw_sprite(x, y, sprite)

    def skp(self):
        reg_value = self.mem.V[self.operand0]
        if 0 <= reg_value < 10:
            target_key = getattr(pygame, "K_KP" + hex(reg_value)[2:].lower())
        else:
            target_key = getattr(pygame, "K_" + hex(reg_value)[2:].lower())
        for event in self.key_pressed:
            # we already know that it is a keydown event
            if event.key == target_key:
                self.mem.PC += 2
                break
        self.key_pressed = []

    def sknp(self):

        reg_value = self.mem.V[self.operand0]
        if 0 <= reg_value < 10:
            target_key = getattr(pygame, "K_KP" + hex(reg_value)[2:].lower())
        else:
            target_key = getattr(pygame, "K_" + hex(reg_value)[2:].lower())
        #print("K_" + hex(reg_value)[2:].lower())
        for event in self.key_pressed:
            if event.key == target_key:
                print("sknp")
                self.key_pressed = []
                return
        self.mem.PC += 2


    def ld_timer(self):
        self.mem.V[self.operand0] = self.mem.DT

    def ld_keypress(self):
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                for button in range(10):
                    if getattr(pygame, "K_" + hex(button)[2:]) == event.key:
                        self.mem.V[self.operand0] = button
                        return
                    # We also handle keypad
                    if getattr(pygame, "K_KP" + hex(button)[2:]) == event.key:
                        self.mem.V[self.operand0] = button
                        return
                for button in range(10, 16):
                    if getattr(pygame, "K_" + hex(button)[2:]) == event.key:
                        self.mem.V[self.operand0] = button
                        return
            elif event.type == TIMER:
                # We have to handle the decrement while we wait
                # print(event)
                self.decrement_counter()
            elif event.type == pygame.QUIT:
                self.running = False
                return

    def ld_settimer(self):
        self.mem.DT = self.mem.V[self.operand0]

    def ld_setsoundtimer(self):
        self.mem.ST = self.mem.V[self.operand0]

    def add_i(self):
        self.mem.I += self.mem.V[self.operand0]

    def ld_sprite(self):
        self.mem.I = self.mem.HEXFONT + self.mem.V[self.operand0] * self.mem.SPRITE_SIZE

    def ld_bcd(self):
        decimal_number = self.mem.V[self.operand0]
        self.mem.mem[self.mem.I + 2] = decimal_number % 10
        decimal_number //= 10
        self.mem.mem[self.mem.I + 1] = decimal_number % 10
        decimal_number //= 10
        self.mem.mem[self.mem.I] = decimal_number % 10

    def ld_dumpregs(self):
        for i in range(self.operand0 + 1):
            self.mem.mem[self.mem.I + i] = self.mem.V[i]

    def ld_loadregs(self):
        for i in range(self.operand0 + 1):
            self.mem.V[i] = self.mem.mem[self.mem.I + i]
