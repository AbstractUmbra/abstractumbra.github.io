# -*- coding: utf-8 -*-

import pathlib

import mistune
from jinja2 import Environment, FileSystemLoader, Template


ENVIRONMENT = Environment(
    loader=FileSystemLoader('.')
)

TEMPLATE: Template = ENVIRONMENT.get_template('template.html')

ROOT = pathlib.Path()


if __name__ == "__main__":
    directories = [ROOT] + [p for p in ROOT.glob("**/*") if p.is_dir()]

    for directory in directories:
        paths = list(directory.glob("*"))
        paths.sort(key=lambda p: (not p.is_dir(), p))

        readme = directory / 'README.md'

        if readme.exists():
            # Render the README
            with open(readme, 'r', encoding='utf-8') as fp:
                readme = mistune.markdown(fp.read())
        else:
            readme = None

        with open(directory / "index.html", "w", encoding="utf-8") as fp:
            fp.write(TEMPLATE.render(
                root=(pathlib.Path('/pip') / directory).as_posix(),
                paths=paths,
                readme=readme,
            ))

        print(f"Generated {directory / 'index.html'}")
