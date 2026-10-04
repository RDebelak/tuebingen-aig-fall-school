# Automated Item Generation with Large Language Models — Fall School, University of Tübingen

Materials for the two-day fall school (6–7 October 2026, University of Tübingen) by Rudolf Debelak (EPFL) and
Rasmus Jensen (ETH Zurich / IBE). Four Jupyter notebooks take you from a naive prompt to an item bank with
psychometric evidence: generation, screening, difficulty prediction, and artificial test-takers.

## What is in this repository

| File | Used | What it does |
|---|---|---|
| `fallschool_01_naive_vs_framework.ipynb` | Day 1, morning | A naive prompt versus the framework's prompts on one passage — you judge the items |
| `fallschool_02_mini_pipeline.ipynb` | Day 1, afternoon | Passages → questions → LLM rating and revision → distractors → 10 reading + 10 maths items (`day1_items.json`) |
| `fallschool_03_screening_and_prediction.ipynb` | Day 2, morning | Part A: rule and LLM checks on the items (`day2_screened_items.json`); Part B: a difficulty predictor trained on CMCQRD, applied to the items (`day1_predictions.json`) |
| `fallschool_04_artificial_test_takers.ipynb` | Day 2, afternoon | Artificial test-takers (persona prompt × model size) answer the items; classical statistics, IRT, distractor analysis, predicted vs. empirical difficulty (`day2_analysis.json`) |
| `cache/`, `day1_items.json`, `day2_screened_items.json`, `day1_predictions.json` | every run | The instructors' reference run. Every LLM call the notebooks make is stored here, so the notebooks run **without** any model endpoint (see "Offline mode") |
| `reference/*.html` | read-only | The instructors' run of each notebook with all outputs, to read along or compare |
| `check_cache.py` | setup | One-command check that notebooks and cache fit together |
| `slides_pdf/` | | Slide PDFs, added the evening before each day |
| `requirements.txt` | setup | Python packages |

The notebooks run in order: each one reads the file the previous one wrote (next to the notebooks).

## How the notebooks are run in the course

The language models behind the notebooks run on an EPFL cluster that is reachable only from inside the EPFL network,
so in Tübingen the notebooks run in **offline mode**: every call is replayed from `cache/`, and you see exactly the
outputs the instructors obtained. Nothing to configure, no key, no waiting for models. The instructors run the same
notebooks live on the projector; when you want to try a different prompt, rubric or setting, say so and we run it
together and compare.

If you have access to an OpenAI-compatible endpoint of your own (now or after the course), the notebooks make real
calls instead: leave `OFFLINE = False`, set the two environment variables before starting Jupyter, and put your
model names into `TEXT_MODEL`, `ITEM_MODEL` and (Notebook 4) `TAKER_MODELS` in the setup cell:

```bash
export AIG_BASE_URL="https://.../v1"        # Windows PowerShell: $env:AIG_BASE_URL="https://.../v1"
export AIG_API_KEY="..."                    #                     $env:AIG_API_KEY="..."
jupyter lab
```

## Before you arrive (about 20 minutes, please do this at home)

1. **Python 3.12.** Install from https://www.python.org/downloads/ (macOS: afterwards double-click
   *Install Certificates.command* in the folder */Applications/Python 3.12*). Python 3.10 or 3.11 also works.
2. **Get the materials.** Green *Code* button above → *Download ZIP*, unzip; or `git clone` this repository.
3. **Install the packages** in a virtual environment. In a terminal, inside the unzipped folder:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt    # ~2 GB (includes PyTorch); use a good connection
   ```
4. **Download the CMCQRD data set** (Day 2, Notebook 3 Part B). The Cambridge Multiple-Choice Questions Reading Dataset
   (Mullooly et al., 2023, documentation: https://doi.org/10.17863/CAM.102185) is available from Cambridge University
   Press & Assessment after accepting their licence: [link to the download page]. Save the file as `CMCQRD.jsonl`
   in the same folder as the notebooks. We cannot redistribute it, so please do this before Day 2.
5. **Check your setup.** In the same terminal, `python check_cache.py` should end with
   *cache, models and first prompts all match*. Then run `jupyter lab`, open Notebook 1, set `OFFLINE = True` in the
   setup cell (the third cell) and run all cells; it finishes in a few seconds. Do the same for the other three
   notebooks when you open them in the course.

## Good to know

**Models.** In the reference run, passages were written by `swiss-ai/Apertus-v1.5-70B`; questions, distractors and
all judgements come from `Qwen/Qwen3-30B-A3B-Instruct-2507`. The artificial test-takers in Notebook 4 are Qwen3 models
of increasing size — 0.6B, 1.7B, 4B, 8B and 30B parameters — one per ability level, each with a persona prompt: a
prompt alone does not make a strong model a weak reader, so model size stands in for ability.

**Caching.** Every call is stored in `cache/` under a key made from the complete request (model, prompt, settings).
A repeated call is answered from disk; a changed prompt is a new call. With an endpoint, re-running a cell is free
and only your edits cost new calls; different seeds (`SEED` in Notebook 2) give different passages and items.

**Offline mode** (`OFFLINE = True`) replays the reference run and raises an error for any call that is not in the
cache. That is by design: it tells you that your notebook differs from the reference version — an edited prompt,
seed or setting — which needs an endpoint to run.

## Schedule

| | Morning (9:15–12:00) | Afternoon (13:00–16:00) |
|---|---|---|
| Day 1 | Framework, item writing with LLMs; **Notebook 1** at the end | Building the generation stage; **Notebook 2** |
| Day 2 | Evaluation: screening and difficulty prediction; **Notebook 3** | Artificial test-takers and validation; **Notebook 4** |

## Troubleshooting

- *`OFFLINE and not in cache: ...`*: the notebook differs from the reference version, or `cache/` is not next to the
  notebook. Start Jupyter from the folder that holds the notebooks and `cache/`, use the unmodified notebooks, and run
  `python check_cache.py` there to see what differs.
- *`... not found — run Notebook N first`*: the notebook needs the file written by the previous one. Run that
  notebook, or copy the reference file of the same name from this repository next to the notebooks.
- *externally-managed-environment* when installing: you are not inside the virtual environment — run
  `source .venv/bin/activate` first.
- *SSL: CERTIFICATE_VERIFY_FAILED* on macOS: run *Install Certificates.command* (step 1).
- With an endpoint: the first call to a model can take up to two minutes while the model wakes up; later calls take
  seconds. A cell that fails with a JSON or schema error can simply be run again — the notebook retries with a
  stricter prompt, and nothing else is recomputed.

## Licence and citation

Notebooks and this text: MIT licence. The framework and the pipeline follow Rasmus Jensen's master's thesis and
semester project at ETH Zurich (Jensen, 2025, 2026). CMCQRD: Mullooly, A., et al. (2023), *The Cambridge Multiple-Choice Questions Reading
Dataset*, Cambridge University Press & Assessment — subject to its own licence, not part of this repository.
Questions: rudolf.debelak@epfl.ch.
