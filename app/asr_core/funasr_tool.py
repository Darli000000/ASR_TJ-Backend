from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess


def recognize_audio_and_emotion(model_dir, audio_path, language="auto"):
    """
    使用 funasr 模型进行语音识别。

    :param model_dir: 模型文件夹路径
    :param audio_path: 输入音频文件路径
    :param language: 识别语言，默认为"auto"自动检测
    :return: 识别结果文本
    """
    # 初始化模型
    model = AutoModel(
        model=model_dir,
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",   # 或者 "cpu"，取决于是否有 GPU
    )

    # 进行语音识别
    res = model.generate(
        input=audio_path,
        cache={},
        language=language,
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        ban_emo_unk=False,
        merge_length_s=15,
    )

    # 后处理识别结果
    text = rich_transcription_postprocess(res[0]["text"])

    return text


def evaluate_emotion(model_dir, audio_path):
    model = AutoModel(model=model_dir)

    # wav_file = f"{model.model_path}/example/test.wav"
    wav_file = audio_path
    res = model.generate(wav_file, output_dir="./outputs", granularity="utterance", extract_embedding=False)
    print(res)

    return res
