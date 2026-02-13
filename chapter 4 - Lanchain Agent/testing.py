from transaction_data import USER_DATABASE


def get_all_balances(user_id) -> str:
    """
    Get the total in the accounts
    """
    accounts = USER_DATABASE[user_id].get('accounts',{})

    if not accounts:
        return "No accounts found."

    result = "Your account balances:\n"
    for acc, bal in accounts.items():
        result += f"{acc.capitalize()}: ${bal:,.2f}\n"

    return result

if __name__=="__main__":
    # print(f"KEYS {USER_DATABASE.keys()}")
    statement = get_all_balances("user_002")
    print(statement)