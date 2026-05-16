# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.1.0] - 2026-05-16

### Features

- feat(ci): add mypy type checking and automated release pipeline (8447c91)
- feat: .python-version file added (61033cf)
- feat: added new test step in CI (eb3f838)
- feat: added ci lint - ruff - audit - build (47c7acb)
- feat: remove loggers info (3641c53)
- feat: better readme (f5bb8c6)
- feat: new pip audit - new requirements.dev.txt - better utils names (d388274)
- feat: better structure by tkinter template (98ea7e0)
- feat: re-organize files (a290c61)
- feat: better structure tkinter project (bcbedc4)
- feat: better exports - new build system and pre-commit added (54ac28f)
- feat: better code and tests added (dac6226)

### Bug fixes

- fix: ImportError: libportaudio.so.2 in ci.yml (986991d)
- fix: redirect egg-info to project root to prevent it from being generated inside src/ (f86f4c8)
- fix: The test job now installs portaudio19-dev (alongside Tkinter/xvfb) before pip install -e '.[test]', so PyAudio can find libportaudio.so.2 at both compile time and runtime. (9d86179)
- fix: Added the missing portaudio19-dev install step to lint-and-audit — it was already present in the build job but had been omitted from the lint job, which also needs it to compile PyAudio when installing [dev] extras. (ad58861)
- fix: PyAudio is a C extension that wraps PortAudio, so it needs the portaudio19-dev system package (which provides portaudio.h) available before pip can compile it. The new step installs that library via apt-get before the pip install -e '.[build]' step. (90d5c64)
- fix: fix vulnerabilities (1ab5f06)
- fix: better tests (9607817)
- fix: title app (4ea23cb)
- fix: better repository name/description and better system test (a75decf)
- fix: remove migrations exclude in pre commit config and update requirements dev (68e6e51)
- fix: better audio model (1a0cba9)
- fix: better constants (42e2401)
- fix: new messages.py (8a88083)
- fix: fix build exe with nex config app.spec (cb2fea4)
- fix: cant start record audio if filename not exists with tests changed (cbe0ed5)
- fix: fix import names (2d04e87)
- fix: fix import names (93cd1d6)

### Refactors

- refactor: replace pip install -r with pip install -e for build deps (f7d9468)
- refactor: migrate deps to pyproject.toml and update README. (e0ea6b4)
- refactor: test suite to align with project testing standards and structure standars (877e8e8)

### Documentation

- docs: simplify production env setup to use .env directly (861b165)

### Build & CI

- ci: run lint-and-audit, test, and build sequentially (19978f3)

### Uncategorized

- patch: readme updated (0c3bb18)
- patch: pyproject.toml update description (5207045)
- patch: readme updated (bd9e297)
- patch: readme updated (dd066fb)
- Update README.md (25f7ae4)
- New structure of project with types (ef8eeca)
- Update README.md (38ad5d9)
- fix link (f333d10)
- new readme (3f6748e)
- Update README.md (f64c627)
- Update README.md (b91e90e)
- New readme (9689688)
- New repository! (6842e7f)
- Initial commit (8a1b59c)

