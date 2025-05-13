"""
Language manager for multi-language support
"""
import os
import json
import configparser

LANGUAGES_DIR = "languages"
DEFAULT_LANGUAGE = "en"
CONFIG_FILE = "config.json"

class LanguageManager:
    """Manages application language and translations"""

    def __init__(self):
        self.current_language = DEFAULT_LANGUAGE
        self.translations = {}
        self.is_rtl = False
        self.load_language_from_config()

    def load_language_from_config(self):
        """Load language from configuration file"""
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
                language_code = config.get("app_language", DEFAULT_LANGUAGE)
                self.load_language(language_code)
        except FileNotFoundError:
            print("Config file not found. Falling back to default language.")
            self.load_language(DEFAULT_LANGUAGE)

    def load_language(self, language_code):
        """Load translations for the specified language

        Args:
            language_code: Language code (e.g., 'en', 'ar')
        """
        try:
            file_path = os.path.join(LANGUAGES_DIR, f"{language_code}.json")
            with open(file_path, "r", encoding="utf-8") as file:
                self.translations = json.load(file)
            self.current_language = language_code
            self.is_rtl = language_code in ["he", "ar"]  # Add RTL languages here
        except FileNotFoundError:
            print(f"Language file for '{language_code}' not found. Falling back to default language.")
            self.load_language(DEFAULT_LANGUAGE)

    def translate(self, key):
        """Translate a key to the current language

        Args:
            key: Translation key

        Returns:
            Translated string
        """
        return self.translations.get(key, key)

# Singleton instance of LanguageManager
language_manager = LanguageManager()
