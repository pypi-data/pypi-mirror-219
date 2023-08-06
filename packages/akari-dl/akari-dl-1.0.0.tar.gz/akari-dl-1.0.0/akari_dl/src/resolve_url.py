def resolve_url(self):
  """
    Resolve working url for user-specified website.
  """
  print(f"Connecting to {self.name}...")

  if isinstance(self.urls, tuple):
    i = 0
    connected = False
    for url in self.urls:
      try:
        while not connected:
          i += 1
          self.response = self.session.get(f"https://{url}")
          if self.response.status_code == 200:
            connected = True
      except Exception:
        try:
          print(f"Failed to connect to {self.name} via https://{url}... trying https://{self.urls[i]}.")
        except IndexError:
          print(f"Failed to connect to {self.name}.")
          exit()
  else:
    try:
      self.response = self.session.get(f"https://{self.urls}")
    except Exception:
      print(f"Failed to connect to {self.name}.")
      exit()

  print(f"Connected to {self.response.url[:-1]}.")
  return self.response.url[:-1]
