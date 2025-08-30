from pypinyin import pinyin, Style
from typing import List, Dict

class PinyinService:
    def __init__(self):
        pass
    
    def generate_pinyin(self, text: str) -> str:
        """Generate pinyin for Chinese text"""
        try:
            # Generate pinyin with tone marks
            pinyin_list = pinyin(text, style=Style.TONE)
            
            # Flatten the list and join with spaces
            result = []
            for word in pinyin_list:
                result.extend(word)
            
            return ' '.join(result)
        except Exception as e:
            # Fallback to character-by-character pinyin
            return self._fallback_pinyin(text)
    
    def generate_pinyin_without_tones(self, text: str) -> str:
        """Generate pinyin without tone marks"""
        try:
            pinyin_list = pinyin(text, style=Style.NORMAL)
            result = []
            for word in pinyin_list:
                result.extend(word)
            return ' '.join(result)
        except Exception as e:
            return self._fallback_pinyin(text)
    
    def generate_character_pinyin(self, text: str) -> List[Dict[str, str]]:
        """Generate pinyin for each character separately"""
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                try:
                    char_pinyin = pinyin(char, style=Style.TONE)[0][0]
                    result.append({
                        'character': char,
                        'pinyin': char_pinyin
                    })
                except:
                    result.append({
                        'character': char,
                        'pinyin': char
                    })
            else:
                result.append({
                    'character': char,
                    'pinyin': char
                })
        return result
    
    def _fallback_pinyin(self, text: str) -> str:
        """Fallback pinyin generation for when pypinyin fails"""
        # Basic pinyin dictionary for common characters
        pinyin_dict = {
            '轉': 'zhuǎn', '法': 'fǎ', '輪': 'lún', '李': 'lǐ', '洪': 'hóng',
            '志': 'zhì', '目': 'mù', '錄': 'lù', '論': 'lùn', '語': 'yǔ',
            '第': 'dì', '一': 'yī', '講': 'jiǎng', '真': 'zhēn', '正': 'zhèng',
            '往': 'wǎng', '高': 'gāo', '層': 'céng', '次': 'cì', '上': 'shàng',
            '帶': 'dài', '人': 'rén', '不': 'bù', '同': 'tóng', '有': 'yǒu',
            '善': 'shàn', '忍': 'rěn', '是': 'shì', '衡': 'héng', '量': 'liáng',
            '好': 'hǎo', '壞': 'huài', '唯': 'wéi', '標': 'biāo', '準': 'zhǔn',
            '氣': 'qì', '功': 'gōng', '史': 'shǐ', '前': 'qián', '文': 'wén',
            '化': 'huà', '就': 'jiù', '修': 'xiū', '煉': 'liàn', '為': 'wèi',
            '甚': 'shén', '麼': 'me', '長': 'zhǎng', '特': 'tè', '點': 'diǎn'
        }
        
        result = []
        for char in text:
            if char in pinyin_dict:
                result.append(pinyin_dict[char])
            else:
                result.append(char)
        
        return ' '.join(result)



