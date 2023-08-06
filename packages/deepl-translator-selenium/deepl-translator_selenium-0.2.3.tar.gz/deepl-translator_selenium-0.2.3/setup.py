from setuptools import setup, find_packages

setup(
    name='deepl-translator_selenium',
    version='0.2.3',
    author="Keit",
    license='MIT',
    py_modules=['main', 'subtitle.helper', 'translator.deepl'],
    packages=(find_packages()),
    install_requires=['Click', 'selenium'],
    description="Translate the subtitle file (*.srt) using DeepL translator, because their API is not free, this tiny tool will use selenium to open the browser and do it instead.",
    long_description='''
Install:
`pip install deepl-translator-selenium`

Usage:
`deepl-translator-selenium --input=<input_file> --output=<output_directory> --source-language=it --target-language=en-US`
    ''',
    entry_points='''
        [console_scripts]
        deepl-translator-selenium=main:cli
    ''',
)
