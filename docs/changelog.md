# Changelog

All notable changes to this project will be documented in this file.

## Upcoming Release: [1.2.0]

### Added

- Ability to change leak response actions
- Ability to altar recording interval
- Ability to disable certain sensors (in order to simulate failure)
- More effective message logging

### Changed

- Small modifications to setup.py
- Fixed bug in Yaw function that was introduced in v1.1.0

## Current Release: [1.1.0]

### Added

- Constant Manual Input mode
- More accurate yaw function
- Sitl Mode
- Scripts now wait for queue to end before returning

### Changed

- Fixed lighting
- Tweaked dive safety threshold
- Tweaked dive acceptance threshold
- Fixed waitQueue not releasing semaphore

### Removed

- wait function marked as deprecated

## [1.0.0]

- Initial Release
