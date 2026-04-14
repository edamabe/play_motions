"""プレイモーションのメインエントリーポイント."""

import queue
import tkinter as tk
from tkinter import ttk

import cv2

from config import POSE_TRIGGERS, VOICE_TRIGGERS
from modules.effect_player import EffectPlayer
from modules.pose_detector import PoseDetector
from modules.voice_listener import VoiceListener


def select_active_triggers():
    """Tkinterを使用してユーザーに有効にするアクションを選択させる."""
    root = tk.Tk()
    root.title("Play Motion - アクション選択")
    root.geometry("400x500")

    # 説明ラベル
    ttk.Label(root, text="有効にしたいアクションにチェックを入れてください").pack(
        pady=10
    )

    # スクロール可能なフレームの作成
    canvas = tk.Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10)
    scrollbar.pack(side="right", fill="y")

    pose_vars = {}
    voice_vars = {}

    # ポーズトリガーのチェックボックス
    ttk.Label(
        scrollable_frame, text="【ポーズ アクション】", font=("", 10, "bold")
    ).pack(anchor="w", pady=(10, 5))
    for trigger in POSE_TRIGGERS:
        name = trigger["name"]
        var = tk.BooleanVar(value=True)
        pose_vars[name] = var
        ttk.Checkbutton(scrollable_frame, text=name, variable=var).pack(
            anchor="w", padx=20
        )

    # 音声トリガーのチェックボックス
    ttk.Label(scrollable_frame, text="【音声 アクション】", font=("", 10, "bold")).pack(
        anchor="w", pady=(15, 5)
    )
    for trigger in VOICE_TRIGGERS:
        label = ", ".join(trigger["keywords"])
        var = tk.BooleanVar(value=True)
        voice_vars[id(trigger)] = var
        ttk.Checkbutton(scrollable_frame, text=label, variable=var).pack(
            anchor="w", padx=20
        )

    result_pose = []
    result_voice = []

    def on_start():
        nonlocal result_pose, result_voice
        result_pose = [t for t in POSE_TRIGGERS if pose_vars[t["name"]].get()]
        result_voice = [t for t in VOICE_TRIGGERS if voice_vars[id(t)].get()]
        root.destroy()

    ttk.Button(root, text="この構成でスタート！", command=on_start).pack(pady=10)

    # ウィンドウを画面中央に表示
    root.update_idletasks()
    width = 400
    height = 500
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.mainloop()

    return result_pose, result_voice


def main() -> None:
    """カメラからの映像を取得し、表示するメインループ."""

    # ユーザーがGUIから有効にするトリガーを選択する
    active_pose_triggers, active_voice_triggers = select_active_triggers()

    # 全く選ばれずにウィンドウを閉じた場合のフェイルセーフ
    if not active_pose_triggers and not active_voice_triggers:
        print("アクションが選択されなかったため、アプリを終了します。")
        return

    # 各種モジュールの初期化（選択されたトリガーのみを渡す）
    pose_detector = PoseDetector(triggers=active_pose_triggers)
    effect_player = EffectPlayer()
    voice_listener = VoiceListener(triggers=active_voice_triggers)

    # 音声認識スレッドの開始
    voice_listener.start()

    # 1. Webカメラの起動
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("エラー: カメラを起動できませんでした。")
        return

    # カメラの解像度をHD (1280x720) または フルHD (1920x1080) に上げる要求を出す
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

            # --- ポーズ検出 ---
            pose_name = pose_detector.detect(frame)
            if pose_name:
                print(f"🎉 ポーズ検知！ トリガー発火: {pose_name}")
                for trigger in active_pose_triggers:
                    if trigger["name"] == pose_name:
                        effect_player.trigger_effect(
                            image_path=trigger["image"],
                            sound_path=trigger["sound"],
                            duration=trigger["duration"],
                        )
                        break

            # --- 音声認識の発火をチェック ---
            try:
                # キューが空でないなら取得
                keyword = voice_listener.result_queue.get_nowait()
                print(f"🎤 音声検知！ トリガー発火: {keyword}")
                for trigger in active_voice_triggers:
                    if keyword in trigger.get("keywords", []):
                        effect_player.trigger_effect(
                            image_path=trigger["image"],
                            sound_path=trigger["sound"],
                            duration=trigger["duration"],
                        )
                        break
            except queue.Empty:
                pass

            # --- 画像の合成処理 ---
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
