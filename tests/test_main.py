"""Mainのテスト用モジュール."""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_imports() -> None:
    """必要なモジュールが正しくインポートできることを確認する."""
    import config  # noqa: F401
    import main  # noqa: F401
    from modules import effect_player, pose_detector, voice_listener  # noqa: F401

    assert True
