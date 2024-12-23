import whisper

def recognize_audio(audio_path):
    """
    使用 modelscope pipeline 模型进行语音识别。

    :param audio_path: 输入音频文件路径

    :return: 识别结果文本
    """

    model = whisper.load_model("turbo")
    result = model.transcribe(audio_path)
    print(result["text"])

    return result["text"]
