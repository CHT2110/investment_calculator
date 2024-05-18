from dataclasses import dataclass
import argparse
import matplotlib.pyplot as plt
import pandas as pd


parser = argparse.ArgumentParser(description='Calculating investment returns')

parser.add_argument('-b', '--balance', type=int, required=True, help='The starting amount of your investment')
parser.add_argument('-c', '--contributions', type=int, required=True, help= 'The monthly investment very month')
parser.add_argument('-i', '--interest', type=float, required=True, help='The expected yearly interest rate in percentages (e.g 0.07)')
parser.add_argument('-y', '--years', type=int, required=True, help='How many years the investment accumulates')

args = parser.parse_args()

@dataclass
class investment_variables:
    starting_balance: int
    monthly_contribution: int
    yearly_interest: float
    years: int

    def calculate_returns(self):
        '''
        This function calculates the final balance of an account and how contributions and returns make
        up the final balance. This is done based of the starting balance, monthly contribution, yearly interest
        and years it accumulates. The output is the final balance, total contributions and total returns.  
        '''
        # Convert annual rate to monthly rate
        monthly_interest = self.yearly_interest / 100 / 12
        # Calculate total number of months
        total_months = self.years * 12

        balance = self.starting_balance
        contributions = self.starting_balance
        returns = 0

        data = []

        for month in range(total_months):
            # Adding monthly interest to balance
            balance *= (1 + monthly_interest)
            # Adding monthly contributions
            balance += self.monthly_contribution
            # Adding monthly contribution to total contributions
            contributions += self.monthly_contribution
            # Calculating the returns based of the balance and contributions
            returns = balance - contributions

            data.append(
                {'month': month,
                 'balance': round(balance),
                 'contributions': contributions,
                 'returns': round(returns)}
            )
        
        for entry in data:
            print(entry)
        
        return data

investment_data = investment_variables(
                    starting_balance=args.balance, 
                    monthly_contribution=args.contributions, 
                    yearly_interest=args.interest, 
                    years=args.years )

df = pd.DataFrame(investment_variables.calculate_returns(investment_data))

x = df.month
y_balance = df.balance
y_contributions = df.contributions
y_returns = df.returns

plt.fill_between(x, y_balance, label='Total Balance')
plt.fill_between(x, y_contributions, label='Total Contributions')
plt.fill_between(x, y_returns, label='Total Returns')
plt.legend()

plt.show()
