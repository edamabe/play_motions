"""エフェクト管理モジュール."""

import time
from typing import Any, Dict, Optional

import cv2
import numpy as np
import pygame
from PIL import Image


class EffectPlayer:
    """画像の合成とPygameによる音声再生ロジックを管理するクラス."""

    def __init__(self) -> None:
        """EffectPlayerの初期化."""
        # Pygame mixerの初期化
        pygame.mixer.init()

        # キャッシュ辞書（ファイル読み込みのオーバーヘッドをなくすため）
        self.sounds_cache: Dict[str, pygame.mixer.Sound] = {}
        self.images_cache: Dict[str, Image.Image] = {}

        # 現在アクティブなエフェクトの状態管理
        self.active_image_path: Optional[str] = None
        self.effect_end_time: float = 0.0

    def trigger_effect(self, image_path: str, sound_path: str, duration: float) -> None:
        """トリガー発火時に呼び出され、効果音を鳴らし、画像を表示キューに入れる.

        Args:
            image_path: 表示する画像のパス
            sound_path: 再生する音声ファイルのパス
            duration: 表示期間 (秒)
        """
        # 音声の再生（遅延なく非同期で再生される）
        if sound_path:
            self.play_sound(sound_path)

        # 画像表示のセットアップ
        if image_path:
            self.active_image_path = image_path
            self.effect_end_time = time.time() + duration

    def play_sound(self, sound_path: str) -> None:
        """効果音を即座に再生する."""
        try:
            if sound_path not in self.sounds_cache:
                self.sounds_cache[sound_path] = pygame.mixer.Sound(sound_path)
            # 再生
            self.sounds_cache[sound_path].play()
        except Exception as e:
            print(f"音声の再生に失敗しました ({sound_path}): {e}")

    def apply_effects(self, frame_bgr: Any) -> Any:
        """現在のフレーム（BGR）にアクティブなエフェクト画像を合成して返す."""
        if not self.active_image_path or time.time() > self.effect_end_time:
            # エフェクトがアクティブでない場合はそのまま返す
            return frame_bgr

        try:
            # 画像のキャッシュ読み込み
            if self.active_image_path not in self.images_cache:
                # 透過情報を保持してRGBAで読み込む
                img = Image.open(self.active_image_path).convert("RGBA")
                self.images_cache[self.active_image_path] = img

            overlay_img = self.images_cache[self.active_image_path]

            # OpenCVのBGRフレームをPillow(RGBA)に変換
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(frame_rgb).convert("RGBA")

            # 画面の中央に配置するための座標計算
            f_width, f_height = pil_frame.size
            o_width, o_height = overlay_img.size

            # 画像が大きすぎる場合は少し縮小などの処理が必要ならここで行う
            # 今回はそのまま中央配置
            x = (f_width - o_width) // 2
            y = (f_height - o_height) // 2

            # 画像をアルファブレンド（透過合成）
            # 新しい透明なキャンバスを用意し、そこにベースとオーバーレイを描画
            canvas = Image.new("RGBA", pil_frame.size, (0, 0, 0, 0))
            canvas.paste(pil_frame, (0, 0))

            # オーバーレイが画面からはみ出ても安全にpaste可能
            canvas.paste(overlay_img, (x, y), overlay_img)

            # CV2用のBGR配列に戻す
            canvas_rgb = canvas.convert("RGB")
            new_frame_bgr = cv2.cvtColor(np.array(canvas_rgb), cv2.COLOR_RGB2BGR)

            return new_frame_bgr

        except Exception as e:
            print(f"画像合成に失敗しました ({self.active_image_path}): {e}")
            return frame_bgr

    def close(self) -> None:
        """リソースの解放."""
        pygame.mixer.quit()
