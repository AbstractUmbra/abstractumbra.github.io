import pathlib

from packaging.utils import parse_wheel_filename

CURRENT_DIR = pathlib.Path(__file__).parent


for file in CURRENT_DIR.glob("*.whl"):
    name, version, build, tags = parse_wheel_filename(file.name)

    print(f"Found {name}, preparing to move.")
    move_to = CURRENT_DIR / name
    if not move_to.exists():
        print(f"No directory for {move_to} found, creating it now.")
        move_to.absolute().mkdir(mode=0o755, exist_ok=True)

    new_path = move_to / file.name
    print(f"Moving file to {new_path}")
    file.replace(new_path)
