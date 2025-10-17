import requests
from typing import Dict, List
import jieba
import os

# Load jieba custom dictionary
jieba_dict_path = os.path.join(os.path.dirname(__file__), '../../data/jieba_userdict.txt')
if os.path.exists(jieba_dict_path):
    jieba.load_userdict(jieba_dict_path)
    print(f"Loaded jieba custom dictionary from {jieba_dict_path}")
else:
    print(f"Warning: Jieba custom dictionary not found at {jieba_dict_path}")

from app.services.dictionary_service import dictionary_service


class TranslationService:
    def __init__(self):
        self.dictionary_service = dictionary_service
        
        # Google Translate API endpoint (free tier)
        self.translate_url = "https://translate.googleapis.com/translate_a/single"
    
        # Cache for API translations to avoid repeated calls
        self.translation_cache = {}
    
    def translate(self, text: str, pinyin: str = None) -> str:
        """
        Translate Chinese text to English.
        
        Priority:
        1. Local dictionary
        2. Translation cache
        3. Google Translate API
        4. Fallback: character-by-character using dictionary
        """
        try:
            # Step 1: Check local dictionary first
            translation = self.dictionary_service.get_translation(text, pinyin)
            if translation:
                print(f"Dictionary hit: '{text}' -> '{translation}'")
                return translation
            
            # Step 2: Check cache
            if text in self.translation_cache:
                print(f"Cache hit: '{text}' -> '{self.translation_cache[text]}'")
                return self.translation_cache[text]
            
            # Step 3: Use Google Translate API
            result = self._google_translate(text)
            print(f"Google Translate: '{text}' -> '{result}'")
            
            # Cache the result
            self.translation_cache[text] = result
            return result
            
        except Exception as e:
            print(f"Translation failed, using fallback: {e}")
            # Step 4: Fallback to character-by-character dictionary lookup
            return self._fallback_translation(text)
    
    def _google_translate(self, text: str) -> str:
        """Translate using Google Translate API"""
        try:
            params = {
                'client': 'gtx',
                'sl': 'zh',  # Source language: Chinese
                'tl': 'en',  # Target language: English
                'dt': 't',   # Translation type
                'q': text
            }
            
            response = requests.get(self.translate_url, params=params, timeout=10)
            response.raise_for_status()
            
            # Parse the response
            data = response.json()
            if data and len(data) > 0 and len(data[0]) > 0:
                # Extract the translated text
                translated_parts = []
                for part in data[0]:
                    if part[0]:  # The translated text
                        translated_parts.append(part[0])
                
                translation = ''.join(translated_parts)
                return translation.strip()
            else:
                raise Exception("No translation data received")
                
        except requests.RequestException as e:
            print(f"Translation API error: {e}")
            raise e
        except Exception as e:
            print(f"Translation parsing error: {e}")
            raise e
    
    def _fallback_translation(self, text: str) -> str:
        """
        Fallback translation using dictionary service character-by-character.
        """
        # Try dictionary service first for the whole text
        translation = self.dictionary_service.get_translation(text)
        if translation:
            return self._extract_first_meaning(translation)
        
        # If not found, try character-by-character using dictionary service
        translations = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                char_translation = self.dictionary_service.get_translation(char)
                if char_translation:
                    # Extract just the first meaning
                    first_meaning = self._extract_first_meaning(char_translation)
                    translations.append(first_meaning)
                else:
                    translations.append(char)  # Keep original if not found
            else:
                translations.append(char)  # Non-Chinese characters kept as-is
        
        result = ' '.join(translations) if translations else text
        # Capitalize first letter
        if result:
            result = result[0].upper() + result[1:] if len(result) > 1 else result.upper()
        return result
    
    def _extract_first_meaning(self, definition: str) -> str:
        """
        Extract the first meaning from a dictionary definition.
        Format: "1. meaning; 2. other meaning" -> "meaning"
        """
        # Split by semicolon to get first definition group
        first_def = definition.split(';')[0]
        
        # Remove number prefix if present (e.g., "1. meaning" -> "meaning")
        if '.' in first_def:
            parts = first_def.split('.', 1)
            if len(parts) > 1:
                first_def = parts[1].strip()
        
        return first_def.strip()
    
    def translate_character_by_character(self, text: str) -> List[Dict[str, str]]:
        """
        Translate text character by character using dictionary service.
        Returns a list of character-translation pairs.
        """
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                # Use dictionary service to get translation
                translation = self.dictionary_service.get_translation(char)
                if translation:
                    # Extract the first definition
                    translation = self._extract_first_meaning(translation)
                else:
                    translation = 'Unknown'
                
                result.append({
                    'character': char,
                    'translation': translation
                })
            else:
                result.append({
                    'character': char,
                    'translation': char
                })
        return result
    
    def get_character_fallback(self, char: str) -> str:
        """
        Get translation for a single character using dictionary service.
        Returns the full definition with all numbered meanings.
        """
        # Use dictionary service to get full translation
        translation = self.dictionary_service.get_translation(char)
        if translation:
            return translation  # Return full definition with all numbers
        
        return 'Unknown'
    
    def get_phrase_fallback(self, phrase: str) -> str:
        """
        Get translation for a multi-character phrase using dictionary service.
        Returns the full definition with all numbered meanings.
        """
        # Use dictionary service to get full translation
        translation = self.dictionary_service.get_translation(phrase)
        if translation:
            return translation  # Return full definition with all numbers
        
        return 'Unknown'


# Create a singleton instance
translation_service = TranslationService()
