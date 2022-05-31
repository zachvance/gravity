# gravity

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple gravity simulation using Python and Matplotlib.

## Usage

1. Adjust the settings located in config.py to your liking.
2. Run main.py

## Background

This project came about as more of a 'happy accident' - a byproduct of my attempting to generate a procedural image of a nebula.

I started off by generating randomized, still images of starfields using PIL. They looked fine for what I had set out to accomplish, but I still felt that the random placement of stars could use some more organic clustering. I figured I had two options; either place the stars randomly but give a higher weight to an area that already has a star in proximity, or place the stars randomly and then move them by applying some kind of directional force.

Placing them by weighted areas would probably have worked and been easier to implement, but I thought that I could learn more from a gravity simulation, and have more fun playing with the variables.

The first version used the force of gravity, however, at first I could only get the objects to attract and 'stick' to eachother. After some searching I learned that I also needed to apply a base velocity to each object to stop them from colliding and allow them to fall into orbit.

[This video](https://www.youtube.com/watch?v=WTLPmUHTPqo) on YouTube helped me understand the mechanics and allowed me to fix my code via it's velocities, force x, and force y.

## Todo

- Probably add an argparse menu
- Add options for saving both the finalized still image and an MP4 animation
- Add some colour options

## Sample images

<img src="https://github.com/zachvance/gravity/blob/main/images/sample1.png" alt="Sample 1" width="400"/>
<img src="https://github.com/zachvance/gravity/blob/main/images/sample2.png" alt="Sample 2" width="400"/>
