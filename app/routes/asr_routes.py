from flask_restx import Namespace, Resource, fields
from flask import request, jsonify, Flask
import os

from app.asr_core.funasr_tool import evaluate_emotion, evaluate_emotion_raw
from app.asr_core.whisper_tool import recognize_audio

# 创建命名空间
asr_ns = Namespace('ASR', description='ASR related operations')

# 上传音频文件的请求数据模型
audio_upload_model = asr_ns.model('AudioUpload', {
    'audio': fields.Raw(required=True, description='Audio file', example='audio.wav')
})

# 配置上传文件夹
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'ogg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """检查文件类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 音频文件上传和识别的路由
@asr_ns.route('/recognize')
class AudioRecognition(Resource):
    @asr_ns.doc('recognize_audio')
    # @asr_ns.expect(audio_upload_model, validate=True)
    def post(self):
        """上传音频文件进行语音识别"""
        if 'audio' not in request.files:
            return {'error': 'No audio file part'}, 401

        file = request.files['audio']
        if file.filename == '':
            return {'error': 'No selected file'}, 402

        if not allowed_file(file.filename):
            return {'error': 'Invalid file type'}, 403

        # 保存上传的文件
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 在这里调用语音识别工具
        try:
            # text = "Link Success!!"
            emotion = "Happy!"
            # emotion = evaluate_emotion(filepath)
            text = recognize_audio(filepath)

        except Exception as e:
            return {'error': str(e)}, 500
        recognition_result = text

        return {'text': recognition_result, 'emotion': emotion}, 200


# 音频文件情感评估的路由
@asr_ns.route('/emotion_evaluate')
class EmotionRecognition(Resource):
    @asr_ns.doc('emotions_evaluate')
    # @asr_ns.expect(audio_upload_model, validate=True)
    def post(self):
        """音频文件上传和情感评估的路由"""
        if 'audio' not in request.files:
            return {'error': 'No audio file part'}, 401

        file = request.files['audio']
        if file.filename == '':
            return {'error': 'No selected file'}, 402

        if not allowed_file(file.filename):
            return {'error': 'Invalid file type'}, 403

        # 保存上传的文件
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 在这里调用语音识别工具
        try:
            # emotion = "Happy!"
            emotion = evaluate_emotion_raw(filepath)

        except Exception as e:
            return {'error': str(e)}, 500

        return {'message': '分析成功', 'result': emotion}, 200


# 音频文件文字识别和情感评估的路由
@asr_ns.route('/comprehensive_recognition')
class ComprehensiveRecognition(Resource):
    @asr_ns.doc('/comprehensive_recognition')
    # @asr_ns.expect(audio_upload_model, validate=True)
    def post(self):
        """音频文件文字识别和情感评估的路由"""
        if 'audio' not in request.files:
            return {'error': 'No audio file part'}, 401

        file = request.files['audio']
        if file.filename == '':
            return {'error': 'No selected file'}, 402

        if not allowed_file(file.filename):
            return {'error': 'Invalid file type'}, 403

        # 保存上传的文件
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 在这里调用语音识别工具
        try:
            # emotion = "Happy!"
            emotion = evaluate_emotion(filepath)
            text = recognize_audio(filepath)

        except Exception as e:
            return {'error': str(e)}, 500

        return {'text': text, 'emotion': emotion}, 200

