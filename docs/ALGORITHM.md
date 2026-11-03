# Analysis method

Git supplies commit metadata and per-file line deltas. The analyzer aggregates
touches and churn by path, attributes those line deltas to author names, buckets
commits by weekday and six-hour block, then compares tracked paths with their
latest observed commit. It skips merge commits and binary files where Git emits no
line counts. These are descriptive heuristics; author aliases are not merged.
