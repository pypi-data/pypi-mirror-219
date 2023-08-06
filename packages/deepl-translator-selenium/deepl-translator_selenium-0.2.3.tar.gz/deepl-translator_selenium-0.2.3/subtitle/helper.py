import os.path
import re


class Helper:
    _file_path: str = ''
    _content: str = ''
    _subtitles: dict[str, str]

    def __init__(self, file: str):
        self._file_path = file
        self._content = self._load_file_to_string()
        self._content = self._content.rstrip('\n')
        self._subtitles = self._load_content_to_dict()


    def _get_filename_from_path(self) -> str:
        return self._file_path.split('/')[-1]

    def _load_file_to_string(self) -> str:
        with open(self._file_path, 'r') as file:
            return file.read()

    def _write_string_to_file(self, output_file: str, content: str):
        with open(output_file, "w") as text_file:
            text_file.write(content)

    def _load_content_to_dict(self) -> dict[str, str]:
        key_regex: str = r'.+ --> .+'
        subtitles: dict[str, str] = {}

        pattern = re.compile(key_regex)
        key = ''
        for line in self._content.split('\n'):
            if line.isnumeric() or len(line.strip()) == 0:
                pass
            elif pattern.match(line):
                key = line
            else:
                if key in subtitles:
                    subtitles[key] = f'{subtitles[key]} {line}'
                else:
                    subtitles[key] = line if len(line) > 0 else "<Empty>"

        return subtitles

    def output_translated_subtitle(self, translated_subtitles: dict[str, str], output_directory: str):
        content: str = self._compose_subtitle(translated_subtitles)
        self._write_string_to_file(f'{output_directory}/{self._get_filename_from_path()}', content)

    def _compose_subtitle(self, translated_subtitles: dict[str, str]) -> str:
        content = ''
        index = 1
        for key in translated_subtitles.keys():
            val = translated_subtitles[key]
            content = content + f'{index}\n{key}\n{val}\n\n'
            index = index + 1

        return content

    def get_subtitles(self) -> dict[str, str]:
        return self._subtitles
