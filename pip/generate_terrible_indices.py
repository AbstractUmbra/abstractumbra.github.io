# -*- coding: utf-8 -*-

import hashlib
import pathlib

import mistune
from jinja2 import Environment, FileSystemLoader, Template


ENVIRONMENT = Environment(
    loader=FileSystemLoader('.')
)

TEMPLATE: Template = ENVIRONMENT.get_template('template.html')

FILETYPE_ICONS = {
    '.whl': 'settings_applications'
}

ENVIRONMENT.globals.update(
    FILETYPE_ICONS=FILETYPE_ICONS
)

ROOT = pathlib.Path()


if __name__ == "__main__":
    directories = [ROOT] + [p for p in ROOT.glob("**/*") if p.is_dir()]

    for directory in directories:
        paths = list(directory.glob("*"))
        paths.sort(key=lambda p: (not p.is_dir(), p))

        # Generate sha256s
        sha256s = {}
        for path in paths:
            if path.is_file():
                with open(path, 'rb') as fp:
                    sha256s[path] = hashlib.sha256(fp.read()).hexdigest()

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
                sha256s=sha256s,
                readme=readme,
            ))

        print(f"Generated {directory / 'index.html'}")
