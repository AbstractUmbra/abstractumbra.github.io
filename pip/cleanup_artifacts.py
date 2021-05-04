import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

for file in CURRENT_DIR.glob("*.whl"):
    package_name = file.name.split("-")[0]  # e.g. yarl-1.5.1 == yarl
    move_to = CURRENT_DIR / package_name
    file.rename(move_to / file.name)
