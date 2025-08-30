#!/usr/bin/env python3
"""
Script to build an expanded Chinese character and phrase dictionary from text samples.
"""

import re
from collections import Counter
import sys
import os
import jieba

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.translation_service import TranslationService

def extract_chinese_characters(text):
    """Extract all Chinese characters from text"""
    # Chinese character range
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', text)
    return chinese_chars

def extract_chinese_phrases(text, min_length=2, max_length=6):
    """Extract Chinese phrases using jieba segmentation"""
    print("Segmenting text with jieba...")
    
    # Clean text - remove non-Chinese characters except basic punctuation
    cleaned_text = re.sub(r'[^\u4e00-\u9fff\s，。！？；：]', '', text)
    
    # Use jieba to segment
    words = jieba.cut(cleaned_text, cut_all=False)
    
    phrases = []
    for word in words:
        # Only keep Chinese phrases of reasonable length
        if (min_length <= len(word) <= max_length and 
            re.match(r'^[\u4e00-\u9fff]+$', word)):
            phrases.append(word)
    
    return phrases

def build_phrase_dictionary_from_text(text, top_phrases=300):
    """Build phrase dictionary from text sample (skip characters)"""
    
    # Extract phrases only
    print("Extracting Chinese phrases...")
    phrases = extract_chinese_phrases(text)
    print(f"Found {len(phrases)} total phrases")
    
    # Count frequencies
    phrase_counts = Counter(phrases)
    most_common_phrases = phrase_counts.most_common(top_phrases)
    
    print(f"\nTop {len(most_common_phrases)} most frequent phrases:")
    for phrase, count in most_common_phrases[:15]:  # Show top 15
        print(f"  {phrase}: {count} times")
    
    # Get translations
    translation_service = TranslationService()
    phrase_dictionary = {}
    
    # Translate phrases
    print(f"\nTranslating {len(most_common_phrases)} phrases...")
    for i, (phrase, count) in enumerate(most_common_phrases):
        try:
            translation = translation_service.translate(phrase)
            if translation and translation != phrase and translation.lower() != 'unknown':
                phrase_dictionary[phrase] = translation
                print(f"  {i+1}/{len(most_common_phrases)}: {phrase} -> {translation}")
            else:
                print(f"  {i+1}/{len(most_common_phrases)}: {phrase} -> [FAILED]")
        except Exception as e:
            print(f"  {i+1}/{len(most_common_phrases)}: {phrase} -> [ERROR: {e}]")
    
    return phrase_dictionary, phrase_counts

def generate_dictionary_code(dictionary, dict_name="character_dict"):
    """Generate Python dictionary code"""
    lines = [f"        {dict_name} = {{"]
    
    # Sort by key for better organization
    sorted_items = sorted(dictionary.items())
    
    for key, translation in sorted_items:
        # Escape single quotes in translation
        escaped_translation = translation.replace("'", "\\'")
        lines.append(f"            '{key}': '{escaped_translation}',")
    
    lines.append("        }")
    
    return "\n".join(lines)

def main():
    print("Chinese Phrase Dictionary Builder")
    print("=" * 40)
    print("(Skipping characters - focusing on phrases only)")
    
    # Check if text file provided
    if len(sys.argv) > 1:
        text_file = sys.argv[1]
        print(f"Reading text from: {text_file}")
        
        try:
            with open(text_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        print("Please provide text input:")
        print("Usage: python build_dictionary.py <text_file>")
        print("Or paste text below (Ctrl+D when done):")
        text = sys.stdin.read()
    
    if not text.strip():
        print("No text provided!")
        return
    
    # Build phrase dictionary only
    phrase_dict, phrase_counts = build_phrase_dictionary_from_text(text, top_phrases=300)
    
    print(f"\nResults:")
    print(f"  Phrases: {len(phrase_dict)}/{min(300, len(phrase_counts))} translated ({len(phrase_dict)/min(300, len(phrase_counts))*100:.1f}%)")
    
    # Generate code for phrase dictionary
    phrase_code = generate_dictionary_code(phrase_dict, "phrase_dict")
    
    # Save to file
    phrase_output_file = "expanded_phrase_dictionary.py"
    
    # Phrase dictionary
    with open(phrase_output_file, 'w', encoding='utf-8') as f:
        f.write("# Expanded Chinese Phrase Dictionary\n")
        f.write("# Generated automatically from text analysis\n\n")
        f.write("def get_expanded_phrase_dict():\n")
        f.write(phrase_code)
        f.write("\n        return phrase_dict\n")
    
    print(f"\nFile generated:")
    print(f"  Phrase dictionary: {phrase_output_file}")
    
    print(f"\nTo integrate:")
    print(f"  1. Add get_phrase_fallback() method to translation_service.py")
    print(f"  2. Update backend routes to check phrase dictionary for multi-character words")
    print(f"  3. Modify translation priority: phrase dict -> batch -> individual")
    
    # Show some statistics
    print(f"\nStatistics:")
    print(f"  Total unique phrases found: {len(phrase_counts)}")
    print(f"  Phrase translation success: {len(phrase_dict)}")
    print(f"  Translation success rate: {len(phrase_dict)/min(300, len(phrase_counts))*100:.1f}%")
    print(f"  Most common phrases: {list(phrase_counts.keys())[:10]}")
    
    # Show sample translations
    print(f"\nSample phrase translations:")
    for phrase, translation in list(phrase_dict.items())[:10]:
        print(f"  {phrase} -> {translation}")

if __name__ == "__main__":
    main()
