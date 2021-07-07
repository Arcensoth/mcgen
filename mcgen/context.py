import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Tuple

LOG = logging.getLogger(__name__)


@dataclass
class Context:
    input_dir: Path
    output_dir: Path
    version: str
    exclude_dirs: Tuple[str, ...] = (".cache", "tmp")

    def resolve_path(self, relpath: Path) -> Path:
        # assert that the given path is relative
        assert not relpath.is_absolute()
        # convert it to an absolute path
        abspath = (self.output_dir / relpath).resolve()
        # assert that it remains within the output directory
        assert abspath.relative_to(self.output_dir)
        # return the final, resolved path
        return abspath

    def prepare_file_path(self, path: Path) -> Path:
        # resolve the given path
        abspath = self.resolve_path(path)
        # create the containing directory, if it does not already exist
        abspath.parent.mkdir(parents=True, exist_ok=True)
        # return the file path
        return abspath

    def write_json_file(self, data: dict, path: Path):
        file_path = self.prepare_file_path(path)
        LOG.debug(f"Writing JSON file: {file_path}")
        with open(file_path, "w") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)

    def prepare_node_path(self, path: Path, name: str) -> Path:
        # resolve the given path
        abspath = self.resolve_path(path)
        # create the node directory, if it does not already exist
        abspath.mkdir(parents=True, exist_ok=True)
        # return the final file path with the given name
        file_path = abspath / name
        return file_path

    def write_json_node(self, data: dict, path: Path, name="data.json"):
        filepath = self.prepare_node_path(path, name)
        LOG.debug(f"Writing JSON file: {filepath}")
        with open(filepath, "w") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)

    def write_min_json_node(self, data: dict, path: Path, name="data.min.json"):
        filepath = self.prepare_node_path(path, name)
        LOG.debug(f"Writing minified JSON file: {filepath}")
        with open(filepath, "w") as fp:
            json.dump(data, fp, separators=(",", ":"), sort_keys=True)

    def write_values_txt_node(self, values: list, path: Path, name="data.values.txt"):
        filepath = self.prepare_node_path(path, name)
        LOG.debug(f"Writing values TXT file: {filepath}")
        with open(filepath, "w") as fp:
            fp.write("\n".join(values))

    def walk(self, path: Path) -> Iterator[Tuple[str, List[str], List[str]]]:
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = [d for d in dirnames if d not in self.exclude_dirs]
            yield dirpath, dirnames, filenames
