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

@google_api_bp.route('/pronounce', methods=['GET'])
def pronounce():
    text = request.args.get('text', '')
    lang = request.args.get('lang', 'en')
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