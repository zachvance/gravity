# gravity

A simple gravity simulation using Python and Matplotlib.

## Usage

1. Adjust the settings located in config.py to your liking.
2. Run main.py

## Reasoning

This project came about as more of a 'happy accident' - a byproduct of my attempting to generate procedural image of a nebula.

I started off by generating randomized, still images of starfields using PIL. They looked fine for what I had set out to accomplish, but I still felt that the random placement of stars could use some more organic clustering. I figured I had two options; either place the stars randomly but give a higher weight to an area that already has a star in proximity, or place the stars randomly and then move them by applying some kind of directional force.

Placing them by weighted areas would probably have worked and been easier to implement, but I thought that I could learn more from a gravity simulation, and have more fun playing with the variables.

## Todo

- Probably add an argparse menu
- Add options for saving both the finalized still image and an MP4 animation
