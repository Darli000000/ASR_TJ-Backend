from flask_restx import Namespace, Resource, fields, Api
from flask import request, jsonify, Flask
import os

from app.asr_core.xinghuo_tool import voice_emotion_assistant

# 创建命名空间
llm_ns = Namespace('LLM', description='LLM related operations')

api = Api()

emotion_model = llm_ns.model('Emotion', {
    'emotion': fields.String(description='情感类别'),
    'score': fields.Float(description='情感得分')
})

request_model = llm_ns.model('EmotionRequest', {
    'text': fields.String(required=True, description='输入文本'),
    'emotion': fields.List(fields.Nested(emotion_model), required=True, description='情感数组')
})

@llm_ns.route('/voice_emotion_assistant', methods=['POST'])
class VoiceEmotionAssistant(Resource):
    @llm_ns.doc('VoiceEmotionAssistant')
    @llm_ns.expect(request_model)
    def post(self):
        try:
            # 获取 JSON 数据
            data = api.payload

            # 验证数据格式
            if not data or 'text' not in data or 'emotion' not in data:
                return {"error": "Invalid input format"}, 400

            # 提取参数
            text = data['text']  # 获取字符串
            emotions = data['emotion']  # 获取数组

            # 过滤主要情感：得分大于 0.1
            main_emotions = [f"{e['emotion']} ({e['score']:.2f})" for e in emotions if e['score'] > 0.1]

            # 将主要情感拼接成字符串
            emotion_str = ', '.join(main_emotions)

            # 调用其他函数示例
            result = voice_emotion_assistant(text, emotion_str)

            # 返回处理后的结果
            return {
                "text": text,
                "main_emotions": emotion_str,
                "result": result
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
