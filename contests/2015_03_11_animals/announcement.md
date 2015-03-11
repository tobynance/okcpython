# Animals!

My son has a card game called _**Spot it Jr.! Animals**_ that has round cards, with
each card showing **6** animals on it.  Given any two cards, there is exactly one
animal that can be found on both cards. There are a total of **31** unique animals
across the cards.

![Example Cards](cards01.jpg)

---

# Goal

Given a number of animals that will appear on each card and a list of animals,
print out the list of cards that need to be generated.

---

# Execution

Assuming your main python file is named `animals.py`, then to execute we would call:

    $ python numbers_game.py num_animals "animal1" "animal2" "animal3" ... "animalN"

Print to standard out a line per card, where each line is a tab delimited list of animal names for the card.

### Example

    $ python animals.py 2 "goat" "lamb" "sea cucumber"
    goat  lamb
    goat  sea cucumber
    lamb  sea cucumber

---

# Judging

The results will be judged primarily on correctness, then succinctness of solution, then speed of execution.

I have made a `solution_checker.py` which can be used to verify your program is working correctly.

You can test running it by running:

    $ python solution_checker.py example_animals.py
    '2	goat	lamb	sea cucumber' - success in 0.01 seconds
    '2	potato monster	larry	lark' - fail in 0.02 seconds

## Submissions Due

Email your solution to contest201503@okcpython.org by midnight of _**April 4th**_.
The test runner can be found at **`https://github.com/tobynance/okcpython`** under **`contests/2015_03_11_animals`**.
