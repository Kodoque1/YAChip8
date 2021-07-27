import pygame

WHITE = (255,255,255)
BLACK = (0,0,0)
CHIP8_WIDTH = 64
CHIP8_HEIGHT = 32

class Screen:
    def __init__(self, width, height):
        width = max(width, CHIP8_WIDTH)
        height = max(height, CHIP8_HEIGHT)
        self.pixel_size_x = width // CHIP8_WIDTH
        self.pixel_size_y = height // CHIP8_HEIGHT
        self.screen = pygame.display.set_mode((width, height))

    def get_pixel(self, x, y):
        color = self.screen.get_at((x * self.pixel_size_x, y * self.pixel_size_y))
        if color == WHITE:
            return 1
        else:
            return 0

    def set_pixel(self, x, y, c):
        if c == 1:
            color = WHITE
        else:
            color = BLACK
        xs, ys = (self.pixel_size_x, self.pixel_size_y)
        pygame.draw.rect(self.screen, color, (x * xs, y * ys, xs, ys))

    def draw_sprite(self, x, y, sprite):
        overwrite = 0

        for idx, line in enumerate(sprite):
            for decal in range(8):
                e = (line >> (7 - decal)) & 1
                c = self.get_pixel((x + decal) % CHIP8_WIDTH, (y + idx) % CHIP8_HEIGHT)
                if overwrite != 1:
                    overwrite = e & c
                self.set_pixel((x + decal) % CHIP8_WIDTH, (y + idx) % CHIP8_HEIGHT, e ^ c)
        pygame.display.flip()

        return overwrite

    def resize(self, width, height):
        old_surface = self.screen
        old_pixel_size_x = self.pixel_size_x
        old_pixel_size_y = self.pixel_size_y
        self.pixel_size_x = width // CHIP8_WIDTH
        self.pixel_size_y = height // CHIP8_HEIGHT
        self.screen = pygame.display.set_mode((width, height))
        for i in range(CHIP8_WIDTH):
            for j in range(CHIP8_HEIGHT):
                if old_surface.get_at((i * old_pixel_size_x, j * old_pixel_size_y)) == WHITE:
                    c = 1
                else:
                    c = 0
                self.set_pixel(i, j, c)

    def clear(self):
        self.screen.fill((0, 0, 0));