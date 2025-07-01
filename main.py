"""
Tia Rice 
3/22/2025
Project 1
"""

import random
import matplotlib.pyplot as plt

MONTHS = 12.0
N = 360.0

class Person:
    def __init__(self,checking,loan):

        """
        Args:
            checking(float): amount in checking
            loan(float): amount of loans
        
        """
        self.savings = 5000.0
        self.checking = checking
        self.debt = 30100.0
        self.loan = loan
        self.boughtHouse = False
        self.housingPriceRemaining = 175000.0
        self.savings_interest = 0.0
        self.loan_interest = 0.0
        self.savings_inflation = 1.0
        self.downpayment_threshold = 0.0
        self.income = 59000.0
        self.totalDebtPaid = 0.0

    def rentPayment(self):
        """
        Deducts the rent payment from the checking account or savings if needed.
        """
        if self.boughtHouse == False:
            rent = 850.0 * MONTHS
            if self.checking >= rent:
                self.checking -= rent
            else:
                dipIntoSavings = rent - self.checking # remaining amount of rent paid by savings
                self.checking = 0
                self.savings -= dipIntoSavings
    
    def populateAccounts(self):
        """
        Populates the person's checking and savings accounts based on their income.
        """
        self.savings += (.2*self.income) # 20% to saving
        self.checking += (.3*self.income) # 30% to checking

    def calculateSavings(self):
        """
        Calculates savings over time by applying the savings interest and inflation.
        """
        self.savings *= self.savings_interest
        self.savings *= self.savings_inflation
    
    def buyHouse(self):
        """
        Simulates buying a house if the person has enough savings for the down payment.
        """
        downpayment = 175000 * self.downpayment_threshold
        if self.checking >= downpayment and self.boughtHouse == False: # buy house as soon as can pay down payment
            self.boughtHouse = True
            self.checking -= downpayment

    def setLoan(self):
        loan_percentage = 0.95 if isinstance(self, nfl) else 0.80 # 95% for NFL, 80% for FL
        loanPrincipal = 175000 * loan_percentage

        i = self.loan_interest / MONTHS # convert annual interest to monthly
        D = ((1+i)**N-1)/(i*(1+i)**N) # discount factor

        monthly_payment = loanPrincipal/D # monthly mortgage payment
        self.loan = monthly_payment * 360

    def mortgagePayment(self):
        """
        Simulates a monthly mortgage payment if the person has bought a house.
        """
        if self.boughtHouse:
            loan_percentage = 0.95 if isinstance(self, nfl) else 0.80 # 95% for NFL, 80% for FL
            loanPrincipal = 175000 * loan_percentage # NFL should get 95% of the house price

            i = self.loan_interest / MONTHS # convert annual interest to monthly
            D = ((1+i)**N-1)/(i*(1+i)**N) # discount factor

            monthly_payment = loanPrincipal/D # monthly mortgage payment

            for i in range(12):
                actual_payment = min(monthly_payment, self.loan)
                self.totalDebtPaid += actual_payment  # Track actual money spent

                if self.checking >= actual_payment:
                    self.checking -= actual_payment
                else:
                    remaining_payment = actual_payment - self.checking
                    self.checking = 0
                    self.savings -= remaining_payment
                self.loan -= actual_payment  # Reduce mortgage loan


    def debtBalance(self):
        """
        Simulates debt repayment for one year.
        """
        total_payment = 0

        for _ in range(12):  # Run payments for 12 months
            if self.debt <= 0:
                break  # Stop payments if debt is fully paid

            min_payment = self.debt * 0.03  # 3% minimum payment
            extra_payment = 15 if isinstance(self, fl) else 1  # FL pays extra $15, NFL pays extra $1
            monthly_payment = min_payment + extra_payment

            actual_payment = min(self.debt, monthly_payment)

            if self.checking >= actual_payment:
                    self.checking -= actual_payment
            else:
                remaining_payment = actual_payment - self.checking
                self.checking = 0
                self.savings -= remaining_payment

            self.debt -= actual_payment
            total_payment += actual_payment

        if self.debt > 1e-10:
            self.debt *= 1.2  # Apply 20% annual interest
        else:
            self.debt = 0

        self.totalDebtPaid += total_payment  # Track total amount paid over the year
        return total_payment



