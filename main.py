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

    def AND(__self__):
        pass

    def LD(__self__):
        pass

    def SNE(__self__):
        pass

    def XOR(__self__):
        pass

    def SUB(__self__):
        pass

    def SKNP(__self__):
        pass

    def JP(__self__):
        pass

    def SHR(__self__):
        pass

    def RET(__self__):
        pass

    def RND(__self__):
        pass

    def SYS(__self__):
        pass

    def ADD(__self__):
        pass

    def CALL(__self__):
        pass

    def SKP(__self__):
        pass

    def SUBN(__self__):
        pass

    def SHL(__self__):
        pass

    def OR(__self__):
        pass

    def SE(__self__):
        pass

    def CLS(__self__):
        pass

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
        getattr(new,tmp[0])(tmp[1:])


if __name__ == '__main__':
    main()


