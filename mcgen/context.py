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

    def prepare_filepath(self, file_root: str, ext: str) -> Path:
        # convert the given path into a pathlib path
        file_reldir = Path(file_root)
        # assert that the given path is relative
        assert not file_reldir.is_absolute()
        # convert the path to an absolute path
        file_absdir = self.output_dir / file_root
        # assert that it remains within the output directory
        assert file_absdir.relative_to(self.output_dir)
        # ensure that the path exists and is a directory
        file_absdir.mkdir(parents=True, exist_ok=True)
        # determine the file path with the given extension
        filepath = (file_absdir / "data").with_suffix(ext)
        return filepath

    def write_json(self, data: dict, file_root: str):
        filepath = self.prepare_filepath(file_root, ".json")
        LOG.debug(f"Writing JSON file: {filepath}")
        with open(filepath, "w") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)

    def write_min_json(self, data: dict, file_root: str):
        filepath = self.prepare_filepath(file_root, ".min.json")
        LOG.debug(f"Writing minified JSON file: {filepath}")
        with open(filepath, "w") as fp:
            json.dump(data, fp, separators=(",", ":"), sort_keys=True)

    def write_values_txt(self, values: list, file_root: str):
        filepath = self.prepare_filepath(file_root, ".values.txt")
        LOG.debug(f"Writing values TXT file: {filepath}")
        with open(filepath, "w") as fp:
            fp.write("\n".join(values))

    def write_data(self, data: dict, file_root: str):
        self.write_json(data, file_root)
        self.write_min_json(data, file_root)

    def write_values(self, values: list, file_root: str):
        self.write_values_txt(values, file_root)

    def walk(self, path: Path) -> Iterator[Tuple[str, List[str], List[str]]]:
        for dirpath, dirnames, filenames in os.walk(path):
            dirnames[:] = [d for d in dirnames if d not in self.exclude_dirs]
            yield dirpath, dirnames, filenames
