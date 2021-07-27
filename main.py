import pygame
import Screen
import Mem
import argparse
import Cpu

TIMER = pygame.USEREVENT + 1
# 60hz frequency
DELAY_INTERVAL = 17


def main():
    parser = argparse.ArgumentParser(description='Chip 8 Emulator.')
    parser.add_argument('rom', type=str, help='Path to the rom')
    parser.add_argument("width", type=int, help='Width of chip8 screen in pixel')
    parser.add_argument("height", type=int, help='Width of chip8 screen in pixel')
    parser.add_argument("delay", type=int, help='CPU frequency (give delay in milliseconds)')
    parser.add_argument("sample", type=str, help='Path to the buzzer sound')

    args = parser.parse_args()
    rom, width, height, sample = (args.rom, args.width, args.height, args.sample)

    with open(rom, "rb") as f:

        screen = Screen.Screen(width, height)

        pygame.init()
        pygame.time.set_timer(TIMER, DELAY_INTERVAL)
        mem = Mem.Mem()
        cpu = Cpu.Cpu(mem, f, screen, sample)

        while cpu.running:
            pygame.time.wait(args.delay)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cpu.running = False
                if event.type == pygame.KEYDOWN:
                    print("Key pressed")
                    cpu.key_pressed += [event]
                if event.type == TIMER:
                    cpu.decrement_counters()
            cpu.execute()


if __name__ == '__main__':
    main()
