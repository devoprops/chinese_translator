"""
Dictionary Service
Provides dictionary lookup, script detection, and conversion between simplified/traditional Chinese.
"""

from typing import Dict, List, Optional, Tuple
import sys
import os

# Add backend directory to path to import local_dictionary
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from data.local_dictionary import DICTIONARY, SIMPLIFIED_TO_TRADITIONAL, TRADITIONAL_TO_SIMPLIFIED


class DictionaryService:
    def __init__(self):
        self.dictionary = DICTIONARY
        self.simp_to_trad = SIMPLIFIED_TO_TRADITIONAL
        self.trad_to_simp = TRADITIONAL_TO_SIMPLIFIED
        
        print(f"Dictionary loaded: {len(self.dictionary)} entries")
    
    def lookup(self, word: str, pinyin: Optional[str] = None) -> Optional[Dict]:
        """
        Look up a word in the dictionary.
        
        Args:
            word: The Chinese word to look up
            pinyin: Optional pinyin to disambiguate (if word has multiple pronunciations)
        
        Returns:
            Dictionary entry or None if not found
        """
        # Try direct lookup (traditional)
        if word in self.dictionary:
            entries = self.dictionary[word]
            
            # If pinyin provided, find matching entry
            if pinyin:
                for entry in entries:
                    if entry['pinyin'].lower() == pinyin.lower():
                        return entry
            
            # When no pinyin specified, prefer non-surname entries
            return self._get_preferred_entry(entries)
        
        # Try converting simplified to traditional and lookup
        if word in self.simp_to_trad:
            traditional = self.simp_to_trad[word]
            if traditional in self.dictionary:
                entries = self.dictionary[traditional]
                
                if pinyin:
                    for entry in entries:
                        if entry['pinyin'].lower() == pinyin.lower():
                            return entry
                
                # When no pinyin specified, prefer non-surname entries
                return self._get_preferred_entry(entries)
        
        return None
    
    def _get_preferred_entry(self, entries: List[Dict]) -> Optional[Dict]:
        """
        Get the preferred entry from a list of entries.
        
        Priority order:
        1. Lowercase pinyin (common words) over capitalized (proper nouns)
        2. Non-surname entries over surname entries
        3. First entry if all else equal
        
        Args:
            entries: List of dictionary entries
        
        Returns:
            The preferred entry, or None if list is empty
        """
        if not entries:
            return None
        
        # Separate entries by type
        lowercase_non_surname = []
        lowercase_surname = []
        capitalized_non_surname = []
        capitalized_surname = []
        
        for entry in entries:
            pinyin = entry.get('pinyin', '')
            definition = entry.get('definition', '').lower()
            is_surname = 'surname' in definition
            is_capitalized = pinyin and pinyin[0].isupper()
            
            if not is_capitalized:
                if not is_surname:
                    lowercase_non_surname.append(entry)
                else:
                    lowercase_surname.append(entry)
            else:
                if not is_surname:
                    capitalized_non_surname.append(entry)
                else:
                    capitalized_surname.append(entry)
        
        # Return in priority order
        if lowercase_non_surname:
            return lowercase_non_surname[0]
        if lowercase_surname:
            return lowercase_surname[0]
        if capitalized_non_surname:
            return capitalized_non_surname[0]
        if capitalized_surname:
            return capitalized_surname[0]
        
        # Fallback to first entry
        return entries[0]
    
    def lookup_all_variants(self, word: str) -> List[Dict]:
        """
        Look up all pronunciation variants of a word.
        
        Returns:
            List of all dictionary entries for this word
        """
        # Try direct lookup
        if word in self.dictionary:
            return self.dictionary[word]
        
        # Try converting simplified to traditional
        if word in self.simp_to_trad:
            traditional = self.simp_to_trad[word]
            if traditional in self.dictionary:
                return self.dictionary[traditional]
        
        return []
    
    def detect_script_type(self, text: str) -> str:
        """
        Detect if text is primarily simplified or traditional Chinese.
        
        Strategy:
        1. Count characters that exist only in simplified form
        2. Count characters that exist only in traditional form
        3. Return the type with more unique characters
        
        Returns:
            'simplified', 'traditional', or 'mixed'
        """
        if not text:
            return 'traditional'
        
        simp_only_count = 0
        trad_only_count = 0
        total_chinese_chars = 0
        
        for char in text:
            # Only check Chinese characters
            if not ('\u4e00' <= char <= '\u9fff'):
                continue
            
            total_chinese_chars += 1
            
            # Check if this character has a different form
            if char in self.simp_to_trad:
                traditional = self.simp_to_trad[char]
                if traditional != char:
                    simp_only_count += 1
            
            if char in self.trad_to_simp:
                simplified = self.trad_to_simp[char]
                if simplified != char:
                    trad_only_count += 1
        
        # If very few Chinese characters, default to traditional
        if total_chinese_chars < 5:
            return 'traditional'
        
        # Calculate ratios
        simp_ratio = simp_only_count / total_chinese_chars if total_chinese_chars > 0 else 0
        trad_ratio = trad_only_count / total_chinese_chars if total_chinese_chars > 0 else 0
        
        # If difference is small, consider it mixed
        if abs(simp_ratio - trad_ratio) < 0.1:
            return 'mixed'
        
        # Return the dominant type
        if simp_only_count > trad_only_count:
            return 'simplified'
        elif trad_only_count > simp_only_count:
            return 'traditional'
        else:
            # No clear distinction, default to traditional
            return 'traditional'
    
    def convert_to_traditional(self, text: str) -> str:
        """
        Convert simplified Chinese to traditional.
        Characters without mapping remain unchanged.
        """
        result = []
        for char in text:
            if char in self.simp_to_trad:
                result.append(self.simp_to_trad[char])
            else:
                result.append(char)
        return ''.join(result)
    
    def convert_to_simplified(self, text: str) -> str:
        """
        Convert traditional Chinese to simplified.
        Characters without mapping remain unchanged.
        """
        result = []
        for char in text:
            if char in self.trad_to_simp:
                result.append(self.trad_to_simp[char])
            else:
                result.append(char)
        return ''.join(result)
    
    def is_in_dictionary(self, word: str) -> bool:
        """
        Check if a word exists in the dictionary.
        Checks both traditional and simplified forms.
        """
        if word in self.dictionary:
            return True
        
        if word in self.simp_to_trad:
            traditional = self.simp_to_trad[word]
            if traditional in self.dictionary:
                return True
        
        return False
    
    def get_translation(self, word: str, pinyin: Optional[str] = None) -> Optional[str]:
        """
        Get the English translation for a word.
        
        If pinyin is specified, returns only that pronunciation's definition.
        If pinyin is not specified, returns combined definitions from all pronunciations,
        sorted by priority: common words → proper nouns → surnames.
        
        Returns:
            The definition string, or None if not found
        """
        # If specific pinyin requested, return only that one
        if pinyin:
            entry = self.lookup(word, pinyin)
            if entry:
                return entry['definition']
            return None
        
        # Otherwise, combine all entries sorted by priority
        all_entries = self.lookup_all_variants(word)
        if not all_entries:
            return None
        
        # Sort entries by priority
        sorted_entries = self._sort_entries_by_priority(all_entries)
        
        # Combine definitions from all entries
        return self._combine_definitions(sorted_entries)
    
    def _sort_entries_by_priority(self, entries: List[Dict]) -> List[Dict]:
        """
        Sort entries by priority:
        1. Lowercase pinyin, non-surname (common words)
        2. Capitalized pinyin, non-surname (proper nouns)
        3. Lowercase pinyin, surname
        4. Capitalized pinyin, surname
        """
        lowercase_non_surname = []
        capitalized_non_surname = []
        lowercase_surname = []
        capitalized_surname = []
        
        for entry in entries:
            pinyin = entry.get('pinyin', '')
            definition = entry.get('definition', '').lower()
            is_surname = 'surname' in definition
            is_capitalized = pinyin and pinyin[0].isupper()
            
            if not is_capitalized:
                if not is_surname:
                    lowercase_non_surname.append(entry)
                else:
                    lowercase_surname.append(entry)
            else:
                if not is_surname:
                    capitalized_non_surname.append(entry)
                else:
                    capitalized_surname.append(entry)
        
        # Combine in priority order
        return lowercase_non_surname + capitalized_non_surname + lowercase_surname + capitalized_surname
    
    def _combine_definitions(self, sorted_entries: List[Dict]) -> str:
        """
        Combine definitions from multiple entries (different pinyin variants).
        Parse each entry's definitions, track numbering, and combine without duplicates.
        """
        import re
        
        all_definitions = []
        seen_definitions = set()  # Track to avoid duplicates
        
        for entry in sorted_entries:
            definition_str = entry.get('definition', '')
            
            # Split by semicolon and numbered pattern (1. 2. 3. etc.)
            parts = re.split(r';\s*', definition_str)
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                
                # Remove leading number if present
                clean_part = re.sub(r'^\d+\.\s*', '', part)
                clean_part = clean_part.strip()
                
                # Normalize for comparison (lowercase, no extra spaces)
                normalized = clean_part.lower().strip()
                
                # Skip if we've seen this definition already
                if normalized in seen_definitions:
                    continue
                
                seen_definitions.add(normalized)
                all_definitions.append(clean_part)
        
        # Renumber all definitions sequentially
        if not all_definitions:
            return ''
        
        numbered = [f"{i+1}. {def_text}" for i, def_text in enumerate(all_definitions)]
        return '; '.join(numbered)
    
    def get_pinyin(self, word: str) -> Optional[str]:
        """
        Get the pinyin for a word.
        If word has multiple pronunciations, returns the first one.
        
        Returns:
            Pinyin string, or None if not found
        """
        entry = self.lookup(word)
        if entry:
            return entry['pinyin']
        return None
    
    def search_by_pinyin(self, pinyin: str) -> List[Tuple[str, Dict]]:
        """
        Search for words by pinyin.
        
        Returns:
            List of (word, entry) tuples matching the pinyin
        """
        results = []
        pinyin_lower = pinyin.lower().strip()
        
        for word, entries in self.dictionary.items():
            for entry in entries:
                if entry['pinyin'].lower() == pinyin_lower:
                    results.append((word, entry))
        
        return results
    
    def get_dictionary_stats(self) -> Dict:
        """
        Get statistics about the dictionary.
        """
        total_words = len(self.dictionary)
        total_entries = sum(len(entries) for entries in self.dictionary.values())
        words_with_multiple_pinyin = sum(1 for entries in self.dictionary.values() if len(entries) > 1)
        
        return {
            'total_words': total_words,
            'total_entries': total_entries,
            'words_with_multiple_pinyin': words_with_multiple_pinyin,
            'simplified_mappings': len(self.simp_to_trad),
            'traditional_mappings': len(self.trad_to_simp)
        }


# Create a singleton instance
dictionary_service = DictionaryService()

