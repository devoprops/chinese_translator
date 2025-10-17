"""
Dictionary Processing Tool
Parses FG_word_list_full.txt and generates clean dictionary files for the application.

Handles:
- Duplicate entries (merges same pinyin, keeps different pinyin separate)
- Moves surname definitions to end
- Preserves frequency data
- Generates multiple output formats (Python dict, jieba userdict, stats)
"""

import pandas as pd
import json
import re
from collections import defaultdict
from typing import Dict, List, Tuple

def is_see_reference(definition: str) -> bool:
    """
    Check if a definition is just a "see" reference (cross-reference).
    Examples: "see 上聲|上声[shàng shēng]", "old variant of 以[yǐ]"
    Returns True if it's ONLY a reference, False if it has actual definitions.
    """
    clean_def = definition.strip().lower()
    
    # Patterns that indicate it's a reference-only entry
    reference_patterns = [
        r'^see\s+',  # "see ..."
        r'^old\s+variant\s+of\s+',  # "old variant of ..."
        r'^variant\s+of\s+',  # "variant of ..."
        r'^archaic\s+variant\s+of\s+',  # "archaic variant of ..."
        r'^same\s+as\s+',  # "same as ..."
        r'^also\s+written\s+',  # "also written ..."
    ]
    
    for pattern in reference_patterns:
        if re.match(pattern, clean_def):
            return True
    
    return False

def parse_definitions(definition_str: str) -> List[Tuple[str, bool, bool]]:
    """
    Parse definition string into list of (definition, is_surname, is_reference) tuples.
    Returns definitions and flags if they are surname entries or just references.
    """
    # Split by numbered definitions (1., 2., 3., etc.)
    parts = re.split(r'(?=\d+\.)', definition_str.strip())
    definitions = []
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Remove leading number and dot
        clean_def = re.sub(r'^\d+\.\s*', '', part)
        
        # Strip trailing semicolons and whitespace
        clean_def = clean_def.rstrip(';').strip()
        
        # Check if it's a surname definition
        is_surname = 'surname' in clean_def.lower()
        
        # Check if it's just a reference
        is_reference = is_see_reference(clean_def)
        
        definitions.append((clean_def, is_surname, is_reference))
    
    return definitions

def merge_definitions(definitions_list: List[str]) -> str:
    """
    Merge multiple definition strings, renumbering them sequentially.
    Move surname definitions to the end.
    Filter out reference-only entries (like "see ..." or "variant of ...").
    """
    all_defs = []
    surname_defs = []
    
    for def_str in definitions_list:
        parsed = parse_definitions(def_str)
        for def_text, is_surname, is_reference in parsed:
            # Skip reference-only entries
            if is_reference:
                continue
                
            if is_surname:
                surname_defs.append(def_text)
            else:
                all_defs.append(def_text)
    
    # Combine: regular definitions first, then surnames
    combined = all_defs + surname_defs
    
    # Renumber sequentially
    numbered = [f"{i+1}. {def_text}" for i, def_text in enumerate(combined)]
    
    return '; '.join(numbered) if numbered else ''

