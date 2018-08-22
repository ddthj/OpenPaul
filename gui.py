import os
import sys
import pygame


folder = os.path.dirname(os.path.realpath(__file__))
background = os.path.join(folder, "background.jpg")

IMG_WIDTH = 1487
IMG_HEIGHT = 1006
SCALE = 0.5


class GUI():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((int(IMG_WIDTH * SCALE), int(IMG_HEIGHT * SCALE)))
        self.bg = pygame.image.load(background).convert_alpha()
        self.white = (255, 255, 255)
        self.orange = (255, 150, 0)
        self.blue = (0, 120, 255)
        self.black = (0, 0, 0)
        self.purple = (148, 0, 211)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.grey = (140, 140, 140)

    def update(self, s):

        # drawing background
        self.render(self.bg, 0, 0, int(IMG_WIDTH * SCALE), int(IMG_HEIGHT * SCALE))

        # drawing the ball
        self.circle(*self.gui_coords(*s.bL[:2]), 5, self.black)

        # drawing each car
        for i in range(s.game.numCars):
            car = s.game.gamecars[i]
            car_color = self.blue if car.Team == 0 else self.orange
            self.circle(*self.gui_coords(car.Location.X, car.Location.Y), 5, car_color)

        if hasattr(s, "tL"):
            # This draws the point the agent is currently targeting
            self.circle(*self.gui_coords(*s.tL[:2]), 5, self.red, 2)

            if hasattr(s, "tLb"):
                self.line(self.gui_coords(*s.tLb[:2]), self.gui_coords(*s.tL[:2]), self.grey)
                self.circle(*self.gui_coords(*s.tLb[:2]), 2, self.purple)

        if hasattr(s, "tcL"):
            self.circle(*self.gui_coords(*s.tcL[:2]), self.gui_rescale(s.trd), self.grey, 1)
            self.circle(*self.gui_coords(*s.pcL[:2]), self.gui_rescale(s.prd), self.grey, 1)
            self.line(self.gui_coords(*s.pcTL[:2]), self.gui_coords(*s.tcTL[:2]), self.grey)

        # update render
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # no hanging on exit
                pygame.quit()
                sys.exit()

    def rectangle(self, x, y, width, height, color):
        pygame.draw.rect(self.window, color, (x, y, width, height))

    def circle(self, x, y, radius, color, outline=0):
        pygame.draw.circle(self.window, color, (x, y), radius, outline)

    def line(self, point1, point2, color):
        pygame.draw.line(self.window, color, point1, point2)

    def render(self, image, x, y, width, height):
        image = pygame.transform.scale(image, (width, height))
        surface = pygame.Rect(x, y, width, height)
        self.window.blit(image, surface)

    def gui_rescale(self, x):
        """Rescales from game to gui size"""
        return int(x * 0.11763 * SCALE)

    def x_coord(self, x):
        return int((x * 0.11693 + 744) * SCALE)

    def y_coord(self, y):
        return int((-y * 0.11833 + 505) * SCALE)

    def gui_coords(self, x, y):
        """Converts 2d coordinates from the game to the gui"""
        return self.x_coord(y), self.y_coord(x)

    def game_coords(self, point):
        """Converts a point/pixel in the gui to game coordinates"""
        return (-(point[1] / SCALE - 505) / 0.11833, (point[0] / SCALE - 744) / 0.11693)
