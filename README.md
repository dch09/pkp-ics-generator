
# PKP ICS Generator 🚅

Python script to generate ics calendar event from PKP Intercity pdf file.


## Usage 🗓️
To generate .ics file, simply use:
```zsh
python3 main.py -i [pdf_filepath]
```

Or using --output argument, if you want to specifiy the path:
```zsh
python3 main.py -i [pdf_filepath] -o [output_path]
```
## Installation 🧑‍💻

Clone this repo or download zip:
```zsh
git clone https://github.com/dch09/pkp-ics-generator.git
cd pkp-ics-generator
```

**Create and activate virtual environment**:

---
Using pyenv

```zsh
pyenv virtualenv pkp-ics
pyenv activate pkp-ics
```
---
Using venv

```zsh
python3 -m venv pkp-ics
source pkp-ics/bin/activate
```

---

Download required packages:

```zsh
pip install -r requirements.txt
```

## Packages 📦
- [ics](https://github.com/ics-py/ics-py)
- [pdfplumber](https://github.com/jsvine/pdfplumber)
- [Pillow](https://github.com/python-pillow/Pillow)
- [pytz](https://pypi.org/project/pytz)

