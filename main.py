from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from config import (ANIMATE, BASE_X_VELOCITY, BASE_Y_VELOCITY,
                    DISTANCE_THRESHOLD, FOLLOW_OBJECT, LABEL_COLOUR,
                    NUMBER_OF_OBJECTS, OBJECT_COLOUR, SAVE_OUTPUT, SHOW_LABELS,
                    SHOW_OBJECTS, SHOW_TRAILS, STEPS, SUN, SUN_MASS, TIME_STEP,
                    TRAIL_COLOUR, ZOOM_LEVEL, G)


class Object:
    def __init__(self, x, y, mass, brightness, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.mass = mass
        self.brightness = brightness
        self.new_coordinates = [self.x, self.y]
        self.colour = None  # Not currently used
        self.radius = None  # Not currently used

        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.orbit = []

    def attraction(self, other) -> Tuple[float, float]:
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
            return 0.0, 0.0

    def update_coordinates(self, stars):
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


def generate_objects() -> List:
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


def plot_objects(self=None) -> None:
    plt.cla()
    ax = plt.gca()
    ax.set_facecolor(color="black")

    # Lists for plotting
    x = []
    y = []
    labels = []
    size = []
    brightness = []
    orbit_x = []
    orbit_y = []

    """
    If ANIMATE is False, we just want to plot the final image, so we iterate through our list of objects and update
    their positions n number of times (STEPS), and then move on to plotting.
    """
    if ANIMATE is False:
        for i in range(STEPS):
            for star in LIST_OF_OBJECTS:
                star.update_coordinates(LIST_OF_OBJECTS)

    for item in LIST_OF_OBJECTS:
        """
        If ANIMATE is True, then we update the position and then plot each item; the animation loop is handled via
        matplotlib.animation's FuncAnimation.
        """
        if ANIMATE:
            item.update_coordinates(LIST_OF_OBJECTS)
        x.append(item.x)
        y.append(item.y)
        labels.append(round(item.mass, 4))
        size.append(item.mass * 10)
        brightness.append(item.brightness)
        for orbit_point in item.orbit:
            orbit_x.append(orbit_point[0])
            orbit_y.append(orbit_point[1])

    # Plot trajectories
    if SHOW_TRAILS:
        plt.scatter(orbit_x, orbit_y, alpha=0.2, s=0.05, c=TRAIL_COLOUR)

    # Plot objects
    if SHOW_OBJECTS:
        plt.scatter(x, y, alpha=brightness, s=size, c=OBJECT_COLOUR)

    # Plot data labels
    if SHOW_LABELS:
        for i, txt in enumerate(labels):
            plt.annotate(txt, (x[i], y[i]), color=LABEL_COLOUR)

    # If FOLLOW_OBJECT is True then adjust the axis accordingly
    if FOLLOW_OBJECT:
        follow_body = LIST_OF_OBJECTS[-1]
        x_min = follow_body.x - ZOOM_LEVEL
        x_max = follow_body.x + ZOOM_LEVEL
        y_min = follow_body.y - ZOOM_LEVEL
        y_max = follow_body.y + ZOOM_LEVEL
        plt.xlim(x_min, x_max)
        plt.ylim(y_min, y_max)
    else:
        plt.xlim(0, 1)
        plt.ylim(0, 1)

    if ANIMATE is False and SAVE_OUTPUT is True:
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.savefig("plot.png", dpi=300, bbox_layout="tight")


if __name__ == "__main__":
    fig = plt.figure()
    LIST_OF_OBJECTS = generate_objects()
    if ANIMATE:
        ani = FuncAnimation(fig, plot_objects, interval=1)
    else:
        plot_objects()
    plt.show()
