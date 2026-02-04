from transaction_data import USER_DATABASE

if __name__=="__main__":
    # print(f"KEYS {USER_DATABASE.keys()}")
    user_id="user_001"
    user_data = USER_DATABASE.get(user_id,{})

    balance =user_data.get("accounts", {}).get("savings")
    print(f"${balance:,.2f}")