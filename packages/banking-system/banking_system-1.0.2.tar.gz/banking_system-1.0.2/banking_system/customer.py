class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def get_info(self):
        return f"Name: {self.name}, Address: {self.address}"
