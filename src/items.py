class Item:
    def __init__(self, key, name, amount=1):
        self.key = key
        self.name = name
        self.amount = amount

    def __str__(self):
        return f"[{self.key}] {self.name} (x{self.amount})"
