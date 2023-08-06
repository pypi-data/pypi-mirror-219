"""
  Download an anime based on user-configuration given desired anime is found on desired website.
"""

import os

def download_episodes(self, anime_slug=str, episodes_regular=list):
  """
    Download all (unless specified otherwise) episodes of an anime
    into a folder of the anime's name inside the user-provided output path.
  """
  ep_count = 0

  folder_path = os.path.join(self.output_path, anime_slug)

  for episode in episodes_regular:
    ep_count += 1
    if self.name == "chauthanh":
      self.response = self.session.get(f"{self.url}/anime/{episode.attrs['href'][3:]}", timeout=30)
    else:
      self.response = self.session.get(f"{self.url}{episode.attrs['href']}", timeout=30)
    anchor = self.response.html.find(self.anchors[2], first=True)
    self.endpoint = anchor.attrs["href"]

    file_format = self.endpoint[-3:]

    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    if self.name == "chauthanh":
      self.response = self.session.get(f"{self.url}/anime/download/{self.endpoint[3:]}", timeout=30)
    else:
      self.response = self.session.get(self.endpoint, timeout=30)

    print(f"Downloading episode {ep_count} from {self.endpoint}")
    file_path = os.path.join(folder_path, f"Episode {ep_count}.{file_format}")
    with open(file_path, "wb") as video_file:
      for chunk in self.response.iter_content(1024):
        video_file.write(chunk)
    print(f"Episode {ep_count} downloaded to {file_path}")


def download_specials(self, anime_slug=str, episodes_special=list):
  """
    Download all (unless specified otherwise) episodes of an anime
    into a folder called "specials" inside a folder of the anime's name inside the user-provided output path.
  """
  ep_count = 0

  folder_path = os.path.join(self.output_path, anime_slug, "specials")

  for episode in episodes_special:
    ep_count += 1
    self.response = self.session.get(f"{self.url}{episode.attrs['href']}", timeout=30)
    anchor = self.response.html.find(self.anchors[2], first=True)
    self.endpoint = anchor.attrs["href"]

    file_format = self.endpoint[-3:]

    if not os.path.exists(folder_path):
      os.makedirs(folder_path)

    file_path = os.path.join(folder_path, f"Special {ep_count}.{file_format}")

    self.response = self.session.get(self.endpoint, timeout=30)

    print(f"Downloading special {ep_count} from {self.endpoint}")
    with open(file_path, "wb") as video_file:
      for chunk in self.response.iter_content(1024):
        video_file.write(chunk)
    print(f"Special {ep_count} downloaded to {file_path}.")


def download_anime(self):
  """
    Download user specified anime by scraping links until reaching a video file source.
  """
  self.response = self.session.get(f"{self.url}{self.endpoint}")
  episodes = self.response.html.find(self.anchors[1]) # Episodes anchors

  episodes_regular, episodes_special = [], []

  # Tokyoinsider puts the specials in the same list as the as the regular episodes.
  if self.name == "tokyoinsider":
    episodes.reverse()
    for episode in episodes:
      match episode.find("em", first=True).text:
        case "episode":
          episodes_regular.append(episode)
        case _:
          episodes_special.append(episode)
  else:
    episodes_regular = episodes

  anime_slug = self.anime
  for char in "/><\"\:|?*":
    anime_slug = anime_slug.replace(char, "")

  download_episodes(self, anime_slug, episodes_regular)

  if self.specials_enabled is True:
    download_specials(self, anime_slug, episodes_special)

  return f"Finished downloading {self.anime}."
