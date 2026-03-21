# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-XX-XX

### Changed

- **Python 3.12+**: Minimum Python version is now 3.12 (was 3.14)
- **Tests on 3.12, 3.13, 3.14**: CI now tests on all three Python versions
- **Dependency bounds**: Added upper version constraints for stability

### Fixed

- Version string mismatch in `__init__.py`

### Removed

- Unused `retry_on_status` configuration field

## [0.2.0] - 2024-03-21

### Added

- Async client with full async support
- Auto-pagination with `async for`
- Webhook delivery logs support
- Comprehensive test suite
- GitHub Actions CI/CD

### Changed

- Python 3.14+ required

## [0.1.0] - 2024-03-20

### Added

- Initial release
- Sync client
- Accounts, Transactions, Categories, Tags, Attachments, Webhooks API
- Pagination support
- Pydantic models
- Retry logic with tenacity
