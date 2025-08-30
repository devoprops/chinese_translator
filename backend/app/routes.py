from flask import Blueprint, request, jsonify
from app.services.text_service import TextService
from app.services.translation_service import TranslationService
from app.services.pinyin_service import PinyinService

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



