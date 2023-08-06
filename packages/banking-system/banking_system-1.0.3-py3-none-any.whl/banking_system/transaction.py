class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def process_transaction(self):
        try:
            self.sender.withdraw(self.amount)
            self.receiver.deposit(self.amount)
            return True
        except ValueError:
            return False
