import sqlite3
import random

connection = sqlite3.connect("card.s3db")
n = 0
choice = None
choice2 = None
create = """
CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
);
"""

select = """
SELECT number, pin, balance FROM card;
"""


def query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()


def reading(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def Alg_Luna(card_n):
    card_number = list(card_n)
    card_number.pop(-1)
    first = "".join(card_number)
    for i in range(len(card_number)):
        card_number[i] = int(card_number[i])
        if i % 2 == 0:
            card_number[i] *= 2
        if card_number[i] > 9:
            card_number[i] -= 9

    total = sum(card_number)
    last_d = 10 - (total % 10)
    if last_d == 10:
        last_d = 0
    return first + str(last_d)


query(connection, create)

while choice != "0":
    choice = input("""
    1. Create an account
    2. Log into account
    0. Exit
    """)
    if choice == "1":
        card_number = "400000" + str(random.randint(1000000000, 10000000000))

        card_number = Alg_Luna(card_number)
        pin = random.randint(1000, 10000)
        print("Your card has been created")
        print("Your card number:")
        print(card_number)
        print("Your card PIN:")
        print(pin)
        query(connection, f"INSERT INTO card (number, pin) VALUES ({card_number}, {pin}); ")

    elif choice == "2":
        card_number = input("Enter your card number:\n")
        pin = input("Enter your PIN:\n")
        result = reading(connection, select)
        for i in range(len(result)):
            n += 1
            if card_number in result[i] and result[i][1] == pin:
                print("\nYou have successfully logged in!")
                balance_id = reading(connection, f"""SELECT id, balance FROM card WHERE number = {card_number}""")
                while choice2 != "0":
                    choice2 = input("""
                    1. Balance
                    2. Add income
                    3. Do transfer
                    4. Close account
                    5. Log out
                    0. Exit
                    """)
                    if choice2 == "1":
                        print(f"\nBalance: {result[i][2]}")
                    elif choice2 == "2":  # Add income
                        income = int(input("Enter income:\n"))

                        query(connection,
                              f"""UPDATE card SET balance = balance + {income} WHERE number = {card_number}""")

                        print("Income was added!")

                    elif choice2 == "3":  # Make transfer to another card
                        trans_pass = input("""Transfer\nEnter card number:\n""")
                        p = 0
                        balance_id = reading(connection, f"""SELECT id, balance FROM card WHERE number = {card_number}""")

                        for j in result:  # checking if the person whom I send money have a card
                            p += 1
                            if p == len(result) and trans_pass == result[i][0]:
                                print("You can't transfer money to the same account!")
                            elif p == len(result) and trans_pass in j and trans_pass == Alg_Luna(trans_pass):
                                trans_money = int(input("Enter how much money you want to transfer\n"))
                                if int(balance_id[0][1]) >= int(trans_money):  # write a query that minus money from your balance and add them to other balance
                                    query(connection,
                                          f"""UPDATE card SET balance = balance - {trans_money} WHERE number = {card_number};""")
                                    query(connection,
                                          f"""UPDATE card SET balance = balance + {trans_money} WHERE number = {trans_pass};""")
                                    print("Success!")
                                elif int(balance_id[0][1]) < int(trans_money):
                                    print("Not enough money!")
                            elif p == len(result) and trans_pass != Alg_Luna(trans_pass):
                                print("Probably you made a mistake in the card number. Please try again!")
                            elif p == len(result) and trans_pass not in j:
                                print("Such card does not exist.")

                    elif choice2 == "4":
                        query(connection, f"""DELETE FROM card WHERE id = {balance_id[0][0]};""")
                        print("The account has been closed!")
                    elif choice2 == "5":
                        print("\nYou have successfully logged out!")
                        break
            elif card_number not in result[i] and result[i][1] != pin and n == len(result) - 1:
                print("Wrong card number or PIN!")
        if choice2 == "0":
            break
print("Bye!")
