import unittest
import main
import pygame
from pygame import *
import sys
from Assembler import assemble_byte

def assemble_drw(x,y,n):
    return ((0xD << 4) + x, (y << 4) + n)

class interpreterTest(unittest.TestCase):



    def test_drw(self):

        (width,height)=(64,32)
        pygame.init()
        screen=pygame.display.set_mode((width, height))
        pygame.display.flip()

        self.itrp=main.interpreter(screen)
        self.itrp.regI=0
#        tmp=assemble_drw(0,0,5)

        for i in range(2,10):
            self.itrp.mem[i] = 255

        #self.itrp.scr[i]=tmp[0]
        #self.itrp.scr[i+1]=tmp[1]

        lf.itrp.DRW((0,0,30)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()



if __name__ == '__main__':
    unittest.main()
