import click
from subtitle.helper import  Helper as Subtitle
from translator.deepl import DeepL as DeepLTranslator
import os


def _create_output_directory_if_not_exist(output_directory: str):
    isExist = os.path.exists(output_directory)
    if not isExist:
        os.makedirs(output_directory)


@click.command()
@click.option('--input', default='./sample.srt', help='Subtitle file *.srt (Default: ./sample.txt)')
@click.option('--output-directory', default='./output', help='Output "directory" not a file name (Default: ./output)')
@click.option('--source-language', default='ja',
              help='Output "Source language code, e.x: it for Italian, ja for Japanese...')
@click.option('--target-language', default='en-US',
              help='Output "Target language code, e.x: en-US for English, ko for Korean...')
def cli(input: str, output_directory: str, source_language: str, target_language: str):
    _create_output_directory_if_not_exist(output_directory)

    # Extract subtitles to dict.
    subtitle_helper = Subtitle(input)
    subtitles: dict[str, str] = subtitle_helper.get_subtitles()
    subtitle_helper.output_translated_subtitle(subtitles, output_directory)
    value_list: list[str] = [v for v in subtitles.values()]

    # Translate using selenium - DeepL
    translator = DeepLTranslator(value_list, source_language, target_language)
    translated_value_list = translator.translate()
    translated_subtitles: dict[str, str] = {}
    index = 0
    for key in subtitles.keys():
        translated_subtitles[key] = translated_value_list[index]
        index += 1

    # Export to file
    subtitle_helper.output_translated_subtitle(translated_subtitles, output_directory)


if __name__ == '__main__':
    cli()
