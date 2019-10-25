import statistics
import math
from collections import Counter
from pathlib import Path

from config.settings.base import PROJECT_ROOT


def load_txt():
    txt_path = Path(PROJECT_ROOT, 'analysis/data/recitatif.txt')
    recitatif = open(txt_path)
    return recitatif

