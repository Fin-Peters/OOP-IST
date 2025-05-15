class Customer:
    def __init__(self, name):
        self.name = name
        self.accounts = []
    
    def add_account(self, account):
        self.accounts.append(account)

    def show_accounts(self):
        for account in self.accounts:
            print(f"Account Type: {account.account_type}")
            

class Bank:
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.customers = []
    
    def add_customer(self, customer):
        self.customers.append(customer)
    
    def show_customers(self):
        for customer in self.customers:
            print(f"Customer Name: {customer.name}")
            customer.show_accounts()