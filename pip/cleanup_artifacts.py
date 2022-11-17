import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

for file in CURRENT_DIR.glob("*.whl"):
    package_name = file.name.split("-")[0]  # e.g. yarl-1.5.1 == yarl
    move_to = CURRENT_DIR / package_name
    if not move_to.exists():
        move_to.mkdir(mode=755, exist_ok=True)
    file.rename(move_to / file.name)
