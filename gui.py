import os
import sys
import pygame
from util import *
from classes import *
from paths import pathTypes
from copy import deepcopy


folder = os.path.dirname(os.path.realpath(__file__))
background = os.path.join(folder, "background.jpg")

IMG_WIDTH = 1487
IMG_HEIGHT = 1006
SCALE = 0.5


class GUI():
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Paul")
        self.window = pygame.display.set_mode((int(IMG_WIDTH * SCALE), int(IMG_HEIGHT * SCALE)))
        self.bg = pygame.image.load(background).convert_alpha()
        self.white = (255, 255, 255)
        self.orange = (255, 150, 0)
        self.blue = (0, 120, 255)
        self.black = (0, 0, 0)
        self.purple = (148, 0, 211)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.grey = (150, 150, 150)
        self.event_text = pygame.font.Font('freesansbold.ttf', 10)

        self.editing = True  # a new path will replace the existing path
        self.event_editing = False  # locks newlines and editing
        self.new_line = False

    def update(self, game, agent):

        # start and end are flags for mouse events, arm is for triggering an event edit or creating a new event
        start_flag = end_flag = arm_edit = arm_new = up_flag = down_flag = False
        close_event = None

        # drawing background
        self.render(self.bg, 0, 0, int(IMG_WIDTH * SCALE), int(IMG_HEIGHT * SCALE))

        # recording mouse events
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:
                    start_flag = True
                elif event.button == 4:
                    # up scroll
                    up_flag = True
                elif event.button == 5:
                    # down scroll
                    down_flag = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    end_flag = True
                    self.new_line = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    agent.path = deepcopy(pathTypes.basicShot)
                elif event.key == pygame.K_2:
                    agent.path = pathTypes.basicShot
                elif event.key == pygame.K_3:
                    agent.path = pathTypes.basicShot
                elif event.key == pygame.K_4:
                    agent.path = pathTypes.basicShot
                elif event.key == pygame.K_5:
                    agent.path = pathTypes.basicShot

            if event.type == pygame.QUIT:  # no more hanging on exit
                pygame.quit()
                sys.exit()

        mouse_position = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        if len(agent.path.lines) > 0:

            # Drawing path and finding closest line to the mouse
            close_dist = dist2d(line_projection(*agent.path.get_points(), self.game_coords(mouse_position)),
                                self.game_coords(mouse_position))
            close_line = agent.path.get_line()

            for item in agent.path.lines:
                temp = dist2d(line_projection(item.start, item.end, self.game_coords(mouse_position)),
                              self.game_coords(mouse_position))
                if temp < close_dist:
                    close_dist = temp
                    close_line = item
                self.line(self.gui_coords(*a2(item.start)), self.gui_coords(*a2(item.end)), self.purple)
                # draws events on line
                for event in item.events:
                    event_loc = set_dist2d(item.start, item.end, event.distance)
                    self.circle(*self.gui_coords(*a2(event_loc)), 2, self.black)

            # drawing the mouse projection
            mouse_distance = dist2d(close_line.start, line_projection(
                close_line.start, close_line.end, self.game_coords(mouse_position)))

            # arming event_editing, causes start flag to trigger editing mode instead of newline
            if (close_dist < 200 and mouse_distance - 50 < dist2d(close_line.start, close_line.end) and
                dist2d(line_projection(close_line.start, close_line.end, self.game_coords(mouse_position)),
                       close_line.end) - 50 < dist2d(close_line.start, close_line.end)):
                # changing the projection circle color if we are over a line or event
                highlight = self.black
                for event in close_line.events:
                    if event.distance + 50 > mouse_distance and event.distance - 50 < mouse_distance:
                        if start_flag:
                            event.active_editing = True
                        arm_edit = True
                        close_event = event
                        highlight = self.blue
                        break
                    elif event.active_editing:
                        highlight = self.blue
                        break

                if not arm_edit:
                    if close_dist < 70:
                        highlight = self.green
                        arm_new = True

                self.circle(*self.gui_coords(*line_projection(close_line.start, close_line.end,
                                                              self.game_coords(mouse_position))), 5, highlight, 2)

            # entry circle
            if hasattr(agent, "circle_center"):
                self.circle(*self.gui_coords(*a2(agent.circle_center)),
                            self.gui_rescale(agent.circle_radius), self.grey, 1)

        # Flags and Mouse clicks are handled below
        # Drawing with the rightmousebutton turns editing back on so that a new path can be created
        if self.editing:
            if start_flag:
                self.line_start = mouse_position
            if end_flag:
                self.line_end = mouse_position
            if mouse_buttons[2] == 1 or mouse_buttons[0] == 1:
                self.line(self.line_start, mouse_position, self.purple)
            if self.new_line:
                temp = line(a3([*self.game_coords(self.line_start), 20]),
                            a3([*self.game_coords(self.line_end), 20]), 1400)
                agent.path = path([temp])
                self.editing = False
                self.new_line = False
        elif self.event_editing:
            if mouse_buttons[0] == 1:
                for event in close_line.events:
                    if event.active_editing and not event.anchored:
                        event.distance = mouse_distance
            if end_flag is True:
                for event in close_line.events:
                    event.active_editing = False
                self.event_editing = False
        else:
            if start_flag:
                if arm_new:
                    close_line.events.append(Event(mouse_distance, 1400))
                elif arm_edit:
                    self.event_editing = True
                    self.editing = False
                else:
                    self.line_start = mouse_position
            elif end_flag:
                self.line_end = mouse_position

            if mouse_buttons[2] == 1:
                self.line(self.line_start, mouse_position, self.purple)
                self.editing = True
                agent.path.clean()

            if mouse_buttons[0] == 1:
                if not arm_new and not arm_edit:
                    self.line(self.line_start, mouse_position, self.purple)
                else:
                    self.new_line = False

            if self.new_line:
                if not arm_new and not arm_edit:
                    temp = line(a3([*self.game_coords(self.line_start), 20]),
                                a3([*self.game_coords(self.line_end), 20]), 1400)
                    agent.path.lines.append(temp)
                    self.editing = False
                    self.new_line = False
                else:
                    self.new_line = False

            if up_flag and close_event is not None:
                close_event.speed += 10
            elif down_flag and close_event is not None:
                close_event.speed -= 10

        ball_loc = game.gameball.Location

        # drawing the ball
        self.circle(*self.gui_coords(ball_loc.X, ball_loc.Y), 5, self.black)

        # drawing each car
        for i in range(game.numCars):
            car = game.gamecars[i]
            if car.Team == 0:
                car_color = self.blue
            else:
                car_color = self.orange
            self.circle(*self.gui_coords(car.Location.X, car.Location.Y), 5, car_color)

            # player only
            if i == agent.index and len(agent.path.lines) > 0:
                # drawing nearest point on the user-made line
                line_projected_point = line_projection(*agent.path.get_points(), (car.Location.X, car.Location.Y))
                self.circle(*self.gui_coords(*line_projected_point), 1, car_color)

        # drawing lines to both goals
        for team in range(2):

            # enemy near post location (2D)
            near_post = (GOAL_WIDTH / 2 * sign(ball_loc.X), FIELD_LENGTH / 2 * sign(team))

            far_post = ((GOAL_WIDTH / 2 - BALL_RADIUS) * -sign(ball_loc.X), FIELD_LENGTH / 2 * sign(team))

            # drawing a circle around the near post
            self.circle(*self.gui_coords(*near_post), 5, self.white, 1)

            tangent_x, tangent_y = tangent_point(near_post, BALL_RADIUS, ball_loc, sign(team) * sign(ball_loc.X))

            # (ball, tangent_point) line intersection with the the goal line
            x_point = line_intersect([(1, near_post[1]), (-1, near_post[1])], [(ball_loc.X, ball_loc.Y),
                                                                               (tangent_x, tangent_y)])[0]

            # extending the lines from starting point by a fixed ammount
            line_length = 11000

            extended_tangent_point = set_dist2d([x_point, near_post[1]], ball_loc, line_length)

            extended_far_point = set_dist2d(far_post, ball_loc, line_length)

            if team == 0:
                line_color = self.blue
            else:
                line_color = self.orange

            # drawing tangent line passing near post
            self.line(self.gui_coords(x_point, near_post[1]), self.gui_coords(*extended_tangent_point), line_color)

            # drawing line to far post
            self.line(self.gui_coords(*far_post), self.gui_coords(*extended_far_point), line_color)

            # drawing near post entrance indication point
            self.circle(*self.gui_coords(x_point, near_post[1]), 1, self.white)

            # drawing far post indication point
            self.circle(*self.gui_coords(*far_post), 1, self.white)

        if hasattr(agent, "player_circle"):
            # drawing the circle showing the current min turn radius
            self.circle(*self.gui_coords(*a2(agent.player_circle)),
                        self.gui_rescale(agent.player_radius), self.purple, 1)

        # This draws the point the agent is currently targeting
        self.circle(*self.gui_coords(*a2(agent.target_loc)), 2, self.red)

        if arm_edit:
            self.draw_event_box(close_event, *mouse_position)

        pygame.display.update()

    def post_update(self, agent):

        pygame.display.update()

    def draw_event_box(self, event, x, y):
        text = []
        text.append(str(int(event.distance)))
        text.append(str(event.speed))
        self.rectangle(x + 10, y + 10, 50, 40, self.grey)
        height = 0
        for z in text:
            text_surface = pygame.font.Font.render(self.event_text, z, True, self.black)
            text_rect = text_surface.get_rect()
            text_rect.x = x + 15
            text_rect.y = y + 15 + (10 * height)
            self.window.blit(text_surface, text_rect)
            height += 1

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

    # rescales from game to gui size
    def gui_rescale(self, x):
        return int(x * 0.11763 * SCALE)

    def x_coord(self, x):
        return int((x * 0.11693 + 744) * SCALE)

    def y_coord(self, y):
        return int((-y * 0.11833 + 505) * SCALE)

    def gui_coords(self, x, y):  # converts 2d coordinates from the game to the gui
        return self.x_coord(y), self.y_coord(x)

    def game_coords(self, point):  # converts a point/pixel in the gui to game coordinates
        return (-(point[1] / SCALE - 505) / 0.11833, (point[0] / SCALE - 744) / 0.11693)
