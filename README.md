<h2>MODELSCOPE 语音模型集成调用后端</h2>

<h3>接口测试方法：</h3>
<h4>1、POST /asr/emotion_evaluate :</h4>
<p>情感分析接口，用modelscope调用emotion2vec_plus_large模型</p>
<p>curl -X POST http://localhost:5000/asr/emotion_evaluate -F "audio=@C:\Users\I750014\Documents\ASR-Project\FunASR\MYT0001.wav"</p>

<h4>1、POST /asr/comprehensive_recognition :</h4>
<p>语音与情感综合分析接口，用whisper调用语音识别模型，并用modelscope调用emotion2vec_plus_large模型</p>
<p>curl -X POST http://localhost:5000/asr/comprehensive_recognition -F "audio=@C:\Users\I750014\Documents\ASR-Project\FunASR\MYT0001.wav"</p>
<br>

<h3>注意：</h3>
<p>启动后端后需要先调用几次接口来加载模型，在git bash里输入上述相关的curl命令即可。可以直接测试第二个接口，可以一同加载两个模型，也可以先调用第一个接口，先加载情感模型，在调用第二个加载语音识别模型</p>
