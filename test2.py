from test import Account

class savingsAccount(Account):
    def __init__(self):
        super().__init__()
        self.account_type = "Savings"
        self.interest_rate = 2.35
        self.interest = 0.0

    def calculate_interest(self):
        self.interest = (self.account_balance * self.interest_rate / 100)
        return self.interest
    
    def addInterest(self, ):
        self.account_balance += self.interest
        print(f"Interest of {self.interest} added to account balance. New balance: {self.account_balance}")
    
bean = savingsAccount()
bean.calculate_interest()
bean.addInterest()