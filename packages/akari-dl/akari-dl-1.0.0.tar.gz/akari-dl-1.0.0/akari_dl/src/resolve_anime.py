def resolve_anime(self):
  """
    Verify user-specified anime exists on user-specified website via resolved url
    and return the link of the first entry of the anime's name on the website.
  """
  print(f"Searching for \"{self.anime}\"...")

  match self.name.lower():
    case "tokyoinsider":
      self.response = self.session.get(f"{self.url}/anime/search?k={self.anime}", timeout=30)
    case "chauthanh":
      self.response = self.session.get(f"{self.url}/search/?s={self.anime}", timeout=30)

  try:
    anchor = self.response.html.find(self.anchors[0], first=True)
    print("Anime found.")
  except Exception:
    print("Anime not found.")
    exit()

  return anchor.attrs["href"]
