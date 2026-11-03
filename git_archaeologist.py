#!/usr/bin/env python3
"""git-archaeologist: dig through a git repository's history.

Reports: hotspot files, bus factor, when the team actually works, and files
nobody has touched for a long time. Standard library only; needs `git` on PATH.
"""
import argparse
import collections
import datetime as dt
import subprocess
import sys

SEP = "\x1f"


def run_git(repo, *args):
    result = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit("git error: " + (result.stderr.strip() or "unknown"))
    return result.stdout


def load_commits(repo):
    """Return commits (newest first) as dicts with author, time, {file: lines_changed}."""
    out = run_git(repo, "log", "--no-merges", "--numstat",
                  f"--format=@@{SEP}%H{SEP}%an{SEP}%at")
    commits, current = [], None
    for line in out.splitlines():
        if line.startswith("@@"):
            _, sha, author, ts = line.split(SEP)
            current = {"sha": sha, "author": author,
                       "time": dt.datetime.fromtimestamp(int(ts)), "files": {}}
            commits.append(current)
        elif line.strip() and current is not None:
            added, deleted, path = line.split("\t", 2)
            if added == "-":  # binary file, no line counts
                continue
            current["files"][path] = int(added) + int(deleted)
    return commits


def hotspots(commits, top):
    touches, churn = collections.Counter(), collections.Counter()
    for c in commits:
        for path, lines in c["files"].items():
            touches[path] += 1
            churn[path] += lines
    # score = commits * log-ish churn weight, kept simple: rank by commits then churn
    ranked = sorted(touches, key=lambda p: (touches[p], churn[p]), reverse=True)
    return [(p, touches[p], churn[p]) for p in ranked[:top]]


def bus_factor(commits):
    """Smallest number of authors who together account for >50% of changed lines."""
    per_author = collections.Counter()
    for c in commits:
        per_author[c["author"]] += sum(c["files"].values())
    total = sum(per_author.values())
    if total == 0:
        return 0, per_author, 0
    running, count = 0, 0
    for _, lines in per_author.most_common():
        running += lines
        count += 1
        if running / total > 0.5:
            break
    return count, per_author, total


def work_rhythm(commits):
    """Grid[weekday][block] with 4 six-hour blocks."""
    grid = [[0] * 4 for _ in range(7)]
    for c in commits:
        grid[c["time"].weekday()][c["time"].hour // 6] += 1
    return grid


def stale_files(repo, commits, top):
    """Currently tracked files ordered by how long ago they were last changed."""
    last_touch = {}
    for c in commits:  # newest first, so first sighting is the latest change
        for path in c["files"]:
            last_touch.setdefault(path, c["time"])
    now = dt.datetime.now()
    tracked = run_git(repo, "ls-files").splitlines()
    rows = [(p, (now - last_touch[p]).days) for p in tracked if p in last_touch]
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows[:top]


def render(repo, top):
    commits = load_commits(repo)
    if not commits:
        sys.exit("No commits found.")
    lines = [f"Repository: {repo}",
             f"Commits (non-merge): {len(commits)}   "
             f"Span: {commits[-1]['time']:%Y-%m-%d} -> {commits[0]['time']:%Y-%m-%d}", ""]

    lines.append(f"Hotspots (most-changed files, top {top})")
    for path, n, churn in hotspots(commits, top):
        lines.append(f"  {n:>4} commits  {churn:>6} lines  {path}")

    bf, per_author, total = bus_factor(commits)
    lines += ["", f"Bus factor: {bf}  (authors needed to cover >50% of {total} changed lines)"]
    for author, n in per_author.most_common(5):
        share = 100 * n / total if total else 0
        lines.append(f"  {share:5.1f}%  {author}")

    lines += ["", "Work rhythm (commits)      00-06 06-12 12-18 18-24"]
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    grid = work_rhythm(commits)
    peak = max(max(row) for row in grid) or 1
    shades = " .:*#"
    for day, row in zip(days, grid):
        cells = "".join(f"  {shades[min(4, round(4 * v / peak))]}{v:<3}" for v in row)
        lines.append(f"  {day}                      {cells}")

    lines += ["", f"Longest untouched files (days since last change, top {top})"]
    for path, age in stale_files(repo, commits, top):
        lines.append(f"  {age:>5} days  {path}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Dig through a git repo's history.")
    parser.add_argument("repo", nargs="?", default=".", help="path to a git repository")
    parser.add_argument("--top", type=int, default=8, help="rows per section")
    args = parser.parse_args()
    print(render(args.repo, args.top))


if __name__ == "__main__":
    main()
