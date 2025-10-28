import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

SPECIAL_CASES: dict[str, str] = {"discord_py": "discord.py", "lru_dict": "lru-dict"}


def resolve_filename(name: str) -> str:
    split_name = name.split("-")[0]  # e.g. yarl-1.5.1 == yarl
    resolved = SPECIAL_CASES.get(split_name)
    if not resolved:
        return name

    return name.replace(split_name, resolved, 1)


for file in CURRENT_DIR.glob("*.whl"):
    package_name = file.name.split("-")[0]  # e.g. yarl-1.5.1 == yarl
    package_name = SPECIAL_CASES.get(package_name, package_name)

    print(f"Found {package_name}, preparing to move.")
    move_to = CURRENT_DIR / package_name
    if not move_to.exists():
        print(f"No directory for {move_to} found, creating it now.")
        move_to.absolute().mkdir(mode=0o755, exist_ok=True)

    filename = resolve_filename(file.name)
    new_path = move_to / filename
    print(f"Moving file to {new_path}")
    file.replace(new_path)
else:
    print("No files found to work on.")
