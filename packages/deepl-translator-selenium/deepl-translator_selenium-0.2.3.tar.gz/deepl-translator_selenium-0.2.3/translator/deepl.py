from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class DeepL:
    _content: list[str] = []
    _url: str = 'https://www.deepl.com/translator'
    _css_selector_input: str = 'div[contenteditable=true]'
    _css_selector_target_language_dropdown: str = 'button[data-testid="translator-target-lang-btn"]'
    _css_selector_source_language_dropdown: str = 'button[data-testid="translator-source-lang-btn"]'
    _css_selector_source_language_dropdown_value: str = 'button[data-testid="translator-lang-option-ja"]'
    _css_selector_target_language_dropdown_value: str = 'button[data-testid="translator-lang-option-en-US"]'
    _css_selector_output_text: str = 'div[aria-labelledby="translation-results-heading"]'
    _wait_time_translate: int = 10
    _wait_time_first_load: int = 5
    _wait_time_implicit: int = 10
    _translator_max_length: int = 1500
    _driver = None

    def __init__(self, content: list[str], source_lang: str = 'ja', target_lang: str = 'en-US'):
        self._css_selector_source_language_dropdown_value = f'button[data-testid="translator-lang-option-{source_lang}"]'
        self._css_selector_target_language_dropdown_value = f'button[data-testid="translator-lang-option-{target_lang}"]'
        self._content = content

    def _check_driver(self):
        pass


    def _open_chrome_browser(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        options.add_argument("--lang=en-US")
        options.add_argument("--lang=en-GB")
        driver = webdriver.Chrome(options=options)
        driver.get(self._url)
        driver.implicitly_wait(self._wait_time_implicit)
        assert "DeepL Translate: The world's most accurate translator" in driver.title
        # Wait for first javascript refresh
        time.sleep(self._wait_time_first_load)

        return driver


    def _break_content_to_batch(self) -> list[str]:
        batch: list[str] = []

        content = ''
        for val in self._content:
            if len(content) + len(val) + 1 > self._translator_max_length:
                batch.append(content)
                content = ''
            content = content + f'{val}\n'

        batch.append(content)

        return batch



    def _translate(self) -> list[str]:
        warning_printed: bool = False

        driver = self._driver

        # Set source language to Japanese
        driver.find_element(By.CSS_SELECTOR, self._css_selector_source_language_dropdown).click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, self._css_selector_source_language_dropdown_value).click()

        # Change target language to English
        driver.find_element(By.CSS_SELECTOR, self._css_selector_target_language_dropdown).click()
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, self._css_selector_target_language_dropdown_value).click()


        batch: list[str] = self._break_content_to_batch()
        translated_text: str = ''

        for val in batch:
            val = val.rstrip("\n")
            # Enter text need to translate
            textarea_input_elem = driver.find_element(By.CSS_SELECTOR, self._css_selector_input)
            textarea_input_elem.send_keys(val)
            time.sleep(self._wait_time_translate)

            # Get Output Text
            output_elem = driver.find_element(By.CSS_SELECTOR, self._css_selector_output_text)
            output_text = output_elem.text
            output_text = output_text.rstrip("\n")

            if output_text.count('\n') != val.count('\n') and not warning_printed:
                import warnings
                warnings.warn('''Number of lines returns from DeepL translator is different from input.
                This will most likely cause mismatch in subtitle timing''')

            translated_text = translated_text + '\n' + output_text

            # Clear input text
            textarea_input_elem.clear()

        return translated_text.split('\n')



    def translate(self) -> list[str]:
        self._check_driver()
        self._driver = self._open_chrome_browser()
        return self._translate()
