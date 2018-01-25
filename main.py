import pygame

black = (0,0,0,255)
white = (255,255,255,255)

opcode_map = {
    0xD : "DRW"
}

def get_nibbles(num):
    return ((num >> 4 & 0xF),num  & 0xF)

def get_nibbles_from_word(num):
    return get_nibbles( num >> 8 & 0xFF) + get_nibbles(num & 0xff)

def get_bits(byte):
    for i in range(8):
        yield (byte >> i) & 1

class interpreter:
    def __init__(self,scr):
        self.regI=0;
        self.reg1=0;
        self.scr=scr;
        self.mem=4096*[0]
        self.VF=0;
        self.V= 16*[0]
        self.pc=0;
        self.sp=0;

    def AND(self,reg0,reg1):
        self.V[reg0] |= self.V[reg1]

    def LD(self,reg,byte):
        self.V[reg]=byte;

    def LD1(self,reg0,reg1):
        self.V[reg0] = self.V[reg1];

    def SNE(self,reg,byte):
        if self.V[reg] != byte:
            self.pc+=1

    def XOR(self,reg0,reg1):
        self.V[reg0] ^= self.V[reg1]

    def SUB(self):
        pass

    def SKNP(self):
        pass

    def JP(self, addr):
        self.pc = addr

    def SHR(self):
        pass

    def RET(self):
        self.pc=self.mem[self.sp]
        self.sp-=1

    def RND(self):
        pass

    def SYS(self):
        pass

    def ADD(self, reg, byte):
        self.V[reg] += byte

    def ADD1(self, reg0, reg1):
        self.V[reg0] += self.V[reg1]

    def CALL(self,addr):
        self.sp+=1
        self.mem[self.sp]=self.pc
        self.pc=addr

    def SKP(self):
        pass

    def SUBN(self):
        pass

    def SHL(self):
        pass

    def OR(self,reg0,reg1):
        self.V[reg0] |= self.V[reg1]

    def SE(self,reg,byte):
        if self.V[reg] == byte:
            self.pc+=1

    def SE1(self,reg0,reg1):
        if self.V[reg0] == self.V[reg1]:
            self.pc+=1

    def CLS(self):
        self.scr.fill(black)

    # Draw on the screen a sprites

    def DRW(self,args):
        x, y, n = args

        for i in range(n):
            byte = self.mem[self.regI + i]
            for (idx,e) in enumerate(get_bits(byte)):
                old_color = self.scr.get_at((x+idx,y+i))
                new_color = white if (int(old_color==white) ^ e) else black

                if old_color != new_color:
                    self.VF=1

                self.scr.set_at((x+idx, y+i), new_color)
        pygame.display.update()




def main():

    (width,height)=(64,32)
    screen=pygame.display.set_mode((width, height))
    pygame.display.flip()

    f=open("rom.txt")
    itrp=interpreter(screen)

    code=iter(f.readlines())

    # Load code in memory

    for opcode in f.readlines():
        tmp = opcode.split()
        getattr(itrp,tmp[0])(tmp[1:])


if __name__ == '__main__':
    main()


