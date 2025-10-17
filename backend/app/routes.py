from flask import Blueprint, request, jsonify
from app.services.text_service import TextService
from app.services.translation_service import TranslationService
from app.services.pinyin_service import PinyinService
from app.services.dictionary_service import dictionary_service

api_bp = Blueprint('api', __name__)
text_service = TextService()
translation_service = TranslationService()
pinyin_service = PinyinService()

@api_bp.route('/text/<text_id>', methods=['GET'])
def get_text(text_id):
    """Get text content by ID"""
    try:
        text_data = text_service.get_text_by_id(text_id)
        return jsonify(text_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/translate', methods=['POST'])
def translate_text():
    """Translate Chinese text to English"""
    try:
        data = request.get_json()
        chinese_text = data.get('text', '')
        
        if not chinese_text:
            return jsonify({'error': 'No text provided'}), 400
        
        translation = translation_service.translate(chinese_text)
        return jsonify({'translation': translation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/translate-word', methods=['POST'])
def translate_word():
    """Translate a single Chinese word to English"""
    try:
        data = request.get_json()
        word = data.get('word', '')
        
        if not word:
            return jsonify({'error': 'No word provided'}), 400
        
        translation = translation_service.translate(word)
        return jsonify({'translation': translation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/translate-batch', methods=['POST'])
def translate_batch():
    """Translate multiple Chinese words/characters in one API call"""
    try:
        data = request.get_json()
        items = data.get('items', [])
        
        print(f"Batch translation request received for {len(items)} items: {items}")
        
        if not items:
            return jsonify({'error': 'No items provided'}), 400
        
        # Step 1: First try local dictionaries (fastest)
        translations = {}
        dictionary_hits = []
        needs_translation = []
        
        for item in items:
            if len(item) == 1 and '\u4e00' <= item <= '\u9fff':
                # Single character - try character dictionary first
                dict_result = translation_service.get_character_fallback(item)
                if dict_result != 'Unknown':
                    translations[item] = dict_result
                    dictionary_hits.append(item)
                    print(f"Character dictionary hit: '{item}' -> '{dict_result}'")
                else:
                    needs_translation.append(item)
            else:
                # Multi-character word - try phrase dictionary first
                phrase_result = translation_service.get_phrase_fallback(item)
                if phrase_result != 'Unknown':
                    translations[item] = phrase_result
                    dictionary_hits.append(item)
                    print(f"Phrase dictionary hit: '{item}' -> '{phrase_result}'")
                else:
                    needs_translation.append(item)
        
        print(f"Dictionary resolved {len(dictionary_hits)} items, need translation for {len(needs_translation)} items")
        
        # Step 2: Batch translate remaining items (efficient)
        if needs_translation:
            csv_text = ', '.join(needs_translation)
            print(f"CSV text to translate: {csv_text}")
            
            batch_translation = translation_service.translate(csv_text)
            print(f"Batch translation result: {batch_translation}")
            
            if batch_translation:
                # Parse CSV response
                translated_parts = [part.strip() for part in batch_translation.split(',')]
                print(f"Parsed translation parts: {translated_parts}")
                
                # Map batch results to original items
                batch_failures = []
                for i, item in enumerate(needs_translation):
                    if i < len(translated_parts):
                        batch_result = translated_parts[i]
                        # Check if batch translation is meaningful
                        if batch_result and batch_result != item and batch_result.lower() not in ['unknown', item.lower()]:
                            translations[item] = batch_result
                            print(f"Batch success: '{item}' -> '{batch_result}'")
                        else:
                            # Batch failed for this item
                            batch_failures.append(item)
                            print(f"Batch failed for: '{item}' (got '{batch_result}')")
                    else:
                        # Not enough parts in batch response
                        batch_failures.append(item)
                        print(f"Batch incomplete for: '{item}'")
                
                # Step 3: Individual translation for remaining failures (last resort)
                if batch_failures:
                    print(f"Need individual translation for {len(batch_failures)} items: {batch_failures}")
                    
                    for item in batch_failures:
                        try:
                            individual_translation = translation_service.translate(item)
                            print(f"Individual fallback: '{item}' -> '{individual_translation}'")
                            
                            if individual_translation and individual_translation != item and individual_translation.lower() != 'unknown':
                                translations[item] = individual_translation
                            else:
                                translations[item] = 'Unknown'
                        except Exception as e:
                            print(f"Error in individual translation for '{item}': {e}")
                            translations[item] = 'Unknown'
            else:
                # Batch translation completely failed, try individual for all
                print("Batch translation failed, trying individual translations")
                for item in needs_translation:
                    try:
                        individual_translation = translation_service.translate(item)
                        print(f"Individual translation: '{item}' -> '{individual_translation}'")
                        translations[item] = individual_translation or 'Unknown'
                    except Exception as e:
                        print(f"Error in individual translation for '{item}': {e}")
                        translations[item] = 'Unknown'
        
        print(f"Final translations mapping: {translations}")
        return jsonify({'translations': translations})
    except Exception as e:
        print(f"Batch translation error: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/pinyin', methods=['POST'])
def generate_pinyin():
    """Generate pinyin for Chinese text"""
    try:
        data = request.get_json()
        chinese_text = data.get('text', '')
        
        if not chinese_text:
            return jsonify({'error': 'No text provided'}), 400
        
        pinyin = pinyin_service.generate_pinyin(chinese_text)
        return jsonify({'pinyin': pinyin})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/characters/<char>', methods=['GET'])
def get_character_info(char):
    """Get detailed information about a Chinese character"""
    try:
        char_info = text_service.get_character_info(char)
        return jsonify(char_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """Comprehensive text analysis including translation and pinyin"""
    try:
        data = request.get_json()
        chinese_text = data.get('text', '')
        
        if not chinese_text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get all analysis in parallel
        pinyin = pinyin_service.generate_pinyin(chinese_text)
        translation = translation_service.translate(chinese_text)
        char_analysis = text_service.analyze_characters(chinese_text)
        
        return jsonify({
            'original': chinese_text,
            'pinyin': pinyin,
            'translation': translation,
            'character_analysis': char_analysis
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/detect-script', methods=['POST'])
def detect_script():
    """Detect if text is simplified or traditional Chinese"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        script_type = dictionary_service.detect_script_type(text)
        return jsonify({'scriptType': script_type})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/convert-script', methods=['POST'])
def convert_script():
    """Convert between simplified and traditional Chinese"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        to_type = data.get('toType', 'traditional')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if to_type == 'traditional':
            converted = dictionary_service.convert_to_traditional(text)
        elif to_type == 'simplified':
            converted = dictionary_service.convert_to_simplified(text)
        else:
            return jsonify({'error': 'Invalid conversion type. Use "traditional" or "simplified"'}), 400
        
        return jsonify({'convertedText': converted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/dictionary/stats', methods=['GET'])
def get_dictionary_stats():
    """Get statistics about the loaded dictionary"""
    try:
        stats = dictionary_service.get_dictionary_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



