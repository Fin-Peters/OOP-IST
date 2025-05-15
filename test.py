class Account:
    def __init__(self):
        self.account_name = ""
        self.bsb = ""
        self.account_balance = 0
        self.pin = ""
        self.overdraft_limit = 0
        self.account_type = "Savings"
        self.interest_rate = 2.35

    def setPin(self):
        pinValid = False
        print("please enter 4 digit pin")
        tempPin = input("")
        while pinValid == False:
            while len(tempPin) == 4 and tempPin.isdigit():
                self.pin = tempPin
                print("Pin set successfully")
                pinValid = True  
                return pinValid
            else:
                print("Pin invalid.")
                self.setPin()

    def checkPin(self):
        maxPinAttempts = 3
        pinAttempts = 0
        while pinAttempts < maxPinAttempts:
            pin = input("Enter your pin: ")
            if pin == self.pin:
                print("Pin is correct")
                return True
            else:
                print("Pin is incorrect")
                pinAttempts += 1
        print("Max pin attempts reached")
        print("Get Fucked")

    def deposit(self):
        # will affect the account balance
        deposit_amount = float(input("Deposit amount: "))
        self.account_balance = self.account_balance + deposit_amount

    def withdraw(self):
        # will affect the account balance
        withdraw_amount = float(input("Withdraw amount: "))
        if withdraw_amount > self.account_balance + self.overdraft_limit:
            print("UNABLE TO PERFORM WITHDRAWAL. NOT ENOUGH FUNDS AVAILABLE.")
        else:
            self.account_balance = self.account_balance - withdraw_amount



