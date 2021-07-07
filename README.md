# mcgen

Python utilities for downloading and processing Minecraft's generated data.

[![PyPI](https://img.shields.io/pypi/v/mcgen.svg)](https://pypi.org/project/mcgen/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mcgen.svg)](https://pypi.org/project/mcgen/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/arcensoth/mcgen)

## Requirements

- Python 3.8+
- Java 11+ (for invoking the Minecraft server's data generator)

## Installation

```bash
pip install mcgen
```

## Usage

```bash
python -m mcgen --help
```

```
mcgen [-h] [--jarpath JARPATH] [--rawpath RAWPATH] [--outpath OUTPATH] [--version VERSION] [--manifest MANIFEST] [--processors [PROCESSORS [PROCESSORS ...]]] [--log LOG]

Download the Minecraft server jar for the specified version, invoke the data generator, and process the output.

optional arguments:
  -h, --help            show this help message and exit
  --jarpath JARPATH     Where to download and store the server jar. Default: temp/jars/minecraft_server.{version}.jar
  --rawpath RAWPATH     Where to store the raw server-generated files. Default: temp/raw/{version}
  --outpath OUTPATH     Where to write the final processed output. Default: temp/out/{version}
  --version VERSION     The server version to download and process. Defaults to latest snapshot.
  --manifest MANIFEST   Where to fetch the version manifest from. Defaults to Mojang's online copy.
  --processors [PROCESSORS [PROCESSORS ...]]
                        Which processors to use in processing the raw server-generated files. Defaults to a set of built-in processors.
  --log LOG             The level of verbosity at which to print log messages.
```

## Processors

Processors are used to process the raw server-generated data and produce output. They are invoked one after the other, in the order they are defined.

To provide a custom set of processors, use the `--processors` option like so:

```bash
python -m mcgen --processors mcgen.processors.split_registries mcgen.processors.summarize_data
```

### Built-in processors

Several built-in processors are provided in [`mcgen.processors`](./mcgen/processors):

- [`write_version_file`](./mcgen/processors/write_version_file.py) - Write the game version to a file.
- [`convert_json_files`](./mcgen/processors/convert_json_files.py) - Convert json files into another form.
- [`simplify_blocks`](./mcgen/processors/simplify_blocks.py) - Create an optimized summary of blocks.
- [`split_registries`](./mcgen/processors/split_registries.py) - Split `registries.json` into separate files.
- [`summarize_biomes`](./mcgen/processors/summarize_biomes.py) - Create a summary of biome reports.
- [`summarize_data`](./mcgen/processors/summarize_data.py) - Create a summary of each vanilla registry.
- [`create_all_tags_data_pack`](./mcgen/processors/create_all_tags_data_pack.py) - Generate a data pack with "all" tags.

## Custom processors

Processors are Python modules containing a function with the following signature:

```python
def process(ctx: Context, **options):
    ...
```

- `ctx` contains information about the processing context
- `options` is a key-value mapping of arbitrary data
