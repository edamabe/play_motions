"""プレイモーションのメインエントリーポイント."""

import queue

import cv2

from config import POSE_TRIGGERS, VOICE_TRIGGERS
from modules.effect_player import EffectPlayer
from modules.pose_detector import PoseDetector
from modules.voice_listener import VoiceListener


def main() -> None:
    """カメラからの映像を取得し、表示するメインループ."""
    # 各種モジュールの初期化
    pose_detector = PoseDetector()
    effect_player = EffectPlayer()
    voice_listener = VoiceListener()

    # 音声認識スレッドの開始
    voice_listener.start()

    # 1. Webカメラの起動
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("エラー: カメラを起動できませんでした。")
        return

    # カメラの解像度をHD (1280x720) または フルHD (1920x1080) に上げる要求を出す
    # ※お使いのWebカメラが対応している最大解像度が自動で適用されます
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # 2. フルスクリーン表示の設定
    window_name = "Play Motion"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    print("アプリを起動しました。終了するには ESC キーを押してください。")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("エラー: フレームを取得できませんでした。")
                break

            # 3. 鏡面モード（左右反転）
            frame = cv2.flip(frame, 1)

            # --- ポーズ検出 (ステップ2) ---
            pose_name = pose_detector.detect(frame)
            if pose_name:
                print(f"🎉 ポーズ検知！ トリガー発火: {pose_name}")
                # --- エフェクトの発動 (ステップ3) ---
                for trigger in POSE_TRIGGERS:
                    if trigger["name"] == pose_name:
                        effect_player.trigger_effect(
                            image_path=trigger["image"],
                            sound_path=trigger["sound"],
                            duration=trigger["duration"],
                        )
                        break

            # --- 音声認識の発火をチェック (ステップ4) ---
            try:
                # キューが空でないなら取得
                keyword = voice_listener.result_queue.get_nowait()
                print(f"🎤 音声検知！ トリガー発火: {keyword}")
                # config.py から該当するトリガーを検索して再生
                for trigger in VOICE_TRIGGERS:
                    if keyword in trigger.get("keywords", []):
                        effect_player.trigger_effect(
                            image_path=trigger["image"],
                            sound_path=trigger["sound"],
                            duration=trigger["duration"],
                        )
                        break
            except queue.Empty:
                pass

            # --- 画像の合成処理 (ステップ3) ---
            frame = effect_player.apply_effects(frame)

            # 映像の描画・表示
            cv2.imshow(window_name, frame)

            # 4. 安全停止処理 (ESCキー: ASCII 27 で処理中断)
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                print("終了します...")
                break
    finally:
        # リソースの解放
        voice_listener.close()
        effect_player.close()
        pose_detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
