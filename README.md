# Back to the Future — DVD Cart

A small kata-style project that prices a DVD shopping cart for the *Back to the Future* trilogy, with progressive discounts based on how many distinct volumes are purchased. Comes with a typed pricing engine, a parametrized `pytest` suite, lint/type-check configuration, a GitHub Actions CI workflow, and a themed Streamlit UI.

## Project structure

```
btf_project/
├── pyproject.toml              # packaging, deps, pytest/ruff/mypy/coverage config
├── requirements.txt            # mirror of pyproject deps for `pip install -r` users
├── README.md
├── .github/workflows/ci.yml    # lint + type-check + tests on 3.11 & 3.12
├── src/
│   └── btf/                    # the package
│       ├── __init__.py
│       ├── __main__.py         # CLI demo (`python -m btf`)
│       ├── catalog.py          # available films
│       ├── models.py           # Film / BttfFilm / OtherFilm dataclasses
│       ├── parser.py           # name -> Film lookup
│       ├── pricing.py          # discount rules and total price
│       └── ui.py               # Streamlit app
└── tests/                      # pytest suite (parametrized)
    ├── test_parser.py
    ├── test_pricing_reduction.py
    └── test_pricing_total.py
```

## Discount rules (per the spec)

| Distinct BTTF volumes in cart | Discount applied to BTTF subtotal |
| ----------------------------- | --------------------------------- |
| 0 or 1                        | 0 %                               |
| 2                             | 10 %                              |
| 3                             | 20 %                              |

"Other" films are never discounted. The discount is applied to the **entire BTTF subtotal**, not per distinct volume — duplicates are charged but still benefit from the rate the cart qualifies for.

> **Pricing note.** The discount is applied to the total number of BTTF DVDs purchased, based on how many distinct volumes are present in the cart. This follows the spec literally — see Example 4: `[v1, v2, v3, v2]` → `4 × 15 × 0.8 = 48 €`. This differs from the classic "book kata" set-partitioning problem, which this assignment does not implement by design.

### Worked example

Cart: `[BTTF1, BTTF2, BTTF3, BTTF2, "La chèvre"]`

- 3 distinct BTTF volumes → 20 % discount
- BTTF subtotal: `4 × 15 € × 0.80 = 48 €`
- Other subtotal: `1 × 20 € = 20 €`
- **Total: 68 €**

---

## 1. Set up the environment

The project targets **Python 3.11+**.

### Recommended (editable install with dev extras)

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Windows (cmd):         .venv\Scripts\activate
# macOS/Linux:           source .venv/bin/activate

pip install -e ".[dev]"
```

This installs the `btf` package in editable mode plus `pytest`, `pytest-cov`, `ruff`, and `mypy`.

### Alternative — `requirements.txt`

```bash
pip install -r requirements.txt
pip install -e .   # still needed so `import btf` resolves
```

### Conda

```bash
conda create -n btf_env python=3.11 -y
conda activate btf_env
pip install -e ".[dev]"
```

---

## 2. Run the tests

All tooling is configured in `pyproject.toml`. From the project root:

```bash
pytest
```

This runs the full suite with coverage (configured to fail under 90 % on the `btf` package, excluding the Streamlit UI).

Run a single file or test:

```bash
pytest tests/test_pricing_total.py
pytest tests/test_pricing_total.py::test_total_price_scenarios -v
```

### Lint & type-check

```bash
ruff check .
mypy
```

The same three commands run in CI on every push / pull request — see [.github/workflows/ci.yml](.github/workflows/ci.yml).

---

## 3. Run the CLI demo

```bash
python -m btf
```

Sample output:

```
Scenario 1 [v1, v2, v3]: 36.00 €
Scenario 2 [v1, v3]: 27.00 €
Scenario 3 [v1]: 15.00 €
Scenario 4 [v1, v2, v3, v2]: 48.00 €
Scenario 5 [v1, v2, v3, other]: 56.00 €
```

A `btf` console script is also installed by the editable install, so you can simply run `btf`.

---

## 4. Run the Streamlit app

The UI is themed after the *Back to the Future* color palette — deep purple sky, flame-gradient title, neon-cyan accents — and delegates all pricing to `btf.pricing`, so it stays consistent with the test suite.

From the project root:

```bash
streamlit run src/btf/ui.py
```

Streamlit will open <http://localhost:8501>. You can:

- Add films to the cart from the catalog grid.
- Increment / decrement / remove items.
- See the BTTF subtotal, discount applied, other-films subtotal, and final total update live.
- Clear the cart with the trash button.

> The script contains a small `sys.path` bootstrap so it runs whether or not the package is installed — but installing the package (`pip install -e .`) is still recommended.

---

## Design notes

- **Pure pricing core.** `btf.pricing` has no I/O and no Streamlit dependency — it operates on lists of `Film` dataclasses. This is what makes the suite easy to test and the UI easy to swap.
- **Single source of truth.** The catalog and pricing functions are imported by both the CLI (`__main__.py`) and the UI (`ui.py`); there are no duplicated price tables.
- **Discount semantics.** The implementation follows the spec literally: rate is determined by *distinct volumes in the cart*, then applied to the whole BTTF subtotal. (This is intentionally simpler than the optimal-set-partitioning variant of the kata.)
- **Quality gates.** `ruff` (lint + isort + pyupgrade), `mypy --strict`, and ≥ 90 % branch coverage are enforced locally and in CI.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'btf'` when running pytest** — install the package: `pip install -e .` from the project root.
- **`ModuleNotFoundError: No module named 'btf'` when running Streamlit** — this should not happen anymore (the UI bootstraps `sys.path` itself), but if it does, run `pip install -e .` and retry, or launch via `python -m streamlit run src/btf/ui.py`.
- **`streamlit: command not found`** — activate your virtualenv, or run `python -m streamlit run src/btf/ui.py`.
- **Fonts look wrong** — the UI loads Google Fonts (Bebas Neue, Orbitron, IBM Plex Mono); first load needs an internet connection.
# Back to the Future — DVD Cart

