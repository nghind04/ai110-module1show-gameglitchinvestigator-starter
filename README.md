# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- The game's purpose: a secret number guessing game, in which users need to guess the correct number using the hints under a specific number of attempts for each level. 
- Bugs I found in the game: 
   * Incorrect High/Low Hint: the game returns Hint of "Go HIGHER" when user guessed a number larger than the secret, and "Go LOWER" when the guess was smaller than the secret. 
   * Unmatching display and incorrect secret generation based on difficulty level: when user selected different difficulty level, the secret number and the guessing range remained unchanged while the number of attempts changed. 
- Fixes in the game: 
   * The game gave correct High/Low hints for eah guess by fixing the game logic and moving `parse_guess` and `check_guess` functions to `logic_utils.py`
   * Correct secret number is generated and correct range is displayed accordingly to each difficulty level

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. User selects level "Normal"
2. Game displays "Guess a number between 1 and 100. Attempts left: 7". The secret number is 66
3. User enters 10 -> Game returns "Go HIGHER"
4. User enters 80 -> Game returns "Go LOWER"
5. Game ends after the correct guess and displays the score

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

```
collected 9 items                                                                                                                                            

tests/test_difficulty_range.py ....                                                                                                                    [ 44%]
tests/test_game_logic.py .....                                                                                                                         [100%]

===================================================================== 9 passed in 0.60s ======================================================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
