# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2022-06-21

### Changed

- Updated the default URL for the version manifest.

## [0.7.0] - 2021-11-11

### Changed

- Generalized the `summarize_biomes` processor to a full-blown `summarize_worldgen` (similar to how `summarize_data` works)
- Changed the default value of `--cmd` to use the `java` command for 21w39a onward

## [0.6.0] - 2021-09-30

### Added

- New CLI option `--cmd` to pass a custom command to invoke the data generator with (to support changes from 21w39a onward)

## [0.5.0] - 2021-07-07

### Added

- Added a `create_all_tags_data_pack` processor that generates a data pack with "all" tags.
  - The data pack contains an `#mcdata:all` tag for each type of supported registry:
    - `minecraft:block` -> `tags/blocks`
    - `minecraft:entity_type` -> `tags/entity_types`
    - `minecraft:fluid` -> `tags/fluids`
    - `minecraft:game_event` -> `tags/game_events`
    - `minecraft:item` -> `tags/items`
  - The data pack is generated under a new top-level `datapacks` directory

## [0.4.0] - 2021-06-18

### Added

- Added missing `simplify_blocks` processor

## [0.3.0] - 2021-06-18

### Changed

- Made the file structure more flexible
  - Paths are now formatted with the resolved version
  - Adjusted CLI argument names to reflect this change

## [0.2.0] - 2021-06-18

### Changed

- Adjusted CLI defaults

## [0.1.0] - 2021-04-08

### Added

- Initial implementation

[unreleased]: https://github.com/Arcensoth/mcgen/compare/v0.8.0...HEAD
[0.8.0]: https://github.com/Arcensoth/mcgen/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/Arcensoth/mcgen/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/Arcensoth/mcgen/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/Arcensoth/mcgen/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/Arcensoth/mcgen/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Arcensoth/mcgen/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Arcensoth/mcgen/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Arcensoth/mcgen/releases/tag/v0.1.0
