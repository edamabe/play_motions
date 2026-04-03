"""設定ファイル."""

from typing import Any, Dict, List

VOICE_TRIGGERS: List[Dict[str, Any]] = [
    {
        "keywords": ["りんご", "いんご", "びんご", "みんご", "リンゴ"],
        "image": "assets/images/apple.png",
        "sound": "assets/sounds/pon.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["ぞうさん", "どうさん", "ぞう"],
        "image": "assets/images/elephant.png",
        "sound": "assets/sounds/pao.wav",
        "duration": 4.0,
    },
    {
        "keywords": ["くるま", "くーま", "ぶーぶー", "ぶぶ", "車"],
        "image": "assets/images/car.png",
        "sound": "assets/sounds/puu.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["まる", "えん", "まう", "丸", "円"],
        "image": "assets/images/circle.png",
        "sound": "assets/sounds/maru.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["さんかく", "たんかく", "三角"],
        "image": "assets/images/triangle.png",
        "sound": "assets/sounds/sankaku.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["しかく", "したく", "四角"],
        "image": "assets/images/square.png",
        "sound": "assets/sounds/shikaku.wav",
        "duration": 3.0,
    },
]

POSE_TRIGGERS: List[Dict[str, Any]] = [
    {
        "name": "banzai",
        "condition": lambda lms: (
            # 両手首と鼻がカメラに映っているか
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            # 両手首が鼻より上にきているか
            and lms["left_wrist"].y < lms["nose"].y
            and lms["right_wrist"].y < lms["nose"].y
        ),
        "image": "assets/images/sparkle.png",
        "sound": "assets/sounds/sharan.wav",
        "duration": 2.0,
    },
    {
        "name": "airplane",
        "condition": lambda lms: (
            # 必要なパーツが映っているか
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["left_shoulder"], "visibility", 0) > 0.5)
            and (getattr(lms["right_shoulder"], "visibility", 0) > 0.5)
            # 両手首がだいたい肩と同じくらいの高さ
            and abs(lms["left_wrist"].y - lms["left_shoulder"].y) < 0.2
            and abs(lms["right_wrist"].y - lms["right_shoulder"].y) < 0.2
            # 両手首間の水平距離が、両肩の距離よりも圧倒的に遠い（横に広げている）
            and abs(lms["left_wrist"].x - lms["right_wrist"].x)
            > abs(lms["left_shoulder"].x - lms["right_shoulder"].x) * 2.5
        ),
        "image": "assets/images/cloud.png",
        "sound": "assets/sounds/byun.wav",
        "duration": 3.0,
    },
    {
        "name": "hide_and_seek",
        "condition": lambda lms: (
            # 必要なパーツが映っているか
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            # 両手首が鼻の高さ付近にあるか
            and abs(lms["left_wrist"].y - lms["nose"].y) < 0.15
            and abs(lms["right_wrist"].y - lms["nose"].y) < 0.15
            # 両手首同士がとても近い（顔の前に集まっている）
            and abs(lms["left_wrist"].x - lms["right_wrist"].x) < 0.15
        ),
        "image": "assets/images/ghost.png",
        "sound": "assets/sounds/baa.wav",
        "duration": 3.0,
    },
]
