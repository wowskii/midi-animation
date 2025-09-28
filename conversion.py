import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from midiutil import MIDIFile
from PIL import Image

from utilities import image_to_midi

image_to_midi("images/notre_dame.png", "notre_dame.mid")