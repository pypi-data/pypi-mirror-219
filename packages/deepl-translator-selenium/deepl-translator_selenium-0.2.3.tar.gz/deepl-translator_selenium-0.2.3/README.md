# What is this?

Translate the subtitle file (*.srt) using DeepL translator, because their API is not free, this tiny tool will use selenium to open the browser and do it instead.

## Installation

Can clone this repo and use the main file directly

```commandline
python main.py --input=<input_file> --output=<output_directory> --source-language=it --target-language=en-US
```

Or using [pipy](https://pypi.org/project/deepl-translator-selenium/)

```commandline
pip install deepl-translator-selenium
```

```commandline
deepl-translator-selenium --input=<input_file> --output=<output_directory> --source-language=it --target-language=en-US
```

## Usage

Note: The source language is not optional, automatic detection sometimes cause issues, so I am forced to have this as a parameter.

```commandline
deepl-translator-selenium --help
Usage: deepl-translator-selenium [OPTIONS]

Options:
  --input TEXT             Subtitle file *.srt (Default: ./sample.txt)
  --output-directory TEXT  Output "directory" not a file name (Default:
                           ./output)
  --source-language TEXT   Output "Source language code, e.x: it for Italian,
                           ja for Japanese...
  --target-language TEXT   Output "Target language code, e.x: en-US for
                           English, ko for Korean...
  --help                   Show this message and exit.
```

## Dependencies
- Selenium Chrome Driver: You should have Chrome and correct [Chrome driver](https://chromedriver.chromium.org/downloads) version installed.

## Later
- Support directory input
- Move CSS selector as environment variables (since it keep getting changed from DeepL)
- Auto chrome driver resolver

