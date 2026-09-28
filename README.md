# Automated Item Generation with Large Language Models — Fall School, University of Tübingen

Materials for the two-day fall school ([dates], University of Tübingen) by Rudolf Debelak (EPFL / University of
Zurich) and Rasmus Jensen ([affiliation]). Four Jupyter notebooks take you from a naive prompt to an item bank with
psychometric evidence: generation, screening, difficulty prediction, and artificial test-takers.

## What is in this repository

| File | Used | What it does |
|---|---|---|
| `fallschool_01_naive_vs_framework.ipynb` | Day 1, morning | A naive prompt versus the framework's prompts on one passage — you judge the items |
| `fallschool_02_mini_pipeline.ipynb` | Day 1, afternoon | Passages → questions → LLM rating and revision → distractors → 10 reading + 10 maths items (`day1_items.json`) |
| `fallschool_03_screening_and_prediction.ipynb` | Day 2, morning | Part A: rule and LLM checks on your items (`day2_screened_items.json`); Part B: a difficulty predictor trained on CMCQRD, applied to your items (`day1_predictions.json`) |
| `fallschool_04_artificial_test_takers.ipynb` | Day 2, afternoon | LLM personas answer your items; classical statistics, IRT, distractor analysis, predicted vs. empirical difficulty (`day2_analysis.json`) |
| `cache/`, `day1_items.json`, `day2_screened_items.json`, `day1_predictions.json` | fallback | The instructors' reference run. Every LLM call the notebooks make is stored here, so all four notebooks also run **without** an endpoint (see "Offline mode"), and Day 2 can start from reference items if your own Day-1 run is incomplete |
| `reference/*.html` | read-only | The instructors' run of each notebook, with all outputs, to read along or compare |
| `slides/` | | Slide PDFs, added the evening before each day |
| `requirements.txt` | setup | Python packages |

The notebooks run in order: each one reads the file the previous one wrote (next to the notebooks).

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
5. **Check your setup** (no endpoint needed): in the same terminal run `jupyter lab`, open Notebook 1, change
   `OFFLINE = False` to `OFFLINE = True` in the setup cell (the third cell), and run all cells. If it finishes in a
   few seconds, everything works. Set `OFFLINE` back to `False` afterwards.

## In the room

**Endpoint and key.** The notebooks talk to an OpenAI-compatible endpoint at EPFL. The URL and the key are given out
on Day 1 (they are valid for the two days only — please do not paste them into a notebook or share them). Set them in
the terminal *before* starting Jupyter, so the notebooks pick them up:

```bash
export AIG_BASE_URL="https://.../v1"        # Windows PowerShell: $env:AIG_BASE_URL="https://.../v1"
export AIG_API_KEY="..."                    #                     $env:AIG_API_KEY="..."
jupyter lab
```

[If the endpoint is reachable from Google Colab: open a notebook in Colab, add `AIG_BASE_URL` and `AIG_API_KEY` in the
Secrets panel (key icon on the left, "notebook access" on), and upload `cache/` and the JSON files to the session — or
delete this paragraph if Colab cannot reach the endpoint.]

**Models.** Passages are written by `swiss-ai/Apertus-v1.5-70B`; questions, distractors and all judgements come from
`Qwen/Qwen3-30B-A3B-Instruct-2507`. Both are set in the setup cell.

**Caching.** Every call is stored in `cache/` and replayed when the same call is made again, so re-running a cell is
free and only changed prompts cost new calls. Different pairs get different items because Notebook 2 seeds the
passages with `SEED` — change it if you want your own set.

**Offline mode.** If the endpoint is unavailable, set `OFFLINE = True` in the setup cell and continue: the notebooks
replay the reference run with identical outputs. This only covers the unmodified notebooks; your own prompt edits need
the endpoint.

## Schedule

| | Morning (9:15–12:00) | Afternoon (13:00–16:00) |
|---|---|---|
| Day 1 | Framework, item writing with LLMs; **Notebook 1** at the end | Building the generation stage; **Notebook 2** |
| Day 2 | Evaluation: screening and difficulty prediction; **Notebook 3** | Artificial test-takers and validation; **Notebook 4** |

## Troubleshooting

- *`... not found — run Notebook N first`*: the notebook needs the file written by the previous one. Run that
  notebook, or copy the reference file of the same name from this repository next to the notebooks.
- *externally-managed-environment* when installing: you are not inside the virtual environment — run
  `source .venv/bin/activate` first.
- *SSL: CERTIFICATE_VERIFY_FAILED* on macOS: run *Install Certificates.command* (step 1).
- The first call of a session takes up to two minutes: the model is waking up; later calls take seconds.
- A cell fails with a JSON or schema error: run it again — the notebook retries once with a stricter prompt, and the
  cache means nothing else is recomputed.

## Licence and citation

Notebooks and this text: MIT licence. The framework follows Jensen ([year], [title]) and the pipeline in
Jensen ([year], [title]). CMCQRD: Mullooly, A., et al. (2023), *The Cambridge Multiple-Choice Questions Reading
Dataset*, Cambridge University Press & Assessment — subject to its own licence, not part of this repository.
Questions: [contact e-mail].
