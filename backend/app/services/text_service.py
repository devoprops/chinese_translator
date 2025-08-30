import re
import jieba
from typing import Dict, List, Any
from app.services.pinyin_service import PinyinService
from app.services.translation_service import TranslationService

class TextService:
    def __init__(self):
        self.pinyin_service = PinyinService()
        self.translation_service = TranslationService()
        
    def get_text_by_id(self, text_id: str) -> Dict[str, Any]:
        """Get text content by ID - simplified for copy-paste approach"""
        try:
            # Return sample data for demonstration
            return {
                'id': text_id,
                'title': 'Sample Text',
                'content': self._get_sample_chinese_text(),
                'sentences': self._segment_into_sentences(self._get_sample_chinese_text())
            }
        except Exception as e:
            raise Exception(f"Failed to get text: {str(e)}")
    
    def _get_sample_chinese_text(self) -> str:
        """Return sample Chinese text for development"""
        return """
        轉法輪
        李洪志
        
        目錄
        
        論語
        
        第一講
        真正往高層次上帶人
        不同層次有不同層次的法
        真、善、忍是衡量好壞人的唯一標準
        氣功是史前文化
        氣功就是修煉
        煉功為甚麼不長功
        法輪大法的特點
        """
    
    def _segment_into_sentences(self, text: str) -> List[str]:
        """Segment Chinese text into sentences"""
        # Remove extra whitespace and split by common sentence endings
        text = re.sub(r'\s+', ' ', text.strip())
        sentences = re.split(r'[。！？\n]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def analyze_characters(self, text: str) -> List[Dict[str, Any]]:
        """Analyze each character in the text using proper services with word grouping"""
        analysis = []
        
        # First, segment the text into words using jieba
        words = list(jieba.cut(text, cut_all=False))
        
        # Track position in original text
        char_index = 0
        
        for word in words:
            # For each word, analyze its characters
            for i, char in enumerate(word):
                if '\u4e00' <= char <= '\u9fff':  # Chinese character range
                    # Use PinyinService for better character coverage
                    char_pinyin = self._get_character_pinyin(char)
                    analysis.append({
                        'character': char,
                        'pinyin': char_pinyin,
                        'meaning': self._get_character_meaning(char),
                        'word': word,  # The complete word this character belongs to
                        'word_position': i,  # Position within the word (0 = first char)
                        'word_length': len(word),  # Total length of the word
                        'is_word_start': i == 0,  # True if this is the first character of a word
                        'is_word_end': i == len(word) - 1  # True if this is the last character of a word
                    })
                else:
                    # Handle non-Chinese characters (spaces, punctuation, etc.)
                    analysis.append({
                        'character': char,
                        'pinyin': char,
                        'meaning': char,
                        'word': char,
                        'word_position': 0,
                        'word_length': 1,
                        'is_word_start': True,
                        'is_word_end': True
                    })
                char_index += 1
        
        return analysis
    
    def get_character_info(self, char: str) -> Dict[str, Any]:
        """Get detailed information about a Chinese character"""
        if not ('\u4e00' <= char <= '\u9fff'):
            return {'error': 'Not a Chinese character'}
        
        return {
            'character': char,
            'pinyin': self._get_character_pinyin(char),
            'meaning': self._get_character_meaning(char),
            'stroke_count': self._get_stroke_count(char),
            'common_phrases': self._get_common_phrases(char)
        }
    
    def _get_character_pinyin(self, char: str) -> str:
        """Get pinyin for a single character using PinyinService"""
        try:
            # Use the PinyinService for better coverage
            char_analysis = self.pinyin_service.generate_character_pinyin(char)
            if char_analysis and len(char_analysis) > 0:
                return char_analysis[0]['pinyin']
            else:
                return char
        except Exception as e:
            # Fallback to hardcoded dictionary if pypinyin fails
            return self._fallback_pinyin(char)
    
    def _fallback_pinyin(self, char: str) -> str:
        """Fallback pinyin for when pypinyin fails"""
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
            '甚': 'shén', '麼': 'me', '長': 'zhǎng', '特': 'tè', '點': 'diǎn',
            # Add more characters for better coverage
            '我': 'wǒ', '在': 'zài', '整': 'zhěng', '個': 'gè', '傳': 'chuán',
            '過': 'guò', '程': 'chéng', '中': 'zhōng', '本': 'běn', '著': 'zhe',
            '對': 'duì', '社': 'shè', '會': 'huì', '負': 'fù', '責': 'zé',
            '學': 'xué', '員': 'yuán', '收': 'shōu', '到': 'dào', '的': 'de',
            '效': 'xiào', '果': 'guǒ', '影': 'yǐng', '響': 'xiǎng', '也': 'yě',
            '比': 'bǐ', '較': 'jiào'
        }
        return pinyin_dict.get(char, char)
    
    def _get_character_meaning(self, char: str) -> str:
        """Get English meaning for a character (will be overridden by batch translation)"""
        # Use local dictionary as placeholder - will be replaced by batch translation
        meaning_dict = {
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
            # Add more characters for better coverage
            '我': 'I, me', '在': 'at, in', '整': 'whole, complete', '個': 'individual, piece',
            '傳': 'transmit, pass on', '過': 'pass, go through', '程': 'process, journey',
            '中': 'middle, center', '本': 'root, origin', '著': 'particle, aspect',
            '對': 'toward, correct', '社': 'society', '會': 'meeting, society',
            '負': 'bear, carry', '責': 'responsibility', '學': 'learn, study',
            '員': 'member, person', '收': 'receive, collect', '到': 'arrive, reach',
            '的': 'possessive particle', '效': 'effect, result', '果': 'fruit, result',
            '影': 'shadow, image', '響': 'sound, influence', '也': 'also, too',
            '比': 'compare, than', '較': 'compare, relatively',
            # Add more common characters that were showing as "Unknown"
            '能': 'able, capable', '夠': 'enough, sufficient', '直': 'straight, direct',
            '接': 'connect, receive', '聽': 'hear, listen', '到': 'arrive, reach',
            '覺': 'feel, perceive', '得': 'get, obtain', '很': 'very, quite',
            '奇': 'strange, odd', '怪': 'strange, weird', '這': 'this', '個': 'classifier',
            '師': 'teacher, master', '父': 'father', '怎': 'how', '會': 'can, able',
            '知': 'know', '道': 'way, path', '呢': 'particle', '因': 'because',
            '國': 'country', '全': 'complete, whole', '形': 'form, shape', '勢': 'power, situation',
            '都': 'all, both', '現': 'now, present', '代': 'generation, era', '科': 'science',
            '醫': 'medicine, doctor', '所': 'place, location', '能': 'able, can',
            '解': 'solve, explain', '釋': 'explain, interpret', '但': 'but, however',
            '它': 'it', '超': 'exceed, surpass', '越': 'surpass, cross', '了': 'particle',
            '常': 'normal, usual', '理': 'principle, reason', '範': 'scope, range',
            '圍': 'surround, range', '用': 'use, employ', '普': 'universal, general',
            '通': 'through, common', '根': 'root, basis'
        }
        return meaning_dict.get(char, 'Unknown')
    
    def _get_stroke_count(self, char: str) -> int:
        """Get stroke count for a character"""
        # This would integrate with a stroke count database
        stroke_dict = {
            '轉': 18, '法': 8, '輪': 15, '李': 7, '洪': 9, '志': 7,
            '目': 5, '錄': 16, '論': 15, '語': 14, '第': 11, '一': 1,
            '講': 17, '真': 10, '正': 5, '往': 8, '高': 10, '層': 15,
            '次': 6, '上': 3, '帶': 11, '人': 2, '不': 4, '同': 6,
            '有': 6, '善': 12, '忍': 7, '是': 9, '衡': 16, '量': 12,
            '好': 6, '壞': 19, '唯': 11, '標': 15, '準': 13, '氣': 10,
            '功': 5, '史': 5, '前': 9, '文': 4, '化': 4, '就': 12,
            '修': 9, '煉': 13, '為': 9, '甚': 9, '麼': 14, '長': 8,
            '特': 10, '點': 17
        }
        return stroke_dict.get(char, 0)
    
    def _get_common_phrases(self, char: str) -> List[str]:
        """Get common phrases that use this character"""
        # This would integrate with a phrase database
        phrase_dict = {
            '法': ['方法', '法律', '法術', '佛法'],
            '輪': ['車輪', '法輪', '輪迴', '輪子'],
            '人': ['人民', '人類', '個人', '好人'],
            '氣': ['空氣', '氣功', '天氣', '生氣'],
            '功': ['功夫', '成功', '功能', '功德'],
            '文': ['文化', '文章', '文學', '文明'],
            '化': ['文化', '變化', '化學', '進化']
        }
        return phrase_dict.get(char, [])
