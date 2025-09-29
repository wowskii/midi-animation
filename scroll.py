import time
from pynput.mouse import Controller

# set up mouse
mouse = Controller()

# scroll settings
fps = 30             # how many scrolls per second
duration = 200        # how many seconds to run
steps = int(fps * duration)

time.sleep(5)  # time to switch to target window
# run scrolling loop
for i in range(steps):
    mouse.scroll(20, 0)  # (x, y) -> scroll down 1 unit
    time.sleep(1 / fps)
