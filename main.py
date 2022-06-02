from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.animation import FFMpegWriter, FuncAnimation

from config import (ANIMATE, BASE_X_VELOCITY, BASE_Y_VELOCITY,
                    DISTANCE_THRESHOLD, FACE_COLOUR, FOLLOW_OBJECT,
                    LABEL_COLOUR, NUMBER_OF_OBJECTS, OBJECT_COLOUR, PALETTE,
                    SAVE_OUTPUT, SAVE_VIDEO, SHOW_LABELS, SHOW_OBJECTS,
                    SHOW_TRAILS, STEPS, SUN, SUN_MASS, TIME_STEP, TRAIL_COLOUR,
                    ZOOM_LEVEL, G)


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


def attraction(a, b) -> Tuple[float, float]:
    """
    Calculates gravitational force based on Newton's universal law of gravitation.

    Calculates directional forces based on Kepler's planetary motion.

    Returns a tuple containing two floats representing the amount of force exerted on A by B in both x and y directions.

    :param a: Object A
    :param b: Object B
    :return: A tuple of floats
    """

    other_x, other_y = b.x, b.y
    distance_x = other_x - a.x
    distance_y = other_y - a.y
    distance = np.sqrt(distance_x ** 2 + distance_y ** 2)

    if distance > DISTANCE_THRESHOLD:
        force = G * a.mass * b.mass / distance ** 2
        theta = np.arctan2(distance_y, distance_x)
        force_x = np.cos(theta) * force
        force_y = np.sin(theta) * force

        return force_x, force_y

    else:
        return 0.0, 0.0


def update_coordinates(object_to_update, list_of_objects):
    total_fx = total_fy = 0
    for obj in list_of_objects:
        if obj == object_to_update:
            continue

        fx, fy = attraction(object_to_update, obj)
        total_fx += fx
        total_fy += fy

    object_to_update.x_velocity += total_fx / object_to_update.mass * TIME_STEP
    object_to_update.y_velocity += total_fy / object_to_update.mass * TIME_STEP

    object_to_update.x += object_to_update.x_velocity * TIME_STEP
    object_to_update.y += object_to_update.y_velocity * TIME_STEP

    object_to_update.orbit.append((object_to_update.x, object_to_update.y))


def generate_objects() -> List:
    """
    Creates n number of objects and appends them to a list.

    If the 'SUN' variable in the config is True, will create an additional 'sun' object and append it to the end of the
    object list.

    :return: A list of object instances
    """
    x = np.random.rand(NUMBER_OF_OBJECTS)
    y = np.random.rand(NUMBER_OF_OBJECTS)

    li = list(map(list, zip(x, y)))

    object_list = []
    for coordinates in li:

        brightness = np.random.rand() * 1.6
        if brightness > 1:
            brightness = 1

        obj = Object(
            coordinates[0],
            coordinates[1],
            np.random.rand(),
            brightness,
            BASE_X_VELOCITY,
            BASE_Y_VELOCITY,
        )
        object_list.append(obj)

    if SUN:
        sun = Object(0.50, 0.50, SUN_MASS, 1, 0.0, 0.0)
        object_list.append(sun)

    return object_list


def plot_objects(self=None) -> None:
    """
    Handles the creation of the plot for both still images and/or an animation.

    .. todo:
        Currently has an unused argument because FuncAnimation requires it. I would like to refactor to clean this up.

    :return: None
    """
    plt.cla()
    ax = plt.gca()
    ax.set_facecolor(color=FACE_COLOUR)

    # Lists for plotting
    x = []
    y = []
    labels = []
    size = []
    brightness = []
    orbit_x = []
    orbit_y = []
    orbit_colour = []

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
            update_coordinates(item, LIST_OF_OBJECTS)
        x.append(item.x)
        y.append(item.y)
        labels.append(round(item.mass, 4))
        size.append(item.mass * 10)
        brightness.append(item.brightness)
        for orbit_point in item.orbit:
            orbit_x.append(orbit_point[0])
            orbit_y.append(orbit_point[1])
            orbit_colour.append(item.brightness)

    # Plot trajectories
    if SHOW_TRAILS:
        sns.scatterplot(
            x=orbit_x,
            y=orbit_y,
            s=1,
            alpha=0.7,
            hue=orbit_colour,
            palette=PALETTE,
            linewidth=0,
            legend=False,
            ax=ax,
        )

    # Plot objects
    if SHOW_OBJECTS:
        sns.scatterplot(x=x, y=y, alpha=brightness, s=size, color=OBJECT_COLOUR)

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

    # If you're not animating and just want a finalized imaged output saved:
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
