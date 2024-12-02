import pandas as pd
import datetime
import matplotlib.pyplot as plt
import os
import random

# Initialize or load existing transaction and goal data
try:
    df = pd.read_excel('expense_tracker.xlsx')
except FileNotFoundError:
    df = pd.DataFrame(columns=['Date', 'Time', 'Category', 'Amount', 'Description', 'Balance'])

try:
    goals_df = pd.read_excel('savings_goals.xlsx')
except FileNotFoundError:
    goals_df = pd.DataFrame(columns=['Goal', 'Category', 'Goal Amount', 'Saved Amount'])

try:
    reminders_df = pd.read_excel('reminders.xlsx')
except FileNotFoundError:
    reminders_df = pd.DataFrame(columns=['Reminder', 'Due Date'])

# 2. Add a New Transaction with improved input validation
def add_transaction(balance_limit):
    while True:
        try:
            amount = float(input("Enter the transaction amount: "))
            break  # Exit the loop if the amount is valid
        except ValueError:
            print("Invalid input for amount. Please enter a numerical value.")

    description = input("Enter the transaction description: ")
    category = input("Enter the transaction category (e.g., Food, Entertainment, Transport): ")

    date = datetime.datetime.now().strftime("%Y-%m-%d")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    # Ensure the balance is properly retrieved from the last row
    previous_balance = df['Balance'].iloc[-1] if not df.empty else 0
    new_balance = previous_balance - amount

    # Adding the new transaction with all required columns
    transaction = {
        'Date': date,
        'Time': time,
        'Category': category,
        'Amount': amount,
        'Description': description,
        'Balance': new_balance
    }

    df.loc[len(df)] = transaction  # Append the transaction as a new row

    if amount > balance_limit:
        print(f"Warning: Transaction limit exceeded! Transaction amount is {amount}")

    df.to_excel('expense_tracker.xlsx', index=False)
    print(f"Transaction added successfully! Previous balance: {previous_balance}, New balance: {new_balance}")

    check_balance()

# 3. Modify Transaction Limit
def set_transaction_limit():
    global transaction_limit
    transaction_limit = float(input("Set your transaction limit: "))
    print(f"Transaction limit set to {transaction_limit}.")

# 4. Add Funds to Savings Goals
def add_to_goal():
    goal_name = input("Enter the goal name (e.g., Vacation): ")
    goal_amount = float(input("Enter amount to add to this goal: "))

    if goal_name in goals_df['Goal'].values:
        goals_df.loc[goals_df['Goal'] == goal_name, 'Saved Amount'] += goal_amount
    else:
        goals_df.loc[len(goals_df)] = [goal_name, "General", 0, goal_amount]

    goals_df.to_excel('savings_goals.xlsx', index=False)
    print(f"Added ${goal_amount} to the {goal_name} goal.")

# 5. Manage Bill Reminders
def manage_reminders():
    num_reminders = int(input("Enter the number of reminders to set: "))
    for _ in range(num_reminders):
        description = input("Enter reminder description: ")
        due_date = input("Enter due date (YYYY-MM-DD): ")
        reminders_df.loc[len(reminders_df)] = [description, due_date]

    reminders_df.to_excel('reminders.xlsx', index=False)
    print("Reminders set successfully.")

# 6. Financial Health Tracker
def financial_health_tracker():
    total_spent = df['Amount'].sum()
    avg_spent = df['Amount'].mean()
    high_debt = total_spent > 1000
    freq_spending = len(df) > 20

    heartbeat = "Healthy" if not high_debt and freq_spending < 20 else "Stressed"
    print(f"Financial Health Status: {heartbeat}")
    print(f"Total spent: ${total_spent:.2f}, Average transaction: ${avg_spent:.2f}")

# 7. Check Balance
def check_balance():
    current_balance = df['Balance'].iloc[-1] if not df.empty else 0
    print(f"Current balance: ${current_balance}")

8

