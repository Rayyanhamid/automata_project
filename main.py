import streamlit as st

# ATM کلاس کی تعریف
class ATM:
    def __init__(self):
        self.users = {
            "Rayyan": {
                "pin": "9009",
                "balance": 10000,
                "transactions": []
            }
        }

    def authenticate(self, username, pin):
        user = self.users.get(username)
        if user and user["pin"] == pin:
            return True
        return False

    def get_balance(self, username):
        return self.users[username]["balance"]

    def deposit(self, username, amount):
        self.users[username]["balance"] += amount
        self.users[username]["transactions"].append(f"Deposited: {amount} rupees")

    def withdraw(self, username, amount):
        if amount <= self.users[username]["balance"]:
            self.users[username]["balance"] -= amount
            self.users[username]["transactions"].append(f"Withdrew: {amount} rupees")
            return True
        return False

    def change_pin(self, username, new_pin):
        self.users[username]["pin"] = new_pin

    def get_transactions(self, username):
        return self.users[username]["transactions"]

# Streamlit ایپلیکیشن
st.set_page_config(page_title="ATM System", layout="centered")
st.title("ATM System")

# ATM آبجیکٹ بنائیں
atm = ATM()

# سیشن سٹیٹ میں صارف کا نام محفوظ کریں
if "username" not in st.session_state:
    st.session_state.username = ""

# اگر صارف لاگ ان نہیں ہے تو لاگ ان فارم دکھائیں
if not st.session_state.username:
    st.subheader("Login")
    username = st.text_input("Enter your name").capitalize()
    pin = st.text_input("Enter your PIN", type="password")
    if st.button("Login"):
        if atm.authenticate(username, pin):
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or PIN.")
else:
    st.subheader(f"Welcome, {st.session_state.username}!")
    option = st.selectbox("Select an option", ["Show Balance", "Deposit", "Withdraw", "Change PIN", "Transaction History", "Logout"])

    if option == "Show Balance":
        balance = atm.get_balance(st.session_state.username)
        st.info(f"Your current balance is: {balance} rupees")

    elif option == "Deposit":
        amount = st.number_input("Enter amount to deposit", min_value=1)
        if st.button("Deposit"):
            atm.deposit(st.session_state.username, amount)
            st.success(f"Deposited {amount} rupees.")

    elif option == "Withdraw":
        amount = st.number_input("Enter amount to withdraw", min_value=1)
        if st.button("Withdraw"):
            if atm.withdraw(st.session_state.username, amount):
                st.success(f"Withdrew {amount} rupees.")
            else:
                st.error("Insufficient funds.")

    elif option == "Change PIN":
        new_pin = st.text_input("Enter new 4-digit PIN", type="password")
        if st.button("Change PIN"):
            if len(new_pin) == 4 and new_pin.isdigit():
                atm.change_pin(st.session_state.username, new_pin)
                st.success("PIN changed successfully.")
            else:
                st.error("Invalid PIN format.")

    elif option == "Transaction History":
        transactions = atm.get_transactions(st.session_state.username)
        if transactions:
            st.write("Transaction History:")
            for txn in transactions:
                st.write(txn)
        else:
            st.info("No transactions found.")

    elif option == "Logout":
        st.session_state.username = ""
        st.success("Logged out successfully.")
