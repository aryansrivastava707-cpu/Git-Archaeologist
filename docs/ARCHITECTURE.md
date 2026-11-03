# Architecture

`git_archaeologist.py` calls the local Git executable and produces terminal output plus JSON report data. The offline page in `dashboard/` uses HTML, CSS, and JavaScript to render a report selected by the user. It makes no network requests and modifies no analyzed repository.

## Main workflow

```bash
python git_archaeologist.py /path/to/repository --top 8 --json report.json
```

Open `dashboard/index.html` and choose the generated JSON file.
