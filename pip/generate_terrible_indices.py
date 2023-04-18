# -*- coding: utf-8 -*-

import hashlib
import pathlib

import mistune
from jinja2 import Environment, FileSystemLoader, Template

ENVIRONMENT = Environment(loader=FileSystemLoader("."))

TEMPLATE: Template = ENVIRONMENT.get_template("template.html")

FILETYPE_ICONS = {".whl": "settings_applications"}

ENVIRONMENT.globals.update(
    Path=pathlib.Path,
    FILETYPE_ICONS=FILETYPE_ICONS,
)

ROOT = pathlib.Path()


if __name__ == "__main__":
    directories = [ROOT] + [p for p in ROOT.glob("**/*") if p.is_dir()]

    for directory in directories:
        paths = list(directory.glob("*"))
        paths.sort(key=lambda p: (not p.is_dir(), p))

        # Generate sha256s
        sha256s: dict[pathlib.Path, str] = {}
        for path in paths:
            if path.is_file():
                with open(path, "rb") as fp:
                    sha256s[path] = hashlib.sha256(fp.read()).hexdigest()

        readme_file = directory / "README.md"

        if readme_file.exists():
            # Render the README
            with readme_file.open("r", encoding="utf-8") as fp:
                readme: str | None = mistune.markdown(fp.read())
        else:
            readme = None

        with open(directory / "index.html", "w", encoding="utf-8") as fp:
            fp.write(
                TEMPLATE.render(
                    root=directory,
                    paths=paths,
                    sha256s=sha256s,
                    readme=readme,
                )
            )

        print(f"Generated {directory / 'index.html'}")
