#----------------------谷歌api后端-------------------------
from flask import current_app
from flask import Blueprint, request, jsonify, Response
import requests

google_api_bp = Blueprint('google_api_bp', __name__)

# 定义Google翻译API的URL

GOOGLE_TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
GOOGLE_TTS_URL = "http://translate.google.com/translate_tts"


@google_api_bp.route('/translate', methods=['GET'])
def translate():
    text = request.args.get('text', '')
    # 设置源语言为英文
    source = 'en'
    # 设置目标语言为简体中文
    target = 'zh-CN'
    params = {
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': 't',
        'q': text,
    }
    
    # 定义代理配置
    proxies = current_app.config['PROXIES']
    
    try:
        response = requests.get(GOOGLE_TRANSLATE_URL, params=params, proxies=proxies)
        response.raise_for_status()
        # 简化响应处理，直接返回第一个翻译结果
        translation = response.json()[0][0][0]
        return jsonify({'translation': translation})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

@google_api_bp.route('/translate_details', methods=['GET'])
def translate_details():
    text = request.args.get('text', '')
    source = 'en'  # 设置源语言为英文
    target = 'zh-CN'  # 设置目标语言为简体中文
    params = {
        'client': 'gtx',
        'sl': source,
        'tl': target,
        'dt': ['t', 'at', 'md', 'ex'],  # 请求基本翻译、额外翻译、定义、例句
        'q': text,
    }
    proxies = current_app.config['PROXIES']
    
    try:
        # response = requests.get(GOOGLE_TRANSLATE_URL, params=params, proxies=proxies)
        # response.raise_for_status()
        # # 这里你可能需要解析响应体以提取详细的翻译、定义和例句
        # translation_data = response.json()
        # # 处理和提取需要的数据
        response = requests.get(GOOGLE_TRANSLATE_URL, params=params, proxies=proxies)
        response.raise_for_status()
        # 解析响应体以提取详细的翻译、定义和例句
        translation_data = (response.json())
        
        return jsonify(translation_data)  # 返回JSON响应
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
def parse_translation_response(data):
    # 初始化结果字典
    result = {
        'translations': [],
        'definitions': []
    }
    
    # 提取基本翻译内容
    if data[0]:
        for item in data[0]:
            result['translations'].append({'text': item[0], 'score': item[4]})

    # 提取额外的翻译选项
    additional_translations = data[5][0][2] if len(data) > 5 and data[5] and data[5][0] and len(data[5][0]) > 2 else []
    for translation in additional_translations:
        result['translations'].append({'text': translation[0], 'score': translation[1]})

    # 提取词性、定义和例句
    if data[7]:
        for part_of_speech_info in data[7]:
            part_of_speech = part_of_speech_info[0]
            for definition_detail in part_of_speech_info[1]:
                definition = definition_detail[0]
                example = definition_detail[2] if len(definition_detail) > 2 else "No example available."
                result['definitions'].append({
                    'part_of_speech': part_of_speech,
                    'definition': definition,
                    'example': example
                })
                
    return result
@google_api_bp.route('/pronounce', methods=['GET'])
def pronounce():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'en-GB')
    params = {
        'client': 'tw-ob',
        'ie': 'UTF-8',
        'tl': lang,
        'q': text,
    }
    try:
        response = requests.get(GOOGLE_TTS_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        # 直接返回音频数据
        return Response(response.content, mimetype='audio/mpeg')
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500
    
    
@google_api_bp.route('/spell', methods=['GET'])
def spell():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'en-GB')
    spelled_text = ' '.join(text)  # Insert spaces between each character

    params = {
        'client': 'tw-ob',
        'ie': 'UTF-8',
        'tl': lang,
        'q': spelled_text,
    }

    try:
        response = requests.get(GOOGLE_TTS_URL, params=params, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return Response(response.content, mimetype='audio/mpeg')
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500