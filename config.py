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
    {
        "keywords": ["がおー", "がお", "らいおん"],
        "image": "assets/images/fire.png",
        "sound": "assets/sounds/gao.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["にゃー", "にゃん", "ねこ"],
        "image": "assets/images/cat.png",
        "sound": "assets/sounds/nya.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["わんわん", "いぬ", "わん"],
        "image": "assets/images/dog.png",
        "sound": "assets/sounds/wan.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["えいっ", "きゅぴーん"],
        "image": "assets/images/beam.png",
        "sound": "assets/sounds/beam.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["ちちんぷいぷい", "まほう"],
        "image": "assets/images/hat.png",
        "sound": "assets/sounds/magic.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["へんしん"],
        "image": "assets/images/glasses.png",
        "sound": "assets/sounds/shakin.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["でんしゃ", "しゅっぱつ"],
        "image": "assets/images/train.png",
        "sound": "assets/sounds/train.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["ぴーぽー", "きゅうきゅうしゃ"],
        "image": "assets/images/police.png",
        "sound": "assets/sounds/police.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["おばけだぞー", "おばけ"],
        "image": "assets/images/ghost2.png",
        "sound": "assets/sounds/baa.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["おおきくなーれ", "おおきい"],
        "image": "assets/images/footprint.png",
        "sound": "assets/sounds/big.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["かちんこちん", "こおり"],
        "image": "assets/images/ice.png",
        "sound": "assets/sounds/freeze.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["おはよう", "おはよ"],
        "image": "assets/images/sun.png",
        "sound": "assets/sounds/rooster.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["おやすみ", "おやすみなさい"],
        "image": "assets/images/moon.png",
        "sound": "assets/sounds/sleep.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["はくしょん", "くしゃみ"],
        "image": "assets/images/confetti.png",
        "sound": "assets/sounds/sneeze.wav",
        "duration": 3.0,
    },
    {
        "keywords": ["おいしい", "オイシイ"],
        "image": "assets/images/heart.png",
        "sound": "assets/sounds/heart.wav",
        "duration": 3.0,
    },
]

POSE_TRIGGERS: List[Dict[str, Any]] = [
    {
        "name": "banzai",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            and lms["left_wrist"].y < lms["nose"].y
            and lms["right_wrist"].y < lms["nose"].y
        ),
        "image": "assets/images/sparkle.gif",
        "sound": "assets/sounds/sharan.wav",
        "duration": 2.0,
    },
    {
        "name": "airplane",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["left_shoulder"], "visibility", 0) > 0.5)
            and (getattr(lms["right_shoulder"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].y - lms["left_shoulder"].y) < 0.2
            and abs(lms["right_wrist"].y - lms["right_shoulder"].y) < 0.2
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
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].y - lms["nose"].y) < 0.15
            and abs(lms["right_wrist"].y - lms["nose"].y) < 0.15
            and abs(lms["left_wrist"].x - lms["right_wrist"].x) < 0.15
        ),
        "image": "assets/images/ghost.png",
        "sound": "assets/sounds/baa.wav",
        "duration": 3.0,
    },
    {
        "name": "rabbit",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["left_ear"], "visibility", 0) > 0.5)
            and (getattr(lms["right_ear"], "visibility", 0) > 0.5)
            and lms["left_wrist"].y < lms["left_ear"].y
            and lms["right_wrist"].y < lms["right_ear"].y
            and abs(lms["left_wrist"].x - lms["left_ear"].x) < 0.15
            and abs(lms["right_wrist"].x - lms["right_ear"].x) < 0.15
        ),
        "image": "assets/images/rabbit.png",
        "sound": "assets/sounds/rabbit.wav",
        "duration": 3.0,
    },
    {
        "name": "monkey",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["mouth_left"], "visibility", 0) > 0.5)
            and (getattr(lms["mouth_right"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].y - lms["mouth_left"].y) < 0.1
            and abs(lms["right_wrist"].y - lms["mouth_right"].y) < 0.1
            and abs(lms["left_wrist"].x - lms["mouth_left"].x) < 0.15
        ),
        "image": "assets/images/monkey.png",
        "sound": "assets/sounds/monkey.wav",
        "duration": 3.0,
    },
    {
        "name": "clap",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].x - lms["right_wrist"].x) < 0.1
            and abs(lms["left_wrist"].y - lms["right_wrist"].y) < 0.1
            and lms["left_wrist"].y > lms["nose"].y
            and lms["left_wrist"].y < lms["left_shoulder"].y
        ),
        "image": "assets/images/clap.png",
        "sound": "assets/sounds/clap.wav",
        "duration": 3.0,
    },
    {
        "name": "cheek",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["mouth_left"], "visibility", 0) > 0.5)
            and (getattr(lms["mouth_right"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].y - lms["mouth_left"].y) < 0.15
            and abs(lms["right_wrist"].y - lms["mouth_right"].y) < 0.15
            and abs(lms["left_wrist"].x - lms["right_wrist"].x) > 0.2
        ),
        "image": "assets/images/cheek.png",
        "sound": "assets/sounds/cheek.wav",
        "duration": 3.0,
    },
    {
        "name": "stretch",
        "condition": lambda lms: (
            (getattr(lms["left_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["right_wrist"], "visibility", 0) > 0.5)
            and (getattr(lms["nose"], "visibility", 0) > 0.5)
            and abs(lms["left_wrist"].x - lms["right_wrist"].x) > 0.6
            and lms["left_wrist"].y > lms["nose"].y
        ),
        "image": "assets/images/stretch.png",
        "sound": "assets/sounds/stretch.wav",
        "duration": 3.0,
    },
]
