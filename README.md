
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

Create and activate virtual environment:

```zsh
pyenv virtualenv pkp-ics
pyenv activate pkp-ics
```

Download [required packages](#packages):

```zsh
pip install -r requirements.txt
```


