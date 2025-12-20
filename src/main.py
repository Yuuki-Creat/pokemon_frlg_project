import pygame
from engine.engine import engine_run

def main():
    pygame.init()
    screen = pygame.display.set_mode((320, 267))
    # screen = pygame.display.set_mode((240, 160))
    pygame.display.set_caption("FRLG-like Engine (PoC)")
    clock = pygame.time.Clock()

    engine = engine_run(screen, clock)
    engine.run()

    pygame.quit()

if __name__ == "__main__":
    main()
