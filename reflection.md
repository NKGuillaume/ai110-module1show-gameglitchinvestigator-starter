# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  when submit is pressed for the first time it didnt change the count 
  the diffuclty did not make sense 
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)? Copilot
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result). reset everything once play again or retry was clicked
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I attempted to handle the missing initial decrement of the attempt counter, the fix ended up affecting something else.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed? By playing with the app until it worked 
- Describe at least one test you ran (manual or using pytest)   to see what happened when you pressed play again , after having won a game 
  and what it showed you about your code. It diplayed that the code worked as intended 
- Did AI help you design or understand any tests? How? No, I found most or all of the logic before asking AI to make the test.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
 A sesion in Streamlit is a like a round and reruns just start the round over 
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects? Just playing with the code.
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task? I will attempt to do more of the work on my own to build stronger fundamentals.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
I never thought to use AI to create Logic test, Now having done it very useful. 