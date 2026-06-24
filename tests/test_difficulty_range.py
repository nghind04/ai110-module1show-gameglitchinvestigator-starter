"""Regression tests for the difficulty/secret bug.

The bug: the secret number was generated only once (guarded by
`if "secret" not in st.session_state`), so changing the difficulty
updated the range but never regenerated the secret. These tests drive
the real app through Streamlit's AppTest harness so the script re-runs
exactly like a user interaction would.
"""

import random

from streamlit.testing.v1 import AppTest


def run_app():
    # Seed the RNG so the very first secret (drawn under the default "Normal"
    # range) is deterministically 80. That value is OUTSIDE both the Easy (1-20)
    # and Hard (1-50) ranges, so if the buggy code fails to regenerate the
    # secret after a difficulty change, these tests reliably FAIL instead of
    # passing by luck. Without the seed the buggy secret lands in range ~20% of
    # the time and the test becomes flaky.
    random.seed(5)
    at = AppTest.from_file("app.py")
    return at.run()


def select_difficulty(at, difficulty):
    # Find the difficulty dropdown and choose a value; .run() re-executes the
    # whole script, which is the moment the old code failed to refresh the secret.
    at.selectbox[0].set_value(difficulty).run()
    return at


def test_secret_in_range_for_easy():
    at = run_app()
    at = select_difficulty(at, "Easy")
    secret = at.session_state["secret"]
    assert 1 <= secret <= 20, f"Easy secret {secret} is outside 1-20"


def test_secret_in_range_for_hard():
    at = run_app()
    at = select_difficulty(at, "Hard")
    secret = at.session_state["secret"]
    assert 1 <= secret <= 50, f"Hard secret {secret} is outside 1-50"


def test_secret_refreshes_when_switching_back_to_normal():
    # Normal -> Easy -> Normal: the secret must track the *current* difficulty,
    # not stay frozen at whatever was generated first.
    at = run_app()
    at = select_difficulty(at, "Easy")
    at = select_difficulty(at, "Normal")
    secret = at.session_state["secret"]
    assert 1 <= secret <= 100, f"Normal secret {secret} is outside 1-100"


def test_secret_difficulty_companion_value_is_tracked():
    # The fix stores which difficulty the secret was built for; it should
    # always match the active difficulty after a change.
    at = run_app()
    at = select_difficulty(at, "Easy")
    assert at.session_state["secret_difficulty"] == "Easy"
