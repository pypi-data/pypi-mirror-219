# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, not-callable

from os import PathLike
import requests_html

from akari_dl import src

class Website:
  def __init__(self, name=str, anime=str, output=PathLike, episodes=int, specials=bool, urls=str|tuple, anchors=tuple):

    self.name = name
    self.anime = anime
    self.output_path = output

    self.episodes_count = episodes
    self.specials_enabled = specials

    self.urls = urls # Available URLs to try to connect to requested site
    self.anchors = anchors # Expected anchor elements to scrape href from to go from the search page to the anime page to the video file link.

    self.url = str
    self.endpoint = None
    self.session  = requests_html.HTMLSession()

    # options.add_argument("User-Agent=Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36")


  def resolve_url(self):
    self.url = src.resolve_url(self)


  def resolve_anime(self):
    self.endpoint = src.resolve_anime(self)


  def download_anime(self):
    src.download_anime(self)
