def assemble_byte(n3,n2,n1,n0):
    return n3 << 12 + n2 << 8 + n1 << 4 + n0

class assembler:
    def __init__(self):
        self.out=open(filename,"wb")

    def CLS(self,args):
        self.out.write(0x00E0)

    def DRW(self,args):
        self.out.write()

def main():
    f=open("rom.txt")
    new=assembler()
    for opcode in f.readlines():
        tmp = opcode.split()
        getattr(new,tmp[0])(tmp[1:])

if __name__ == '__main__':
    main()