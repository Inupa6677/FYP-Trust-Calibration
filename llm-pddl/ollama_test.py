import ollama

prompt = """
Generate a valid PDDL problem for the barman domain with:
- 2 shots (shot1, shot2)
- 1 cocktail (cocktail1)
- A shaker
- Proper (:objects), (:init), and (:goal) sections
Output only PDDL code in the format:

(define (problem p01)
  (:domain barman)
  (:objects ...)
  (:init ...)
  (:goal (and ...))
)
"""

response = ollama.generate(model='phi', prompt=prompt)
print("=== Model Output ===")
print(response['response'])
