import pathlib

CURRENT_DIR = pathlib.Path(__file__).parent

SPECIAL_CASES: dict[str, str] = {"discord_py": "discord.py", "lru_dict": "lru-dict"}


for file in CURRENT_DIR.glob("*.whl"):
    package_name = file.name.split("-")[0]  # e.g. yarl-1.5.1 == yarl
    special_resolved_name = SPECIAL_CASES.get(package_name)
    if special_resolved_name:
        package_name = special_resolved_name

    print(f"Found {package_name}, preparing to move.")
    move_to = CURRENT_DIR / package_name
    if not move_to.exists():
        print(f"No directory for {move_to} found, creating it now.")
        move_to.absolute().mkdir(mode=0o755, exist_ok=True)

    new_path = move_to / file.name
    print(f"Moving file to {new_path}")
    file.replace(new_path)
else:
    print("No files found to work on.")
