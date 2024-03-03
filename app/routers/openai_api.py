#----------------------openai api后端-------------------------
from flask import Flask, render_template, request, jsonify
import requests

openai_api_bp = Blueprint('openai_api_bp', __name__)

@openai_api_bp.route('/generate', methods=['POST'])
def generate_text():
    data = request.json  # 从前端接收数据
    prompt = data['prompt']

    # 向 GPT-4 API 发送请求（替换 YOUR_API_KEY 为你的实际 API 密钥）
    headers = {
        'Authorization': 'Bearer YOUR_API_KEY'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': 100
    }
    response = requests.post('https://api.openai.com/v4/completions', json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json())  # 将 GPT-4 响应返回给前端
    else:
        return jsonify({'error': 'API 请求失败'}), 500
    
