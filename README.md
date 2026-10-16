# Automated Item Generation with Large Language Models — Fall School, University of Tübingen

Materials for the two-day workshop *Automated Item Generation with Agentic AI Approaches* by Rudolf Debelak (EPFL)
and Rasmus Jensen (ETH Zurich / IBE), taught on 6–7 October 2026 at the 5th Fall School of the
[Methods Center (Methodenzentrum)](https://uni-tuebingen.de/fakultaeten/wirtschafts-und-sozialwissenschaftliche-fakultaet/faecher/fachbereich-sozialwissenschaften/methodenzentrum/events/fall-school/)
of the University of Tübingen, *Advanced AI for Research Design and Analysis*. Four Jupyter notebooks take you from a
naive prompt to an item bank with psychometric evidence: generation, screening, difficulty prediction, and artificial
test-takers.

You are welcome to use the materials in your own teaching and research (see [Licence and citation](#licence-and-citation)).
You need neither an API key nor a GPU: all four notebooks can replay the instructors' reference run from `cache/`.
The only thing to fetch separately is the CMCQRD data set for Notebook 3, Part B (see [Setup](#setup)).

## What is in this repository

| File | Course slot | What it does |
|---|---|---|
| `fallschool_01_naive_vs_framework.ipynb` | Day 1, morning | A naive prompt versus the framework's prompts on one passage — you judge the items |
| `fallschool_02_mini_pipeline.ipynb` | Day 1, afternoon | Passages → questions → LLM rating and revision → distractors → 10 reading + 10 maths items (`day1_items.json`) |
| `fallschool_03_screening_and_prediction.ipynb` | Day 2, morning | Part A: rule and LLM checks on the items (`day2_screened_items.json`); Part B: a difficulty predictor trained on CMCQRD, applied to the items (`day1_predictions.json`) |
| `fallschool_04_artificial_test_takers.ipynb` | Day 2, afternoon | Artificial test-takers (persona prompt × model size) answer the items; classical statistics, IRT, distractor analysis, predicted vs. empirical difficulty (`day2_responses.json`, `day2_analysis.json`) |
| `cache/` and the `day*.json` files | every run | The instructors' reference run. Every LLM call the notebooks make is stored in `cache/`, so the notebooks run **without** any model endpoint (see "Offline mode"); the JSON files are what each notebook wrote in that run |
| `reference/*.html` | read-only | The instructors' run of each notebook with its outputs, to read along or compare. Notebook 3 omits the summary tables of the CMCQRD data, which its licence does not allow us to publish |
| `check_cache.py` | setup | One-command check that notebooks and cache fit together |
| `slides_pdf/` | | Slides for Day 1 and Day 2 (PDF) |
| `requirements.txt` | setup | Python packages |
| `LICENSE` | | MIT licence for the code |

The notebooks run in order: each one reads the file the previous one wrote (next to the notebooks).

## Setup

About 20 minutes, most of it spent on the package download.

1. **Python 3.12.** Install from https://www.python.org/downloads/ (macOS: afterwards double-click
   *Install Certificates.command* in the folder */Applications/Python 3.12*). Python 3.10 or 3.11 also works.
2. **Get the materials.** Green *Code* button above → *Download ZIP*, unzip; or `git clone` this repository.
3. **Install the packages** in a virtual environment. In a terminal, inside the unzipped folder:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt    # ~2 GB (includes PyTorch); use a good connection
   ```
4. **Download the CMCQRD data set** (only needed for Notebook 3, Part B). The Cambridge Multiple-Choice Questions
   Reading Dataset (Mullooly et al., 2023, documentation: https://doi.org/10.17863/CAM.102185) is available from
   Cambridge University Press & Assessment after registering and accepting their licence, which covers
   non-commercial research and teaching:
   https://researchdatasets.cambridge.org/datasets/cambridge-multiple-choice-questions-reading-dataset.
   Rename the downloaded file to `CMCQRD.jsonl` and put it in the same folder as the notebooks. The licence does not
   allow us to redistribute the data, so it is not part of this repository. Without it, everything else still runs:
   Notebook 4 then uses the reference predictions in `day1_predictions.json`.
5. **Check your setup.** In the same terminal, `python check_cache.py` should end with
   *cache, models and first prompts all match*. Then run `jupyter lab`, open Notebook 1, set `OFFLINE = True` in the
   setup cell (the third cell) and run all cells; it finishes in a few seconds. Set `OFFLINE = True` in the same way
   in each of the other notebooks.

## Running the notebooks

**Without an endpoint (offline mode).** With `OFFLINE = True`, every LLM call is replayed from `cache/`, and you see
exactly the outputs of the instructors' reference run. This is how the participants ran the notebooks in Tübingen:
the models ran on an EPFL cluster that is reachable only from inside the EPFL network, so the instructors ran the same
notebooks live on the projector, and new prompts or settings were tried together in the room.

**With your own endpoint.** To try your own prompts, rubrics or seeds, you need an OpenAI-compatible endpoint. Leave
`OFFLINE = False`, set the two environment variables before starting Jupyter, and put your model names into
`TEXT_MODEL`, `ITEM_MODEL` and (Notebook 4) `TAKER_MODELS` in the setup cell:

```bash
export AIG_BASE_URL="https://.../v1"        # Windows PowerShell: $env:AIG_BASE_URL="https://.../v1"
export AIG_API_KEY="..."                    #                     $env:AIG_API_KEY="..."
jupyter lab
```

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

## Course outline

If you work through the materials on your own, the slides and notebooks follow the order of the course:

| | Morning | Afternoon |
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

Code (the notebooks and `check_cache.py`): MIT licence, see [`LICENSE`](LICENSE). Slides and this text:
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Figures, tables and examples taken from other publications
remain under their original terms and are cited on the slides.

The framework and the pipeline follow Rasmus Jensen's master's thesis and semester project at ETH Zurich
(Jensen, 2025, 2026). CMCQRD: Mullooly, A., et al. (2023), *The Cambridge Multiple-Choice Questions Reading
Dataset*, Cambridge University Press & Assessment — subject to its own licence, not part of this repository.

If you use these materials, please cite them as:

> Debelak, R., & Jensen, R. (2026). *Automated item generation with agentic AI approaches* [Course materials].
> 5th Fall School of the Methods Center, University of Tübingen.
> https://github.com/RDebelak/tuebingen-aig-fall-school

Questions: rudolf.debelak@epfl.ch.
