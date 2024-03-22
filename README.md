## AHI Bank - Python Code Description

This Python code simulates a simple bank management system called AHI Bank. It allows users to create accounts, log in, and perform transactions such as checking balance, depositing, withdrawing, and transferring funds.

**Data Structure:**

* A pandas DataFrame named `accounts_df` is used to store account information. 
* The DataFrame has columns for `first_name`, `last_name`, `account_number`, `PIN`, and `balance`.

**Main Functionality:**

The code runs in a loop, presenting the user with a menu:

1. **Create an account:** This option allows users to enter their details and create a new account with a randomly generated account number.
2. **Log into account:** Users can enter their account number and PIN to log in. If successful, they can access their account information and perform transactions.
3. **Make a transaction:** This option (intended to potentially be integrated into future functionalities) seems to currently redirect to the login option.

**Login and Transaction Options:**

* Upon successful login, users can:
    * Check their current balance.
    * Deposit funds into their account.
    * Withdraw funds from their account (with insufficient balance check).
    * Transfer funds to another account within the system (with insufficient balance check and update of both accounts).
