# -*- coding: utf-8 -*-

import pathlib


INDEX_FORMAT = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Directory listing for {0}</title>
    </head>
    <body>
        <h1>Directory listing for {0}</h1>
        <hr>
        <ul>
{1}
        </ul>
        <hr>
    </body>
</html>
"""

LINK_FORMAT = """            <li><a href="{0}">{1}</a></li>"""

ROOT = pathlib.Path()

def web_location(path: pathlib.Path):
    relative = pathlib.Path('pip') / path
    return f"https://gorialis.github.io/{relative.as_posix()}"


if __name__ == "__main__":
    directories = [ROOT] + [p for p in ROOT.glob("**/*") if p.is_dir()]

    for directory in directories:
        index_elements = "\n".join(
            LINK_FORMAT.format(web_location(path), path.parts[-1])
            for path in directory.glob("*")
        )

        with open(directory / "index.html", "w", encoding="utf-8") as fp:
            fp.write(INDEX_FORMAT.format(
                (pathlib.Path('/pip') / directory).as_posix(),
                index_elements
            ))
