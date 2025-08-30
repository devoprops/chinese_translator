import requests
from typing import Dict, List
import json

class TranslationService:
    def __init__(self):
        # Keep some common phrases for quick access
        self.common_phrases = {
            '轉法輪': 'Zhuan Falun',
            '第一講': 'Lecture One',
            '李洪志': 'Li Hongzhi',
            '法輪大法': 'Falun Dafa'
        }
        
        # Google Translate API endpoint (free tier)
        self.translate_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text: str) -> str:
        """Translate Chinese text to English using Google Translate API"""
        try:
            # Check for common phrases first
            if text in self.common_phrases:
                return self.common_phrases[text]
            
            # Use Google Translate API for dynamic translation
            result = self._google_translate(text)
            print(f"Google Translate result: {result}")
            return result
            
        except Exception as e:
            print(f"Translation failed, using fallback: {e}")
            # Fallback to basic character translation if API fails
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
        """Fallback translation using basic character dictionary"""
        # Basic character translations for fallback
        char_dict = {
            '轉': 'turn', '法': 'law', '輪': 'wheel', '李': 'Li', '洪': 'Hong',
            '志': 'zhi', '目': 'eye', '錄': 'record', '論': 'discuss', '語': 'language',
            '第': 'number', '一': 'one', '講': 'lecture', '真': 'true', '正': 'correct',
            '往': 'go', '高': 'high', '層': 'level', '次': 'time', '上': 'up',
            '帶': 'bring', '人': 'person', '不': 'not', '同': 'same', '有': 'have',
            '善': 'good', '忍': 'endure', '是': 'is', '衡': 'balance', '量': 'measure',
            '好': 'good', '壞': 'bad', '唯': 'only', '標': 'mark', '準': 'standard',
            '氣': 'qi', '功': 'merit', '史': 'history', '前': 'before', '文': 'culture',
            '化': 'change', '就': 'just', '修': 'cultivate', '煉': 'refine', '為': 'for',
            '甚': 'what', '麼': 'particle', '長': 'long', '特': 'special', '點': 'point',
            '我': 'I', '在': 'at', '整': 'whole', '個': 'piece', '傳': 'transmit',
            '過': 'pass', '程': 'process', '中': 'middle', '本': 'root', '著': 'aspect',
            '對': 'toward', '社': 'society', '會': 'meeting', '負': 'bear', '責': 'responsibility',
            '學': 'learn', '員': 'member', '收': 'receive', '到': 'arrive', '的': 'of',
            '效': 'effect', '果': 'result', '影': 'shadow', '響': 'influence', '也': 'also',
            '比': 'compare', '較': 'relatively'
        }
        
        result = []
        for char in text:
            if char in char_dict:
                result.append(char_dict[char])
            else:
                result.append(char)
        
        translation = ' '.join(result)
        if translation:
            translation = translation[0].upper() + translation[1:]
        return translation
    
    def translate_character_by_character(self, text: str) -> List[Dict[str, str]]:
        """Translate text character by character"""
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                # For character-by-character, use the fallback dictionary
                char_dict = {
                    '轉': 'turn, rotate', '法': 'law, method', '輪': 'wheel, round',
                    '李': 'plum', '洪': 'flood, vast', '志': 'will, purpose',
                    '目': 'eye, item', '錄': 'record, copy', '論': 'discuss, theory',
                    '語': 'language, speech', '第': 'sequence, number', '一': 'one',
                    '講': 'speak, lecture', '真': 'true, real', '正': 'correct, right',
                    '往': 'go, toward', '高': 'high, tall', '層': 'layer, level',
                    '次': 'time, order', '上': 'up, above', '帶': 'bring, lead',
                    '人': 'person, human', '不': 'not, no', '同': 'same, together',
                    '有': 'have, exist', '善': 'good, kind', '忍': 'endure, patience',
                    '是': 'is, are', '衡': 'balance, measure', '量': 'measure, quantity',
                    '好': 'good, well', '壞': 'bad, broken', '唯': 'only, unique',
                    '標': 'mark, sign', '準': 'accurate, standard', '氣': 'qi, energy',
                    '功': 'merit, achievement', '史': 'history', '前': 'before, front',
                    '文': 'writing, culture', '化': 'change, transform', '就': 'just, then',
                    '修': 'cultivate, repair', '煉': 'refine, practice', '為': 'for, as',
                    '甚': 'what, why', '麼': 'particle', '長': 'long, grow',
                    '特': 'special, particular', '點': 'point, dot',
                    '我': 'I, me', '在': 'at, in', '整': 'whole, complete', '個': 'individual, piece',
                    '傳': 'transmit, pass on', '過': 'pass, go through', '程': 'process, journey',
                    '中': 'middle, center', '本': 'root, origin', '著': 'particle, aspect',
                    '對': 'toward, correct', '社': 'society', '會': 'meeting, society',
                    '負': 'bear, carry', '責': 'responsibility', '學': 'learn, study',
                    '員': 'member, person', '收': 'receive, collect', '到': 'arrive, reach',
                    '的': 'possessive particle', '效': 'effect, result', '果': 'fruit, result',
                    '影': 'shadow, image', '響': 'sound, influence', '也': 'also, too',
                    '比': 'compare, than', '較': 'compare, relatively'
                }
                translation = char_dict.get(char, 'Unknown')
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
    
    def get_phrase_translation(self, phrase: str) -> str:
        """Get translation for a specific phrase"""
        return self.common_phrases.get(phrase, 'Translation not available')
