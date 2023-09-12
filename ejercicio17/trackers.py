class IncomeManager:
    def __init__(self):
        self.income = 0
        self.incomes_list = []

    def add_income(self, amount):
        self.income += amount
        self.incomes_list.append(amount)

    def get_income(self):
        return self.income

    def get_incomes_list(self):
        return self.incomes_list


class ExpenseManager:
    def __init__(self):
        self.expense = 0
        self.expenses_list = []

    def add_expense(self, amount):
        self.expense += amount
        self.expenses_list.append(amount)

    def get_expense(self):
        return self.expense

    def get_expenses_list(self):
        return self.expenses_list


class SavingsManager:
    def __init__(self):
        self.saving = 0
        self.savings_list = []

    def add_saving(self, amount):
        self.saving += amount
        self.savings_list.append(amount)

    def get_saving(self):
        return self.saving

    def get_savings_list(self):
        return self.savings_list