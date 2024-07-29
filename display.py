import pygame
import engine


def main():
    pygame.init()

    window_width = 1500
    window_height = 1000
    center_x = window_width // 2
    center_y = window_height // 2
    scale = 150
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Double Inverted Pendulum on Cart")

    system = engine.DIPC()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    system.u = -400
                if event.key == pygame.K_RIGHT:
                    system.u = 400
            else:
                system.u = 0
        window.fill((0, 0, 0))

        system.update()

        # left, top, width, height
        cart = (
            int((system.x0 - system.w / 2) * scale + center_x),
            int(-system.h * scale + center_y),
            int(system.w * scale),
            int(system.h * scale),
        )
        points = (
            (int(system.x0 * scale + center_x), int(-system.h * scale + center_y)),
            (int(system.x1 * scale + center_x), int(-system.y1 * scale + center_y)),
            (int(system.x2 * scale + center_x), int(-system.y2 * scale + center_y)),
        )
        pygame.draw.rect(window, (255, 255, 255), cart)
        pygame.draw.lines(window, (255, 255, 255), False, points, 2)

        pygame.display.flip()


if __name__ == "__main__":
    main()