class nfl(Person):
    """
    Represents an NFL (non finicially literate) as a subclass of Person
    """
    def __init__(self):
        super().__init__(checking=0.0, loan=0.0)
        self.savings_interest = 1.01 # 1% annual interest
        self.savings_inflation = .98 # 2% deflation
        self.downpayment_threshold = .05
        self.loan_interest = .05


    def __str__(self):
        """stringify"""
        return f"nfl "



class fl(Person):
    """
    Represents a FL (finicially literate) person as a subclass of Person
    """
    def __init__(self):
        super().__init__(checking=0.0, loan=0.0)
        self.savings_interest = 1.07
        self.savings_inflation = 1.0
        self.downpayment_threshold = .20
        self.loan_interest = .045

    def __str__(self):
        """stringify"""
        return f"fl "
            


class Simulation:
    """
    Runs the simulation for a person.
    """
    def __init__(self,person,enable_life_events=False):
        self.person = person
        self.enable_life_events = enable_life_events
        if self.enable_life_events:
            self.life_events = LifeEvents(person)

    def runSimulation(self):
        """
        Runs the simulation for 40 years, updating wealth, debt, and housing.
        Tracks wealth, years in debt, years renting, and total debt paid.

        Returns:
            list, int, int, float
        """
        wealthInfo = []
        countYearsOfDebt = 0
        countYearsOfRent = 0
        yearsMortgage = 0

        self.person.setLoan()
        for i in range(41):
            
            if self.person.boughtHouse:
                totalWealth = self.person.savings + self.person.checking - self.person.debt - self.person.loan
            else:
                totalWealth = self.person.savings + self.person.checking - self.person.debt

            self.person.populateAccounts()

            self.person.calculateSavings()
            
            if self.enable_life_events:
                self.life_events.apply_random_events()
            self.person.buyHouse()

            if not self.person.boughtHouse: # rent if no house bought
                self.person.rentPayment()
                countYearsOfRent += 1
            else:
                self.person.mortgagePayment()
                if self.person.loan > 1e-10:
                    yearsMortgage += 1

            self.person.debtBalance() # pay debt

            if self.person.boughtHouse:
                if self.person.debt > 0 or self.person.loan > 0:
                    countYearsOfDebt += 1
            else:
                if self.person.debt > 0:
                    countYearsOfDebt += 1

            wealthInfo.append(round(totalWealth))
        return wealthInfo, countYearsOfDebt, countYearsOfRent, self.person.totalDebtPaid


class LifeEvents:
    def __init__(self,person):
        self.person = person

    def job_loss(self):
        """ 5% chance of job loss. New salary is randomly $15/hour or $7.25/hour. """

        if random.random() < 0.05: # 5% chance
            print(f"Job loss event triggeredy!")
            new_income = random.choice([15000, 31200]) # minimum wage salaries
            self.person.income = new_income
            print(f"New income set to: ${new_income}")

    def gambling(self):
        """ Simulates gambling with a random win/loss. """

        if random.random() < 0.2: # 20% chance of gambling
            print("Gambling event triggered!")
            gamble_outcome = random.uniform(-0.2, 0.2) # Lose up to 20% or win up to 20%
            winnings = self.person.checking * gamble_outcome
            self.person.checking += winnings
            print(f"Gambling result: {'won' if winnings > 0 else 'lost'} ${abs(winnings):.2f}")

    def lottery(self):
        """ Simulates a lottery win with a 1% chance of winning. """

        if random.random() < 0.01: # 1% chance to win
            lottery_winnings = random.randint(100000, 1000000) # random prize between $100k and $1M
            print(f"Lottery event triggered! wins ${lottery_winnings}!")
            self.person.checking += lottery_winnings # add winnings to checking account 
    
    def job_promotion_or_demotion(self):
        """ Simulates job promotion or demotion. """

        chance = random.random()
        if chance < 0.05: # 5% chance of promotion
            salary_increase = self.person.income * 0.1 # 10% salary increase
            self.person.income += salary_increase
            print(f"Promotion event: a {salary_increase:.2f} salary increase!")
        elif chance < 0.1: # 5% chance of demotion
            salary_decrease = self.person.income * 0.05 # 5% salary decrease
            self.person.income -= salary_decrease
            print(f"Demotion event: a {salary_decrease:.2f} salary decrease!")


    def apply_random_events(self):
        """ Random life events applied each year. """

        self.job_loss()
        self.gambling()
        self.lottery()
        self.job_promotion_or_demotion()

