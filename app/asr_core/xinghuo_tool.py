import requests
import json

prompt = "你好吗？"

def voice_emotion_assistant(text, emotion):
    url = "https://spark-api-open.xf-yun.com/v1/chat/completions"

    prompt = f"请根据我提供的聊天语句和说话时的情感为我生成答复。这是我的聊天语句:{text};这是我说话时的情感(以及对应的分数):{emotion}。"

    data = {
        "max_tokens": 4096,
        "top_k": 4,
        "temperature": 0.5,
        "messages": [
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "4.0Ultra"
    }
    data["stream"] = True
    header = {
        "Authorization": "Bearer JWRyODlzPvjFWnNQuiwK:cQaFQeYakyjiVwjEuEsr"
    }
    response = requests.post(url, headers=header, json=data, stream=True)

    # 流式响应解析
    response.encoding = "utf-8"
    full_content = ""
    for line in response.iter_lines(decode_unicode="utf-8"):
        if line.startswith("data: "):
            # 提取每一行的内容
            data = line[len("data: "):]
            # print('Data:', data)

            if data == '[DONE]':
                break

            # 将每一行的数据转换成字典并提取 'content' 字段
            json_data = json.loads(data)
            for choice in json_data.get("choices", []):
                content = choice.get("delta", {}).get("content", "")
                # print('Content:', content)
                full_content += content

    print(full_content)

    return full_content

