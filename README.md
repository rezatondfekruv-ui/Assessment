# ✨ VU Assessment Practice Hub

A single [Streamlit](https://streamlit.io) web app that helps Victoria University learning designers and academics design **backward-designed, authentic, secure** assessments aligned to VU's Higher Education Assessment Standards.

It combines three previously-separate tools into one cohesive, accessible app:

| Section | What it does |
|---|---|
| **✨ Design Generator** | A guided, backward-design questionnaire that builds a tailored **MS Copilot master prompt** plus six modular follow-up prompts for a complete assessment structure. |
| **🛠️ Tools** | **Unit LO Builder**, **Course LO Builder** (with Graduate Capability & Employability Skills coverage), **Rubric Builder** (Generic / SOLO / Bloom's descriptors), **Assessment Checker** (HE & TAFE), and a **Standards Reference**. |
| **📚 Resources** | A curated, topic-filterable, searchable library of assessment-design readings, guides, frameworks and tools — from VU and across the sector. |

> Designed for VU Higher Education delivery on Australian campuses (Melbourne, Sydney, Brisbane). The Assessment Checker also includes a TAFE/VET pathway.

---

## 🚀 Quick start (run locally)

You'll need **Python 3.9+**.

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/vu-assessment-practice-hub.git
cd vu-assessment-practice-hub

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run streamlit_app.py
```

The app opens in your browser at <http://localhost:8501>.

---

## ☁️ Deploy to Streamlit Community Cloud (free)

1. Push this repository to GitHub.
2. Go to <https://share.streamlit.io> and sign in with GitHub.
3. Click **New app**, choose this repo, and set the main file to **`streamlit_app.py`**.
4. Click **Deploy**. Streamlit auto-installs `requirements.txt` and serves the app.

`streamlit_app.py` is the conventional entry-point name that Streamlit Community Cloud detects automatically.

---

## 📁 Project structure

```
.
├── streamlit_app.py        # The entire app (entry point)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore
└── .streamlit/
    └── config.toml         # VU brand theme
```

Everything lives in one `streamlit_app.py` for easy review and deployment — data, prompt builders, and page renderers are clearly sectioned within it.

---

## ♿ Accessibility ("the blind spot")

Accessibility was treated as a first-class requirement, not an afterthought:

- **Never colour alone** — every status (pass/warn/fail, coverage, weighting totals) is conveyed with **text + an icon**, so it works for colour-blind users and screen readers.
- **Native, accessible controls** — built from standard Streamlit widgets, which ship with ARIA roles and full keyboard support.
- **Copy-friendly outputs** — generated prompts use Streamlit code blocks with a built-in, keyboard-accessible *copy* button.
- **Linear pages, no hidden steps** — each tool is one scrollable page rather than a multi-step wizard with hidden state, which is far friendlier for assistive technology.
- **High contrast + visible focus** — the VU aubergine/blue palette meets contrast guidance, and a visible focus outline aids keyboard navigation.
- **Logical headings** — a consistent heading hierarchy supports screen-reader navigation.

> **Privacy:** the app holds everything in your browser session. Nothing you type is stored or transmitted.

---

## 🎨 Branding

Colours follow VU Brand Guidelines v1.2:

| Token | Hex |
|---|---|
| Aubergine | `#1E1248` |
| Blue | `#5BC2E7` |
| Melon | `#ED6B5E` |
| Grape | `#B49AD2` |

The theme is set in `.streamlit/config.toml`; component-level styling is injected from within the app.

---

## 🧩 Notes & limitations

- The Design Generator and Tools **produce prompts and structures for review** — they don't call any AI model. Paste the generated prompt into MS Copilot to generate the full design.
- Curated resource links are reproduced from the original hub. A few external links that were wrapped by an email security gateway now point to their publisher landing pages; please verify any link before sharing widely.
- This is an independent learning-design aid and is **not** an official VU policy system. Always confirm against current VU Assessment Standards and CAMS requirements.

---

## 📄 Licence

Released under the [MIT Licence](LICENSE). VU branding and curated content remain the property of Victoria University and the respective resource authors.

---

*Built by Learning Design and Innovation, Victoria University.*
