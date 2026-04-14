"""音声認識モジュール."""

import json
import queue
import threading
from typing import Any, Optional

import pyaudio
from vosk import KaldiRecognizer, Model


class VoiceListener:
    """Voskによる音声認識を別スレッドで管理するクラス."""

    def __init__(
        self, triggers: list[dict[str, Any]], model_path: str = "models/vosk-model-ja"
    ) -> None:
        """VoiceListenerの初期化.

        Args:
            triggers: 有効にする音声トリガーのリスト
            model_path: Vosk用言語モデルの配置ディレクトリ
        """
        self.triggers = triggers
        self.model_path = model_path
        self.running = False
        self.result_queue: queue.Queue[str] = queue.Queue()
        self.thread: Optional[threading.Thread] = None
        self.audio = pyaudio.PyAudio()

    def start(self) -> None:
        """バックグラウンドスレッドで音声認識ループを開始する."""
        if self.running:
            return

        print("Voskモデルをロードしています...(数秒かかります)")
        try:
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
        except Exception as e:
            print(f"警告: Voskモデルの読み込みに失敗しました: {e}")
            return

        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self) -> None:
        """音声ストリームから継続的に音声を認識するループ."""
        try:
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000,
            )
            stream.start_stream()
            print("マイクの音声認識を開始しました！「りんご」と言ってみてください。")

            while self.running:
                data = stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    # 結果が確定したタイミング
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        self._evaluate_text(text)
                else:
                    # 部分的な結果（リアルタイム性を高めるため、部分結果でもチェック）
                    partial = json.loads(self.recognizer.PartialResult())
                    text = partial.get("partial", "")
                    if text:
                        self._evaluate_text(text)

        except Exception as e:
            print(f"音声認識ループでエラーが発生しました: {e}")
        finally:
            if "stream" in locals() and stream.is_active():
                stream.stop_stream()
                stream.close()

    def _evaluate_text(self, text: str) -> None:
        """認識されたテキストからトリガーワードを探し、あればキューに送る."""
        text = text.replace(" ", "")  # Voskの出力には空白が含まれることがあるため除去
        for trigger in self.triggers:
            for keyword in trigger.get("keywords", []):
                if keyword in text:
                    # キューに追加してメインスレッドに通知する
                    self.result_queue.put(keyword)
                    # 連続発火を防ぐためRecognizerをリセット
                    self.recognizer.Reset()
                    return

    def close(self) -> None:
        """スレッドとリソースを安全に終了させる."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self.audio.terminate()
