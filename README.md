# Git Archaeologist

> Explore a repository's history with a Python analyzer and a local JavaScript dashboard.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-Dashboard-f1e05a.svg?logo=javascript)](https://developer.mozilla.org/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Tests](#-tests)
- [Limitations](#-limitations)
- [License](#-license)

## 🎯 Overview

Git Archaeologist analyzes commit activity and presents the results in the terminal or an offline HTML/CSS/JavaScript dashboard.

## ✨ Features

- Rank file hotspots by commits and changed lines
- Estimate contributor concentration and bus factor
- Summarize activity by weekday and six-hour block
- List stale tracked files
- Export JSON for a local dashboard

## 🧱 Architecture

Python calls the Git executable and aggregates history. The browser dashboard reads the generated JSON locally and renders tables and an activity grid; it needs no server or external JavaScript packages.

See [analysis method](docs/ALGORITHM.md), [architecture](docs/ARCHITECTURE.md), and [input/output notes](docs/INPUTS_AND_OUTPUTS.md).

## 🚀 Quick Start

Requires Python 3.10+ and Git on PATH. From this folder:

```bash
python -m unittest -v
python git_archaeologist.py /path/to/repository --json report.json
```

Then open `dashboard/index.html` and choose `report.json`.

## ✅ Tests

`python -m unittest -v` tests the calculations using a temporary local Git repository.

## ⚠️ Limitations

Author names are not identity verification; bus factor is estimated from changed-line attribution. Rename history is limited, and commit timestamps come from Git metadata. The JSON report includes repository paths and author names, so review it before sharing.

## 📄 License

MIT. See [LICENSE](LICENSE).
