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
