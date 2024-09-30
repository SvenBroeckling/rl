import random


class DiceRoll:
    def __init__(self, formula, minimum_roll=5, crit_target=11):
        self.single_die_rolls = []

        try:
            dice, modifier = formula.split("+")
        except ValueError:
            dice = formula
            modifier = 0

        count, sides = dice.split("d")
        self.dice = [Die(int(sides)) for _ in range(int(count))]
        self.minimum_roll = minimum_roll
        self.crit_target = crit_target
        self.modifier = int(modifier)

    def roll(self):
        self.single_die_rolls = [die.roll_with_exploding() for die in self.dice]
        return self

    @property
    def result_sum(self):
        return sum(self.single_die_rolls) + self.modifier

    @property
    def result_string(self):
        return " + ".join(
            [str(roll) for roll in sorted(self.single_die_rolls, reverse=True)]
        )

    @property
    def successes(self):
        return len(
            [roll for roll in self.single_die_rolls if roll >= self.minimum_roll]
        )

    @property
    def critical_hits(self):
        return len([roll for roll in self.single_die_rolls if roll >= self.crit_target])


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
