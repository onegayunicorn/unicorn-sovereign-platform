"""Dialogue unit tests."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "packages"))
from npc_core.dialogue.manager import DialogueManager

def test_intent_detection():
    dm = DialogueManager("c137_rick")
    assert dm.detect_intent("Can you give me a quest?") == "quest"
    assert dm.detect_intent("Goodbye!") == "farewell"
    assert dm.detect_intent("How does the laser work?") == "question"

def test_context_window_trimming():
    dm = DialogueManager("c137_rick")
    dm.MAX_CONTEXT_TURNS = 5
    for i in range(10):
        dm.add_player_turn(f"msg {i}")
    assert len(dm.context_window()) <= 5