def plot_wealth(wealthInfo,filename, title):
    """

    Plots wealth
    Args:
        wealthInfo: list[int]
        filename: str
        title: str
    
    """
    years = list(range(len(wealthInfo)))
    
    plt.figure(figsize=(10, 5))
    plt.plot(years, wealthInfo, marker='o', linestyle='-', color='r', label="Wealth") # plot wealth over time
    
    # make plot
    plt.xlabel("Years")
    plt.ylabel("Total Wealth (millions $)")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    
    plt.savefig(filename, format='png')

    # show the plot
    plt.show()


def main():
    user_choice = input("Do you want life events to be included? (y/n): ").strip().lower()
    enable_life_events = user_choice.startswith('y')

    nfl_person = nfl()
    nfl_sim = Simulation(nfl_person, enable_life_events) # only apply life events to non-financially literate
    nfl_results = nfl_sim.runSimulation()

    fl_person = fl()
    fl_sim = Simulation(fl_person)
    fl_results = fl_sim.runSimulation()

    print("FL Wealth Over 40 Years:", fl_results[0])
    print("FL Years in Debt:", fl_results[1], "Years Renting:", fl_results[2])
    print("FL Debt Paid:", round(fl_results[3],2))

    print("NFL Wealth Over 40 Years:", nfl_results[0])
    print("NFL Years in Debt:", nfl_results[1], "Years Renting:", nfl_results[2])
    print("NFL Debt Paid:", round(nfl_results[3],2))

    
    plot_wealth(fl_results[0], "fl.png", "fl Wealth Over Time")
    plot_wealth(nfl_results[0], "nfl.png", "nfl Wealth Over Time")




