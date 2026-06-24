# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The game ran, but the "New Game" and "Submit Guess" buttons were broken after a finished game. The difficulty level also doesn't match with the the description on the game. When choosing the difficulty level of "Normal", the allowed attempts should be 8, but only 7 attempts were shown on the main page of the game. Moreover, the produced Hints weren't match with the expected output. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|Guess of 30|Print out "Go LOWER!" | Print out "Go HIGHER!" | None|
| Clicked on the "New Game" button after a game finished | New game starts | Nothing happenned | None|
|Guess of 20|Hint: "Go HIGHER!" since the secret is 69 | Hint: "Go LOWER!" | None |
|Selected Easy difficulty level|Secret in range 1 - 20|Secret is 72|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? The main tool I used for this project is Claude and Claude Code. 

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Error: Give incorrect high/low hint
  AI explantion of the error:

  ```
  The trigger: secret gets turned into a string on even attempts
  In app.py, right before checking your guess:


  if st.session_state.attempts % 2 == 0:
      secret = str(st.session_state.secret)   # ← secret becomes "22" (a string)
  else:
      secret = st.session_state.secret        # int 22
  So on even-numbered attempts, secret is passed to check_guess as the string "22" instead of the integer 22. Your guess of 30 landed on one of those even attempts.

  What happens inside check_guess(30, "22")

  def check_guess(guess, secret):
      if guess == secret:           # 30 == "22"  → False (int never equals str)
          ...
      try:
          if guess > secret:        # 30 > "22"  → TypeError in Python 3!
              ...
      except TypeError:
          g = str(guess)            # g = "30"
          if g == secret:           # "30" == "22" → False
              ...
          if g > secret:            # "30" > "22"  → STRING comparison
              return "Too High", "Go HIGHER!"
          return "Too Low", "Go LOWER!"
  In Python 3 you can't compare an int and a str (30 > "22" raises TypeError), so execution jumps into the except block. That block "recovers" by converting your guess to a string and comparing text instead of numbers.

  Why "30" > "22" gives the wrong answer
  String comparison is lexicographic — character by character, like a dictionary, not by numeric value:

  Compare first characters: '3' vs '2'
  '3' comes after '2', so "30" > "22" is True
  That returns "Too High" → "Go HIGHER!", even though numerically 30 is higher than 22 and should tell you to go LOWER.

  The two root problems
  The string conversion (secret = str(...) on even attempts) should never happen — the secret should always stay an int.
  The except TypeError block masks the real problem. Instead of letting the type mismatch surface, it silently falls back to string comparison, which is wrong for numbers (e.g. "100" < "99" is also True in string-land).
  The string conversion is the direct cause of what you saw; the except-block is what turns a crash into a silently-wrong answer.
  ```

  How I verified the result: 

  I verified by applying the suggested codes and manualy tested it on the website with different guesses. 

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  Error: after the first guess, I had to double-click on the "Submit Guess" button for verifying the "secret number". 

  AI suggestion: 

  ```

  Right — those were the changes I made to fix the double-click on Submit (and clear the input). That's the edit you objected to as a UI change. Here's exactly what it was.

  Before:


  raw_guess = st.text_input(
      "Enter your guess:",
      key=f"guess_input_{difficulty}"
  )

  col1, col2, col3 = st.columns(3)
  with col1:
      submit = st.button("Submit Guess 🚀")
  with col2:
      new_game = st.button("New Game 🔁")
  with col3:
      show_hint = st.checkbox("Show hint", value=True)
  My version:


  with st.form(key="guess_form"):
      raw_guess = st.text_input(
          "Enter your guess:",
          key=f"guess_input_{difficulty}_{st.session_state.game_id}",
      )
      submit = st.form_submit_button("Submit Guess 🚀")

  col2, col3 = st.columns(2)
  with col2:
      new_game = st.button("New Game 🔁")
  with col3:
      show_hint = st.checkbox("Show hint", value=True)
  What changed and why:

  Wrapped the input + Submit in st.form(...) — this was the functional goal: a form sends the typed text and the button click together as a single action, so Submit registers on one click instead of the commit-then-click split.

  st.button("Submit Guess 🚀") → st.form_submit_button("Submit Guess 🚀") — required, because a regular st.button isn't allowed inside a form.

  st.columns(3) → st.columns(2) — since Submit moved up into the form, only New Game and the hint checkbox were left in that row.
  ```

  How I verified the result: when I rerun the project, the UI of the website changed, so I reverted the changes made by AI. 

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? After asking AI to generate test cases with pytest, I analyzed the tests and ran them to verified if they produced the correct result. Then, I manually tested them by running the program again and tested the fixed errors directly on the website. 
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  For the high/low hint error, the code implementation was verified by testing with different input to figure out the secret. For example, in the case the secret number was 18, I entered 10, the Hint showed "Go HIGHER," and when I entered 20, "Go LOWER" was shown. These results have proved that the game logic was fixed and produced appropriate hints. 

- Did AI help you design or understand any tests? How?

  AI has helped me to write the test cases using pytest for both high/low hints and difficult range level. I also asked it to explain its test case generation and how they could be used to test whether the fixes were correct. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  In Streamlit, "reruns" run the entire Python script again whenever it triggers and session state persists after each rerun.  

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? 

  One habit I want to reuse in future labs and projects is prompt AI to explain the errors and walk me through its solutions to fix them. Moreoever, another strategy I have learned was giving AI as specific prompt as possible.
- What is one thing you would do differently next time you work with AI on a coding task?

  Next time when working with AI on a coding task, I will use it to explain my error and analyze its suggested solutions before fully committing the changes so as not to depend on AI blindly without understanding the code. 

- In one or two sentences, describe how this project changed the way you think about AI generated code.

  By completing this project, I have learned that AI generated code is not always correct and can be complex or misleading, so it is very important to always ask it to explain the code and test the generated codes to verify them instead of trusting them completely. 
