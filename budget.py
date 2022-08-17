class Category:
    def __init__(self, categorie):
        self.name = categorie
        self.ledger = list()
        self.balance = 0.0

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})
        self.balance += amount

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": -1 * amount,
                "description": description
            })
            self.balance -= amount
            return True
        else:
            return False

    def get_balance(self):
        return self.balance

    def transfer(self, amount, object_categorie):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {object_categorie.name}')
            object_categorie.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.balance:
            return False
        else:
            return True

    def __repr__(self):
        budget_title = self.name.capitalize().center(30, '*') + '\n'
        for item in self.ledger:
            line_description = f'{item["description"][:23]}'.ljust(23)
            line_amount = f'{item["amount"]:4.2f}'.rjust(7)
            budget_title += line_description + line_amount + '\n'
        budget_title += f'Total: {self.balance:.2f}'
        return budget_title

def create_spend_chart(categories):
    chart_title = 'Percentage spent by category'

    spent_amounts = []
    for category in categories:
        spent_category = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spent_category += abs(item['amount'])
        spent_amounts.append(round(spent_category, 2))

    spent_total = round(sum(spent_amounts), 2)
    spent_percentage = [(((x / spent_total) * 100) // 10) * 10
                        for x in spent_amounts]

    chart_body = ''
    for i in range(100, -1, -10):
      chart_body += '\n' + str(i).rjust(3) + '| '
      for percent in spent_percentage:
        if percent >= i:
          chart_body += 'o  '
        else:
          chart_body += '   '

    chart_footer = '\n' + '    ' + ''.center(len(categories) * 3 + 1, '-')
    list_categories = [x.name for x in categories]
    max_length = max(map(len, list_categories))
    # Makes all categories the same length to avoid range errors
    list_categories = [x.ljust(max_length) for x in list_categories]
    for x in zip(*list_categories):
      chart_footer += '\n' + '     ' + '  '.join(x) + '  '

    chart = chart_title + chart_body + chart_footer

    return chart