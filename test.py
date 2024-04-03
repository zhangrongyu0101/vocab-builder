# import requests

# def test_translate():
#     url = "http://localhost:5000/translate_details"
#     params = {
#         'text': 'Hello',
#         'source': 'en',
#         'target': 'zh-CN'
#     }
#     response = requests.get(url, params=params)
#     print("Status Code:", response.status_code)
#     print("Response Body:", response.json())

# if __name__ == "__main__":
#     test_translate()


response_body = [
    [['你好', 'Hello', None, None, 10]], 
    None, 
    'en', 
    None, 
    None, 
    [['Hello', None, [['你好', 1000, True, False, [10, 3], None, [[3]]], ['您好', 1000, True, False, [10]], ['喂', 0, True, False, [8]]], [[0, 5]], 'Hello', 0, 0]], 
    None, 
    [], 
    None, 
    None, 
    None, 
    None, 
    [['exclamation', [['used as a greeting or to begin a phone conversation.', 'm_en_gbus0460730.012', 'hello there, Katie!']], 
      'hello', 17], ['noun', [['an utterance of “hello”; a greeting.', 
                            
                            'm_en_gbus0460730.025', 'she was getting polite nods and hellos from people']], 'hello', 1], ['verb', [['say or shout “hello”; greet someone.', 'm_en_gbus0460730.034', 'I pressed the phone button and helloed']], 'hello', 2]]]

# 初始化结果字典
result = {
    'translations': [],
    'definitions': []
}

# 提取基本翻译
for item in response_body[0]:
    result['translations'].append({'text': item[1], 'score': item[4]})

# 提取额外翻译选项
additional_translations = response_body[5][0][2]
for translation in additional_translations:
    result['translations'].append({'text': translation[0], 'score': translation[1]})

# 提取词性、定义和例句
definitions_section = response_body[-1]  # 修正后直接定位到最后一个元素，即包含定义的部分
for part_of_speech_info in definitions_section:
    part_of_speech = part_of_speech_info[0]
    for definition_detail in part_of_speech_info[1]:
        definition_text = definition_detail[0]
        examples = definition_detail[1] if len(definition_detail) > 1 else []
        for example_detail in examples:
            example_text = example_detail if example_detail else "No example available."
            result['definitions'].append({
                'part_of_speech': part_of_speech,
                'definition': definition_text,
                'example': example_text
            })

# 打印结果以验证
print("Translations:")
for translation in result['translations']:
    print(f" - {translation['text']} (Score: {translation['score']})")

print("\nDefinitions:")
for definition in result['definitions']:
    print(f" - Part of Speech: {definition['part_of_speech']}, Definition: {definition['definition']}, Example: {definition['example']}")

