# Development notes

## Run tests

```bash
python -m unittest -v
```

## Run the example

```bash
python git_archaeologist.py /path/to/repository --top 8
```

The tests use deterministic inputs where practical. They check core behavior and
edge handling; they are not a benchmark or a production readiness certification.