def process_dictionary(input_file: str, output_dir: str = 'backend/data'):
    """
    Process the FG word list and generate dictionary files.
    """
    print(f"Reading dictionary from {input_file}...")
    
    # Read CSV file
    df = pd.read_csv(input_file, sep='\t', names=['Word', 'Simplified', 'Traditional', 'Frequency', 'Pinyin', 'Definition'])
    
    # Skip header row
    df = df[1:]
    
    print(f"Loaded {len(df)} entries")
    
    # Data structures for processing
    word_entries = defaultdict(list)  # word -> list of entries
    simplified_to_traditional = {}
    traditional_to_simplified = {}
    
    # Group by word and pinyin
    stats = {
        'total_entries': len(df),
        'unique_words': 0,
        'entries_with_multiple_pinyin': 0,
        'merged_entries': 0,
        'surnames_moved': 0
    }
    
    print("Processing entries...")
    
    for idx, row in df.iterrows():
        word = str(row['Word']).strip()
        simplified = str(row['Simplified']).strip()
        traditional = str(row['Traditional']).strip()
        frequency = float(row['Frequency']) if pd.notna(row['Frequency']) else 0.0
        pinyin = str(row['Pinyin']).strip()
        definition = str(row['Definition']).strip()
        
        # Store conversion mappings (use traditional as primary)
        if simplified != traditional:
            simplified_to_traditional[simplified] = traditional
            traditional_to_simplified[traditional] = simplified
        
        # Use traditional as the primary key
        primary_word = traditional
        
        # Add to word entries
        word_entries[primary_word].append({
            'simplified': simplified,
            'traditional': traditional,
            'frequency': frequency,
            'pinyin': pinyin,
            'definition': definition
        })
    
    print("Merging duplicate entries...")
    
    # Process entries to merge duplicates with same pinyin
    final_dictionary = {}
    
    for word, entries in word_entries.items():
        # Group by pinyin
        pinyin_groups = defaultdict(list)
        for entry in entries:
            pinyin_groups[entry['pinyin']].append(entry)
        
        # Process each pinyin group
        word_definitions = []
        for pinyin, pinyin_entries in pinyin_groups.items():
            # Use the first entry's metadata
            first_entry = pinyin_entries[0]
            
            if len(pinyin_entries) > 1:
                # Merge definitions
                definitions = [e['definition'] for e in pinyin_entries]
                merged_def = merge_definitions(definitions)
                stats['merged_entries'] += 1
            else:
                # Single entry, check if surnames need moving and filter references
                parsed_defs = parse_definitions(first_entry['definition'])
                
                # Filter out reference-only entries
                valid_defs = [(d, is_s) for d, is_s, is_ref in parsed_defs if not is_ref]
                
                # Skip if no valid definitions remain after filtering
                if not valid_defs:
                    continue
                
                has_surname = any(is_surname for _, is_surname in valid_defs)
                
                if has_surname:
                    # Reorder to move surnames to end
                    regular_defs = [d for d, is_s in valid_defs if not is_s]
                    surname_defs = [d for d, is_s in valid_defs if is_s]
                    all_defs = regular_defs + surname_defs
                    merged_def = '; '.join([f"{i+1}. {d}" for i, d in enumerate(all_defs)])
                    stats['surnames_moved'] += 1
                else:
                    # Extract just the definition text (first element of tuple)
                    just_defs = [d for d, _ in valid_defs]
                    # If original had numbered format, keep it; otherwise use as-is
                    if len(just_defs) > 1 or first_entry['definition'].strip().startswith('1.'):
                        merged_def = '; '.join([f"{i+1}. {d}" for i, d in enumerate(just_defs)])
                    else:
                        merged_def = first_entry['definition']
            
            # Skip if merged definition is empty (all were references)
            if not merged_def or not merged_def.strip():
                continue
            
            word_definitions.append({
                'pinyin': pinyin,
                'definition': merged_def,
                'frequency': first_entry['frequency'],
                'simplified': first_entry['simplified']
            })
        
        # Only add to dictionary if there are valid definitions
        if word_definitions:
            final_dictionary[word] = word_definitions
            
            if len(word_definitions) > 1:
                stats['entries_with_multiple_pinyin'] += 1
    
    stats['unique_words'] = len(final_dictionary)
    
    print(f"Processed {stats['unique_words']} unique words")
    print(f"Merged {stats['merged_entries']} duplicate entries")
    print(f"Moved surnames in {stats['surnames_moved']} entries")
    
    # Generate output files
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Generate Python dictionary file
    print(f"\nGenerating {output_dir}/local_dictionary.py...")
    generate_python_dict(final_dictionary, simplified_to_traditional, traditional_to_simplified, 
                        f"{output_dir}/local_dictionary.py")
    
    # 2. Generate jieba userdict file
    print(f"Generating {output_dir}/jieba_userdict.txt...")
    generate_jieba_dict(final_dictionary, f"{output_dir}/jieba_userdict.txt")
    
    # 3. Generate statistics file
    print(f"Generating {output_dir}/dictionary_stats.json...")
    with open(f"{output_dir}/dictionary_stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print("\n[+] Dictionary processing complete!")
    print(f"   - Python dictionary: {output_dir}/local_dictionary.py")
    print(f"   - Jieba userdict: {output_dir}/jieba_userdict.txt")
    print(f"   - Statistics: {output_dir}/dictionary_stats.json")
    
    return final_dictionary, stats

def generate_python_dict(dictionary: Dict, simp_to_trad: Dict, trad_to_simp: Dict, output_file: str):
    """Generate Python dictionary file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('"""\n')
        f.write('Local Dictionary - Generated from FG_word_list_full.txt\n')
        f.write('This file contains the primary translation dictionary for the application.\n')
        f.write('"""\n\n')
        
        # Write main dictionary
        f.write('DICTIONARY = {\n')
        for word, entries in sorted(dictionary.items()):
            f.write(f"    '{word}': [\n")
            for entry in entries:
                f.write(f"        {{\n")
                f.write(f"            'pinyin': '{entry['pinyin']}',\n")
                f.write(f"            'definition': '''{entry['definition']}''',\n")
                f.write(f"            'frequency': {entry['frequency']},\n")
                f.write(f"            'simplified': '{entry['simplified']}'\n")
                f.write(f"        }},\n")
            f.write(f"    ],\n")
        f.write('}\n\n')
        
        # Write conversion mappings
        f.write('SIMPLIFIED_TO_TRADITIONAL = {\n')
        for simp, trad in sorted(simp_to_trad.items()):
            f.write(f"    '{simp}': '{trad}',\n")
        f.write('}\n\n')
        
        f.write('TRADITIONAL_TO_SIMPLIFIED = {\n')
        for trad, simp in sorted(trad_to_simp.items()):
            f.write(f"    '{trad}': '{simp}',\n")
        f.write('}\n')

def generate_jieba_dict(dictionary: Dict, output_file: str):
    """
    Generate jieba userdict file.
    Format: word frequency pinyin (space-separated)
    Higher frequency = higher priority in segmentation
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, entries in sorted(dictionary.items(), key=lambda x: -max(e['frequency'] for e in x[1])):
            # Use the highest frequency for this word
            max_freq = max(e['frequency'] for e in entries)
            # Convert frequency to integer for jieba (scale up)
            freq_int = int(max_freq * 1000)
            
            # Use first entry's pinyin (or combine if multiple)
            pinyin = entries[0]['pinyin']
            
            f.write(f"{word} {freq_int} {pinyin}\n")
            
            # Also add simplified version if different
            simplified = entries[0]['simplified']
            if simplified != word:
                f.write(f"{simplified} {freq_int} {pinyin}\n")

if __name__ == '__main__':
    import sys
    
    input_file = 'FG_word_list_full.txt'
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    try:
        dictionary, stats = process_dictionary(input_file)
        print(f"\n[i] Statistics:")
        print(f"   Total entries processed: {stats['total_entries']}")
        print(f"   Unique words: {stats['unique_words']}")
        print(f"   Words with multiple pinyin: {stats['entries_with_multiple_pinyin']}")
        print(f"   Merged duplicate entries: {stats['merged_entries']}")
        print(f"   Surnames repositioned: {stats['surnames_moved']}")
    except Exception as e:
        print(f"\n[!] Error processing dictionary: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

