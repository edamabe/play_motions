"""ポーズ判定モジュール."""

import os
import time
import urllib.request
from typing import Any, Dict, List, Optional

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ランドマークのインデックス定義
LANDMARK_NAMES = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
]


class PoseDetector:
    """MediaPipe Tasks APIによるポーズ判定とトリガー管理を行うクラス."""

    def __init__(self, triggers: List[Dict[str, Any]]) -> None:
        """PoseDetectorの初期化.

        Args:
            triggers: 有効にするポーズトリガーのリスト
        """
        self.triggers = triggers
        self.model_path = "models/pose_landmarker_lite.task"
        self._ensure_model_exists()

        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_poses=1,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

        self.last_pose_name: Optional[str] = None
        self.last_trigger_time: float = 0.0

    def _ensure_model_exists(self) -> None:
        """必要なモデルファイルが存在するか確認し、なければダウンロードする."""
        if not os.path.exists(self.model_path):
            print(f"モデルをダウンロードしています: {self.model_path} ...")
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task"
            urllib.request.urlretrieve(url, self.model_path)
            print("ダウンロード完了しました。")

    def detect(self, frame: Any) -> Optional[str]:
        """画像フレームからポーズを検出し、トリガー条件を満たした場合はポーズ名を返す.

        Args:
            frame: OpenCVの画像フレーム (BGR)

        Returns:
            条件を満たしたポーズの名前。何も満たしていない・クールダウン中ならNone。
        """
        # BGR画像をRGBに変換し、MediaPipeのImageオブジェクトを作成
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        # 検出の実行
        detection_result = self.detector.detect(mp_image)

        if not detection_result.pose_landmarks:
            return None

        # 最初の人物のランドマークを取得
        pose_landmarks = detection_result.pose_landmarks[0]

        # 全ランドマークを辞書化し、config.pyの条件式で使いやすくする
        landmarks_dict: Dict[str, Any] = {}
        for idx, landmark in enumerate(pose_landmarks):
            if idx < len(LANDMARK_NAMES):
                landmarks_dict[LANDMARK_NAMES[idx]] = landmark

        current_time = time.time()

        for trigger in self.triggers:
            name = trigger["name"]
            condition = trigger["condition"]
            duration = trigger["duration"]

            try:
                # 条件式を満たすか判定
                if condition(landmarks_dict):
                    # クールダウンの判定
                    if self.last_pose_name == name:
                        if (current_time - self.last_trigger_time) < duration:
                            # クールダウン中のため発火しない
                            return None

                    # トリガー発火
                    self.last_pose_name = name
                    self.last_trigger_time = current_time
                    return name
            except KeyError as e:
                # 必要なランドマークが存在しない場合はスキップ
                print(f"警告: ランドマークが取得できませんでした: {e}")
            except Exception as e:
                print(f"エラー: 条件評価中にエラーが発生しました: {e}")

        return None

    def close(self) -> None:
        """リソースの解放."""
        self.detector.close()