# 8. Visualize Daily & Weekly Expenses
def plot_expenses():
    df['Date'] = pd.to_datetime(df['Date'])

    # Daily expenses
    daily_expenses = df.groupby(df['Date'].dt.date)['Amount'].sum()

    # Weekly expenses - using iso calendar to get week number
    weekly_expenses = df.groupby(df['Date'].dt.isocalendar().week)['Amount'].sum()

    # Plotting both daily and weekly expenses
    plt.figure(figsize=(12, 5))

    # Plot daily expenses
    plt.subplot(1, 2, 1)
    daily_expenses.plot(kind='bar', title='Daily Expenses')

    # Plot weekly expenses
    plt.subplot(1, 2, 2)
    weekly_expenses.plot(kind='line', title='Weekly Expenses')

    plt.tight_layout()
    plt.show()


# 9. Group Expense Sharing
def group_expense_sharing():
    expense = float(input("Enter total group expense: "))
    num_people = int(input("Enter the number of people sharing: "))
    each_share = expense / num_people
    print(f"Each person should pay: ${each_share:.2f}")

# 10. Subscription Management
def manage_subscriptions():
    subscriptions = []
    num_subs = int(input("Enter the number of subscriptions: "))
    for _ in range(num_subs):
        sub_name = input("Subscription name: ")
        sub_cost = float(input("Monthly cost: "))
        subscriptions.append({"Subscription": sub_name, "Cost": sub_cost})

    sub_df = pd.DataFrame(subscriptions)
    sub_df.to_excel('subscriptions.xlsx', index=False)
    print("Subscriptions added.")

# 11. Price Drop & Refund Alerts
def price_drop_alert():
    print("Feature: Tracks recent purchases for price drops and issues alerts for potential refunds.")

# 12. Mood-Based Financial Planning
def mood_based_suggestions():
    mood = input("How do you feel today? (happy, stressed, etc.): ")
    if mood.lower() == "stressed":
        print("Suggestion: Avoid major purchases today and try a free activity to unwind.")

# 13. Eco-Savings Tracker
def eco_savings_tracker():
    eco_expenses = float(input("Enter the amount saved by choosing eco-friendly options: "))
    print(f"Eco-savings this month: ${eco_expenses:.2f}")

# 14. Micro-Investment Suggestions
def suggest_micro_investments():
    print("Micro-investment suggestion: Invest $5 weekly in diversified funds for gradual growth.")

# 15. Goal-Oriented Expense Buckets
def goal_expense_buckets():
    print("You can create separate buckets for specific goals, like travel or emergency funds.")

# 16. Financial Insights Dashboard
def insights_dashboard():
    print("Feature: A personalized dashboard offers insights on spending trends, upcoming bills, and goals.")

# Main Interactive Menu
def main():
    print("Welcome to the Advanced Personal Expense Tracker")
    set_transaction_limit()

    while True:
        print("\nChoose an option:")
        options = [
            "Add a transaction", "Modify transaction limit", "Add funds to savings goal",
            "Set and track reminders", "View financial health tracker", "Check current balance",
            "Visualize daily & weekly expenses", "Group expense sharing",
            "Manage subscriptions", "Price drop alerts", "Mood-based planning",
            "Eco-savings tracker", "Micro-investment tips", "Goal-oriented expense buckets",
            "Insights dashboard", "Exit"
        ]

        for i, opt in enumerate(options, 1):
            print(f"{i}. {opt}")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_transaction(transaction_limit)
        elif choice == 2:
            set_transaction_limit()
        elif choice == 3:
            add_to_goal()
        elif choice == 4:
            manage_reminders()
        elif choice == 5:
            financial_health_tracker()
        elif choice == 6:
            check_balance()
        elif choice == 7:
            plot_expenses()
        elif choice == 8:
            group_expense_sharing()
        elif choice == 9:
            manage_subscriptions()
        elif choice == 10:
            price_drop_alert()
        elif choice == 11:
            mood_based_suggestions()
        elif choice == 12:
            eco_savings_tracker()
        elif choice == 13:
            suggest_micro_investments()
        elif choice == 14:
            goal_expense_buckets()
        elif choice == 15:
            insights_dashboard()
        elif choice == 16:
            print("Exiting the Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main function
main()
