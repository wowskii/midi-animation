import time
import sys
from pynput.mouse import Controller

with open("horizontal_resolution.txt", "r") as f:
    HORIZONTAL_RESOLUTION = int(f.read())

if len(sys.argv) > 1:
    HORIZONTAL_RESOLUTION = int(sys.argv[1])

# set up mouse
mouse = Controller()

# scroll settings
fps = 30             # how many scrolls per second
duration = 10        # how many seconds to run
steps = int(fps * duration)

time.sleep(5)  # time to switch to target window
# run scrolling loop
for i in range(steps):
    mouse.scroll(HORIZONTAL_RESOLUTION/(24*4), 0)  # (x, y) -> scroll down 1 unit
    time.sleep(1 / fps)
