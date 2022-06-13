import pygame
import math

from sqlalchemy import PrimaryKeyConstraint
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
GREEN = (0, 255, 0)
RED = (189, 30, 50)
DARK_GREY = (80, 78, 81)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 8 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 10:
            self.orbit.pop(0)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            # pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP

        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 2, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 1, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 1, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 1, DARK_GREY, 3.3 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 1, WHITE, 4.8695 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.203 * Planet.AU, 0, 1, RED, 1.898 * 10**27)
    jupiter.y_vel = -13.07 * 1000

    saturn = Planet(-9.586 * Planet.AU, 0, 1, YELLOW, 5.683 * 10**26)
    saturn.y_vel = 9.68 * 1000

    uranus = Planet(19.191 * Planet.AU, 0, 1, GREEN, 8.681 * 10**25)
    uranus.y_vel = -6.8 * 1000

    neptune = Planet(-30.047 * Planet.AU, 0, 1, BLUE, 1.024 * 10**26)
    neptune.y_vel = 5.43 * 1000

    pluto = Planet(39.506 * Planet.AU, 0, 1, DARK_GREY, 1.303 * 10**22)
    pluto.y_vel = -4.743 * 1000

    planets = [sun, earth, mars, mercury,
               venus, jupiter, saturn, uranus, neptune, pluto]

    while run:
        clock.tick(1000)
        WIN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
