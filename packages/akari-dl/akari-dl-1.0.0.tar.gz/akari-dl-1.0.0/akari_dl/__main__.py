from . import parser, logger
from .src.website import Website

def main():
  args = parser.parse_args()

  if args.debug is True:
    logger.basicConfig(level=logger.NOTSET)

  website = Website(args.website, args.anime, args.output, args.episodes, args.specials, urls=None, anchors=None)

  match args.website.lower():
    case "tokyoinsider":
      website.urls = ("tokyoinsider.com", "tokyoinsider.net", "tokyoinsider.org")
      website.anchors = ("table > tr > .c_h2 > a", ".episode > div > a", ".c_h2 > div > a")
    case "chauthanh":
      website.urls = "chauthanh.info"
      website.anchors = (".boxcontent > p > span > a", "tbody > tr > td > a", ".bd-blue > .p100 > a")
    case _:
      print(f"\033[91m\"{args.website}\" not supported.\033[0m")

  # pylint: disable=no-member
  website.resolve_url()
  website.resolve_anime()
  website.download_anime()

  print("Downloading Complete.")

if __name__ == "__main__":
  main()