A small kata-style project that prices a DVD shopping cart for the *Back to the Future* trilogy, with progressive discounts based on how many distinct volumes are purchased. Comes with a pricing engine, a pytest test suite, and a themed Streamlit UI.

## Project structure

```
btf_project/
├── requirements.txt
├── README.md
└── src/
    ├── app.py          # CLI entry point (prints scenario totals)
    ├── catalog.py      # Available films
    ├── models.py       # Film dataclasses
    ├── parser.py       # Name -> Film lookup
    ├── pricing.py      # Discount rules and total price
    ├── ui.py           # Streamlit app
    └── tests/          # Pytest suite
```

## Discount rules

| Distinct BTTF volumes in cart | Discount on BTTF subtotal |
| ----------------------------- | ------------------------- |
| 1                             | 0%                        |
| 2                             | 10%                       |
| 3                             | 20%                       |

"Other" films are not discounted.

---

## 1. Set up the environment

The project targets **Python 3.11+**.

### Using conda (recommended on Windows)

```bash
conda create -n btf_env python=3.11 -y
conda activate btf_env
pip install -r requirements.txt
```

### Using venv

```bash
python -m venv .venv
# Windows (cmd)
.venv\Scripts\activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

Dependencies installed: `pytest`, `streamlit`.

---

## 2. Run the tests

The test files use top-level imports such as `from models import ...`, so `src/` must be on `PYTHONPATH`. Two equivalent options:

### Option A — `pytest.ini` at the project root (recommended)

Create `pytest.ini` next to `requirements.txt`:

```ini
[pytest]
pythonpath = src
testpaths = src/tests
```

Then from the project root:

```bash
pytest
```

### Option B — run pytest from inside `src/`

```bash
cd src
pytest tests
```

Run a single test file:

```bash
pytest src/tests/test_parse_input.py -v
```

---

## 3. Run the CLI demo

The CLI prints totals for a few preset scenarios:

```bash
cd src
python app.py
```

Expected output is something like:

```
Scenario 1:  36.0
Scenario 2:  24.0
Scenario 3:  15.0
...
```

---

## 4. Run the Streamlit app

The UI is themed after the *Back to the Future* color palette (deep purple sky, flame-gradient title, neon-cyan accents).

From the project root:

```bash
streamlit run src/ui.py
```

Streamlit will open a browser tab (default: <http://localhost:8501>). You can:

- Add films to the cart from the catalog grid.
- Increment / decrement / remove items.
- See the BTTF subtotal, discount applied, other-films subtotal, and final total update live.
- Clear the cart with the trash button.

The UI delegates all pricing to `pricing.get_total_price` and `pricing.get_bttf_reduction_rate`, so it stays consistent with the test suite.

---

## Troubleshooting

- **`ModuleNotFoundError: No module named 'models'` when running pytest** — `src/` isn't on `PYTHONPATH`. Use the `pytest.ini` from section 2 or run pytest from inside `src/`.
- **Streamlit can't find `catalog` / `pricing`** — make sure you launch with `streamlit run src/ui.py` from the project root (Streamlit adds the script's directory to `sys.path`).
- **Fonts look wrong** — the UI loads Google Fonts (Bebas Neue, Orbitron, IBM Plex Mono); an active internet connection is required for the first load.
