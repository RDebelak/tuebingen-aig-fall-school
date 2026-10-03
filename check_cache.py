"""Why does OFFLINE mode report "not in cache"? Run this in the folder that holds the notebooks and cache/:

    python check_cache.py

It checks (1) that cache/ is there and populated, (2) that the hash scheme reproduces the file names,
(3) that the model IDs in the cache match the notebooks' setup cells, (4) whether the first call of each
notebook is cached, and prints a verdict.
"""
import json, hashlib, re, sys
from pathlib import Path
from collections import Counter

here = Path(".").resolve()
cache = here / "cache"
notebooks = sorted(here.glob("fallschool_0*.ipynb"))
FIRST_CALLS = {"fallschool_01": "Write four multiple-choice questions",
               "fallschool_02": "Write a reading passage in English for learners at CEFR level B1",
               "fallschool_03": "Judge only the correct answer of this question",
               "fallschool_04": "Passage:\n"}
problems = []

print(f"folder: {here}")
print(f"notebooks found: {[p.name for p in notebooks] or 'NONE'}")
if not notebooks:
    problems.append("no fallschool_0*.ipynb here - run this script inside the folder with the notebooks")

# ---- 1. the cache folder
files = sorted(cache.glob("*.json")) if cache.exists() else []
print(f"cache/: {'exists' if cache.exists() else 'MISSING'}, {len(files)} .json files")
if not cache.exists():
    problems.append("cache/ is not next to the notebooks: the notebooks create an empty cache/ and every call misses")
elif len(files) < 100:
    problems.append(f"cache/ holds only {len(files)} files; the reference run has ~250 (GitHub's web upload takes 100 files per upload)")
for extra in ["day1_items.json", "day2_screened_items.json", "day1_predictions.json"]:
    print(f"{extra}: {'present' if (here / extra).exists() else 'MISSING'}")

# ---- 2. hash scheme and models in the cache
entries, bad_hash, models, temps = [], 0, Counter(), Counter()
for f in files:
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        p = d["payload"]
    except (ValueError, KeyError, OSError):
        continue
    key = hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()[:24]
    if key != f.stem:
        bad_hash += 1
    entries.append(p); models[p.get("model")] += 1; temps[p.get("temperature")] += 1
if files:
    print(f"hash check: {len(entries) - bad_hash}/{len(entries)} file names reproduce from their payload"
          + ("" if bad_hash == 0 else f"  ({bad_hash} retried calls store the retry's payload under the original name - normal)"
             if bad_hash < 0.1 * len(entries) else "  <- most files were produced with a different hashing, i.e. different notebooks"))
    print(f"models in cache: {dict(models)}")

# ---- 3. model IDs in the notebooks
nb_models = {}
for p in notebooks:
    src = "".join("".join(c["source"]) for c in json.load(open(p, encoding="utf-8"))["cells"] if c["cell_type"] == "code")
    m = {k: re.search(rf'{k}\s*=\s*"([^"]+)"', src) for k in ("TEXT_MODEL", "ITEM_MODEL")}
    nb_models[p.name] = {k: (v.group(1) if v else None) for k, v in m.items()}
    off = re.search(r"OFFLINE\s*=\s*(True|False)", src)
    print(f"{p.name}: TEXT_MODEL={nb_models[p.name]['TEXT_MODEL']}  ITEM_MODEL={nb_models[p.name]['ITEM_MODEL']}  OFFLINE={off.group(1) if off else '?'}")
if files and notebooks:
    wanted = {v for d in nb_models.values() for v in d.values() if v}
    if not wanted & set(models):
        problems.append(f"model IDs differ: notebooks use {sorted(wanted)}, the cache was produced with {sorted(models)} "
                        "- the notebooks in this folder are not the versions that made the cache")

# ---- 4. is each notebook's first call in the cache?
for stem, prefix in FIRST_CALLS.items():
    hits = [p for p in entries if p["messages"][-1]["content"].startswith(prefix)]
    if hits:
        p = hits[0]
        print(f"{stem}: first prompt cached ({len(hits)} match{'es' if len(hits) > 1 else ''}; model {p['model']}, "
              f"temperature {p['temperature']}, seed {p.get('seed')}, system prompt starts {p['messages'][0]['content'][:50]!r})")
    elif entries:
        print(f"{stem}: first prompt NOT in cache")
        problems.append(f"{stem}: no cached call starts with {prefix[:40]!r} - the cache is from a run with different prompts")

# ---- 5. are all calls of a standard run there? (default settings; re-asks and rewrites add calls, never remove them)
EXPECTED = {"fallschool_01": [("Write four multiple-choice questions", 1), ("Write 1 question(s)", 4), ("Write 3 wrong answer options", 4)],
            "fallschool_02": [("Write a reading passage", 3), ("Which CEFR level", 3), ("Write 3 question(s)", 12), ("Rate each question-answer pair", 12),
                              ("Write 6 wrong answer options", 10), ("Choose the 3 best distractors", 10), ("Explain in two sentences", 10),
                              ("Rewrite this maths question", 10)],
            "fallschool_03": [("Judge only the correct answer", 10), ("Give two scores", 10), ("For each wrong option", 10)],
            "fallschool_04": [("Passage:", 60), ("Questions:", 20)]}
if entries:
    for stem, checks in EXPECTED.items():
        short = []
        for prefix, n in checks:
            found = sum(p["messages"][-1]["content"].startswith(prefix) for p in entries)
            if found < n:
                short.append(f"{prefix[:28]!r}: {found}/{n}")
        print(f"{stem}: {'all standard calls present' if not short else 'short: ' + ', '.join(short)}")
        hard = [x for x in short if not x.startswith("'Rate each")]      # a group emptied by the rule check is never rated
        if hard:
            problems.append(f"{stem}: fewer cached calls than a standard run makes ({'; '.join(hard)}) - files were probably lost "
                            "in a batched web upload; re-upload the complete cache/ with GitHub Desktop or git")
        elif short:
            print(f"   (fewer rating calls than groups is normal when the rule check empties a group; not an error)")

print("\nverdict:")
if problems:
    for x in problems:
        print(" -", x)
else:
    print(" - cache, models and first prompts all match. If a notebook still misses, its kernel is not running in this folder:",
          "start `jupyter lab` from here (VS Code: set jupyter.notebookFileRoot to ${fileDirname}), or the notebook was edited.")
