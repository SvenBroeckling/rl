import random


class DiceRoll:
    def __init__(self, formula, minimum_roll=5):
        self.single_die_rolls = []
        self.result_sum = 0

        dice, modifier = formula.split("+")
        count, sides = dice.split("d")
        self.dice = [Die(int(sides)) for _ in range(int(count))]
        self.minimum_roll = minimum_roll
        self.modifier = int(modifier)
        self.successes = 0

    def roll(self):
        self.single_die_rolls = [die.roll_with_exploding() for die in self.dice]
        self.result_sum = sum(self.single_die_rolls) + self.modifier
        self.successes = len(
            [roll for roll in self.single_die_rolls if roll >= self.minimum_roll]
        )
        return self.successes


class Die:
    def __init__(self, sides):
        self.sides = sides

    def roll_with_exploding(self):
        result = 0
        roll = random.randint(1, self.sides)
        result += roll
        while roll == self.sides:
            roll = random.randint(1, self.sides)
            result += roll
        return result
