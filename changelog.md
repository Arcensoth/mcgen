# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[unreleased]: https://github.com/Arcensoth/mcgen/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/Arcensoth/mcgen/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/Arcensoth/mcgen/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/Arcensoth/mcgen/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Arcensoth/mcgen/releases/tag/v0.1.0
