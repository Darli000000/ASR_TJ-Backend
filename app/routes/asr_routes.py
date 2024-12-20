from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
import os

from app.asr_core.funasr_tool import recognize_audio_and_emotion, evaluate_emotion

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
            return {'error': 'No audio file part'}, 400

        file = request.files['audio']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if not allowed_file(file.filename):
            return {'error': 'Invalid file type'}, 400

        # 保存上传的文件
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # 在这里调用语音识别工具
        # 先定义调用模型的路径
        model_dir_text = "iic/SenseVoiceSmall"
        model_dir_emotion = "iic/emotion2vec_plus_large"
        try:
            text = recognize_audio_and_emotion(model_dir_text, filepath)
            emotion = evaluate_emotion(model_dir_emotion, filepath)
        except Exception as e:
            return {'error': str(e)}, 500
        recognition_result = text

        return {'text': recognition_result, 'emotion': emotion}, 200

