class Mem:
    PROG_START = 0x200
    MEM_SIZE = 0x1000
    STACK_SIZE = 0x10
    REGISTER_NUM = 0x10
    HEXFONT = 0x50
    SPRITE_SIZE = 0x5

    def __init__(self):
        self.mem = self.MEM_SIZE * [0]
        self.stack = self.STACK_SIZE * [0]
        self.V = self.REGISTER_NUM * [0]
        self.I = 0
        self.DT = 0x0
        self.ST = 0x0
        self.PC = self.PROG_START
        self.SP = 0

    def push(self, word):
        self.stack[self.SP] = word
        self.SP = self.SP + 1

    def pop(self):
        self.SP = self.SP - 1
        return self.stack[self.SP]