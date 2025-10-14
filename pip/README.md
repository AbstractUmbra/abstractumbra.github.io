This is a custom pip index.

Read more about how this works [here](https://packaging.python.org/guides/hosting-your-own-index/).

The pages for the index are generated using a custom script Gorialis made that templates using Jinja2. You can see the source [on the repository](https://github.com/AbstractUmbra/abstractumbra.github.io/tree/main/pip).

Gorialis styled the page originally based on how Apache automatically generates its directory indices, but they softened it up to make it a bit easier on the eyes, without adjusting the key components that allow pip to detect the packages from it.

To allow pip to download from this index, you can use the `--extra-index-url` flag, e.g.:

```bash
pip install discord.py[voice] --extra-index-url https://abstractumbra.github.io/pip/
```

### Using uv

You can also set this repository as a source in `uv`, either via the cli:
```bash
uv add discord.py[voice,speed] --extra-index-url https://abstractumbra.github.io/pip/
```
Or within your `pyproject.toml` file:

```toml
[[tool.uv.index]]
name = "umbra"
url = "https://about.abstractumbra.dev/pip/"
```

Specifying this index will add it as an extra index url as with the CLI for all uv operations. See the [documentation on that](https://docs.astral.sh/uv/concepts/indexes/) for more info.
