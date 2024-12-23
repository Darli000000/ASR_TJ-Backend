from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks


def recognize_audio(audio_path):
    """
    使用 modelscope pipeline 模型进行语音识别。

    :param model_dir: 模型文件夹路径
    :param audio_path: 输入音频文件路径

    :return: 识别结果文本
    """

    inference_pipeline = pipeline(
        task=Tasks.auto_speech_recognition,
        model='iic/SenseVoiceSmall',
        model_revision="master",
        device="cuda:0",
        disable_update=True,
    )

    input = audio_path

    res = inference_pipeline(input)
    # print(rec_result)

    # 后处理识别结果
    #text = rich_transcription_postprocess(res[0]["text"])

    return res[0]["text"]


def simplify_output(output):
    if not output or 'labels' not in output[0] or 'scores' not in output[0]:
        return {'error': 'Invalid input format'}

    labels = output[0]['labels']
    scores = output[0]['scores']

    # 将标签和分数组合成字典，并按分数降序排序
    result = sorted(
        [{'emotion': labels[i], 'score': scores[i]} for i in range(len(labels))],
        key=lambda x: x['score'],
        reverse=True
    )
    return result


def evaluate_emotion(audio_path):
    inference_pipeline = pipeline(
        task=Tasks.emotion_recognition,
        model="iic/emotion2vec_plus_large",
        # disable_update=True,
    )

    input_audio = audio_path

    rec_result = inference_pipeline(input=input_audio, granularity="utterance", extract_embedding=False)
    print(rec_result)

    result = simplify_output(rec_result)

    return result

def evaluate_emotion_raw(audio_path):
    inference_pipeline = pipeline(
        task=Tasks.emotion_recognition,
        model="iic/emotion2vec_plus_large",
        # disable_update=True,
    )

    input_audio = audio_path

    rec_result = inference_pipeline(input=input_audio, granularity="utterance", extract_embedding=False)
    print(rec_result)

    return rec_result
