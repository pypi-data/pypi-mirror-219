"""
akari-dl
--------
A lightweight and open-source anime downloading CLI.

https://github.com/keisanng/akari-dl
"""

import logging
import argparse
from sys import version_info

if not version_info[0] >= 3 and not version_info[1] >= 10:
  print("You must use Python 3.10 or above.")
  exit()

parser = argparse.ArgumentParser(prog="akari_dl")

parser.add_argument("website", type=str, help="Specify the name of what website to direct-download anime from (see supported websites: https://github.com/keisanng/akari-dl#supported-websites.)")
parser.add_argument("anime", type=str, help="Specify what anime to download by title (in Romaji {https://en.wikipedia.org/wiki/Romanization_of_Japanese}.)")
parser.add_argument("output", type=str, help="Specify path to output downloaded video files to.")
parser.add_argument("-e", "--episodes", type=int, help="Specify the amount of episodes to download (downloads all if not specified) [NOT YET IMPLEMENTED.]")
parser.add_argument("-s", "--specials", action="store_true", help="Enable downloading of special episodes.")
parser.add_argument("-d", "--debug", action="store_true", help="Enable logging module for debugging.")
parser.add_argument("-v", "--version", action="version", version="1.0.0", help="Print the current version of akari-dl.")

logger = logging