def run_tests():
    fl_person = fl()
    nfl_person = nfl()

    assert fl_person.savings == 5000.0, f"Expected FL savings: 5000.0, got {fl_person.savings}"
    assert fl_person.checking == 0.0, f"Expected FL checking: 0.0, got {fl_person.checking}"
    assert fl_person.debt == 30100.0, f"Expected FL debt: 30100.0, got {fl_person.debt}"
    assert fl_person.loan == 0.0, f"Expected FL loan: 0.0, got {fl_person.loan}"

    assert nfl_person.savings == 5000.0, f"Expected NFL savings: 5000.0, got {nfl_person.savings}"
    assert nfl_person.checking == 0.0, f"Expected NFL checking: 0.0, got {nfl_person.checking}"
    assert nfl_person.debt == 30100.0, f"Expected NFL debt: 30100.0, got {nfl_person.debt}"
    assert nfl_person.loan == 0.0, f"Expected NFL loan: 0.0, got {nfl_person.loan}"

    assert str(fl_person) == "fl ", f"Expected FL string: 'fl ', got {str(fl_person)}"

    assert str(nfl_person) == "nfl ", f"Expected NFL string: 'nfl ', got {str(nfl_person)}"

    fl_person.debt = 30100.0
    fl_person.debtBalance()
    assert fl_person.debt < 30100.0, f"Expected FL debt to decrease, got {fl_person.debt}"

    nfl_person.debt = 30100.0
    nfl_person.debtBalance()
    assert nfl_person.debt < 30100.0, f"Expected NFL debt to decrease, got {nfl_person.debt}"

    fl_person.debt = 0
    total_payment = fl_person.debtBalance()
    assert total_payment == 0, f"Expected total FL payment to be 0, got {total_payment}"

    nfl_person.debt = 0
    total_payment = nfl_person.debtBalance()
    assert total_payment == 0, f"Expected total NFL payment to be 0, got {total_payment}"

    fl_person.debt = 30100.0
    fl_person.debtBalance()
    assert fl_person.debt < 30100.0, f"Expected FL debt to decrease after one year, got {fl_person.debt}"

    nfl_person.debt = 30100.0
    nfl_person.debtBalance()
    assert nfl_person.debt < 30100.0, f"Expected NFL debt to decrease after one year, got {nfl_person.debt}"

    fl_person.checking = 1000
    result = fl_person.rentPayment()
    assert result is None, f"Expected rentPayment to return None, got {result}"
    fl_person.boughtHouse = True
    fl_person.checking = 5000
    fl_person.savings = 3000
    fl_person.rentPayment()
    assert fl_person.checking == 5000, f"Expected checking to remain 5000, got {fl_person.checking}"
    assert fl_person.savings == 3000, f"Expected savings to remain 3000, got {fl_person.savings}"

    fl_person = fl() # reset after payment
    nfl_person = nfl()
    
    fl_person.income = 50000 # set test income for easy manual checking
    nfl_person.income = 50000
    
    fl_person.populateAccounts()
    nfl_person.populateAccounts()
    
    assert fl_person.savings == 5000 + (0.2 * 50000), f"FL savings incorrect after populateAccounts, got {fl_person.savings}"
    assert fl_person.checking == 0 + (0.3 * 50000), f"FL checking incorrect after populateAccounts, got {fl_person.checking}"
    assert nfl_person.savings == 5000 + (0.2 * 50000), f"NFL savings incorrect after populateAccounts, got {nfl_person.savings}"
    assert nfl_person.checking == 0 + (0.3 * 50000), f"NFL checking incorrect after populateAccounts, got {nfl_person.checking}"

    # set up scenario
    fl_person.savings_interest = 1.02 # 2% interest
    fl_person.savings_inflation = 1.01 # 1% inflation
    before_savings = fl_person.savings
    fl_person.calculateSavings()
    expected_savings = before_savings * 1.02 * 1.01
    assert abs(fl_person.savings - expected_savings) < 1e-6, f"calculateSavings incorrect, got {fl_person.savings}, expected {expected_savings}"
    result = fl_person.calculateSavings()
    assert result is None, f"Expected rentPayment to return None, got {result}"

    fl_person.savings_interest = 1.0
    fl_person.savings_inflation = 1.0
    before_savings = fl_person.savings
    fl_person.calculateSavings()
    assert fl_person.savings == before_savings, f"calculateSavings should not change savings when interest and inflation are 1.0, got {fl_person.savings}"

    fl_person.savings = 50000 # enough for down payment
    fl_person.buyHouse()
    assert fl_person.boughtHouse == True, f"FL should have bought a house, but didn't."
    assert fl_person.savings < 50000, f"Savings should have decreased after buying house, got {fl_person.savings}"
    nfl_person.buyHouse()
    assert nfl_person.boughtHouse == True, f"NFL should NOT have bought a house, but did."

    fl_person.checking = 1000
    fl_person.savings = 10000
    fl_person.housingPriceRemaining = 100000
    fl_person.loan_interest = 0.05
    fl_person.mortgagePayment()
    assert fl_person.checking < 1000 or fl_person.savings < 10000, f"Mortgage payment not deducted properly."
    assert fl_person.totalDebtPaid > 0
    assert fl_person.mortgagePayment() is None, f"expected None type"

#if __name__ == "__main__":
    #run_tests()
main()
