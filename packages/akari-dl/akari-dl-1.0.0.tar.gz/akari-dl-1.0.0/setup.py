from setuptools import find_packages, setup

setup(
  name="akari-dl",
  version="1.0.0",
  author="keisan",
  author_email="<keisan@skiff.com>",
  description="A lightweight and open-source anime downloading CLI.",
  long_description="akari-dl downloads anime video files from direct download websites based on user configuration to avoid more annoying downloading methods like torrenting and manually downloading.",
  url="https://github.com/keisanng/akari-dl",
  project_urls={
    "Documentation": "https://github.com/keisanng/akari-dl#readme",
    "Tracker": "https://github.com/keisanng/projects/3"
  },
  packages=find_packages(),
  python_requires=">=3.10",
  install_requires=["requests_html"],
  entry_points={"console_scripts":["akari-dl=akari_dl.__main__:main"]}
)
