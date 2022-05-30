import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Global configs
BASE_X_VELOCITY = 0.0000001
BASE_Y_VELOCITY = 0.0000001
G = 0.0000001
TIME_STEP = .3
NUMBER_OF_OBJECTS = 2
SUN = True
SUN_MASS = 20
DISTANCE_THRESHOLD = 0.03
ZOOM_LEVEL = 0.5
FOLLOW_OBJECT = False
SHOW_OBJECTS = False
SHOW_TRAILS = True
SHOW_LABELS = False
STEPS = 200000
ANIMATE = False


class Object:
    def __init__(self, x, y, mass, brightness, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.mass = mass
        self.brightness = brightness
        self.new_coordinates = [self.x, self.y]
        self.colour = None
        self.radius = None

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.orbit = []

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = np.sqrt(distance_x ** 2 + distance_y ** 2)

        if distance > DISTANCE_THRESHOLD:
            force = G * self.mass * other.mass / distance ** 2
            theta = np.arctan2(distance_y, distance_x)
            force_x = np.cos(theta) * force
            force_y = np.sin(theta) * force

            return force_x, force_y

        else:
            return 0, 0

    def update_position(self, stars):
        total_fx = total_fy = 0
        for star in stars:
            if star == self:
                continue

            fx, fy = self.attraction(star)
            total_fx += fx
            total_fy += fy

        self.x_velocity += total_fx / self.mass * TIME_STEP
        self.y_velocity += total_fy / self.mass * TIME_STEP

        self.x += self.x_velocity * TIME_STEP
        self.y += self.y_velocity * TIME_STEP

        self.orbit.append((self.x, self.y))


def generate_stars():
    x = np.random.rand(NUMBER_OF_OBJECTS)
    y = np.random.rand(NUMBER_OF_OBJECTS)

    li = list(map(list, zip(x, y)))

    object_list = []
    for coordinates in li:
        b = np.random.rand() * 2.4
        if b > 1:
            b = 1
        s = Object(
            coordinates[0],
            coordinates[1],
            np.random.rand(),
            b,
            BASE_X_VELOCITY,
            BASE_Y_VELOCITY,
        )
        object_list.append(s)

    if SUN:
        sun = Object(0.50, 0.50, SUN_MASS, 1, 0.0, 0.0)
        object_list.append(sun)

    return object_list


def animate(i):
    plt.cla()
    ax = plt.gca()

    for star in LI:
        star.update_position(LI)

    x = []
    y = []
    n = []
    s = []
    b = []

    orbit_x = []
    orbit_y = []

    for item in LI:
        ix = item.x
        iy = item.y
        x.append(item.x)
        y.append(item.y)
        n.append(round(item.mass, 3))
        item.x = ix
        item.y = iy
        ii = item.mass
        s.append(ii * 9)
        ib = item.brightness
        b.append(ib)

        for item_y in item.orbit:
            orbit_x.append(item_y[0])
            orbit_y.append(item_y[1])

    # Plot trajectories
    if SHOW_TRAILS:
        plt.scatter(orbit_x, orbit_y, alpha=0.5, s=0.08, c="r")

    # Plot objects
    if SHOW_OBJECTS:
        plt.scatter(x, y, alpha=1, s=s, c="w")

    # Plot data labels
    if SHOW_LABELS:
        for i, txt in enumerate(n):
            plt.annotate(txt, (x[i], y[i]), color="w")

    if FOLLOW_OBJECT:
        follow_body = LI[-1]
        x_min = follow_body.x - ZOOM_LEVEL
        x_max = follow_body.x + ZOOM_LEVEL
        y_min = follow_body.y - ZOOM_LEVEL
        y_max = follow_body.y + ZOOM_LEVEL
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
    else:
        plt.xlim(0, 1)
        plt.ylim(0, 1)

    ax.set_facecolor(color="black")


def static(objects):
    plt.cla()
    ax = plt.gca()

    for i in range(STEPS):
        for star in LI:
            star.update_position(LI)

    x = []
    y = []
    n = []
    s = []
    b = []

    orbit_x = []
    orbit_y = []

    for item in objects:
        ix = item.x
        iy = item.y
        x.append(item.x)
        y.append(item.y)
        n.append(round(item.mass, 3))
        item.x = ix
        item.y = iy
        ii = item.mass
        s.append(ii * 9)
        ib = item.brightness
        b.append(ib)

        for item_y in item.orbit:
            orbit_x.append(item_y[0])
            orbit_y.append(item_y[1])

    # Plot trajectories
    if SHOW_TRAILS:
        plt.scatter(orbit_x, orbit_y, alpha=0.2, s=0.08, c="w")

    # Plot objects
    if SHOW_OBJECTS:
        plt.scatter(x, y, alpha=1, s=s, c="w")

    # Plot data labels
    if SHOW_LABELS:
        for i, txt in enumerate(n):
            plt.annotate(txt, (x[i], y[i]), color="w")

    if FOLLOW_OBJECT:
        follow_body = LI[-1]
        x_min = follow_body.x - ZOOM_LEVEL
        x_max = follow_body.x + ZOOM_LEVEL
        y_min = follow_body.y - ZOOM_LEVEL
        y_max = follow_body.y + ZOOM_LEVEL
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
    else:
        plt.xlim(0, 1)
        plt.ylim(0, 1)

    ax.set_facecolor(color="black")


if __name__ == "__main__":
    fig = plt.figure()
    LI = generate_stars()
    if ANIMATE:
        ani = FuncAnimation(fig, animate, interval=1)
    else:
        static(LI)
    plt.show()
