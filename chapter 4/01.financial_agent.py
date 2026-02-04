# a Financial Assistant Agent

from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def get_account_balance(account_type:str)->str:
    """
     GEt the current balance for a specific account
     Args: 
        account_type: Type of account = 'checking', saving',or 'investment'
    """

    balances = {
        "checking": 25000.00,
        "savings": 15000.00,
        "investment": 45000.00
    }

    balance = balances.get(account_type.lower())
    if balance is not None:
        return f"Your {account_type} account  balance is ${balance:,.2f}"
    return f"Unknown account type {account_type}.\nAvailable account types are Checking, Savings and Investment "


@tool
def get_recent_transaction(account_type: str, Limit: int = 5) -> str:
    """
     Get recent transactions for an account

     Args:
        account_type: Type of account = 'checking', saving',or 'investment'
        limit: Number of transaction to return. default is 5
    """
    transactions = {
        "checking":[
            {"date":"2025-01-15", "description": "Grocery Store", "amount":-85.50},
            {"date":"2025-01-14", "description": "Direct Deposit", "amount":3200.00},
            {"date":"2025-01-13", "description": "Electricity Bill", "amount":-120.00},
            {"date":"2025-01-12", "description": "Restaurant", "amount":-45.00},
            {"date":"2025-01-11", "description": "Gas Station", "amount":-55.00},
             
        ],
        "savings": [
            {"date":"2025-01-01", "description": "Interest Payment", "amount":12.50},
            {"date":"2025-01-01", "description": "Transfer from Checking", "amount":500.00}
            
        ],
        "investment":[
            {"date":"2025-01-14", "description": "Divident -  AAPL", "amount":125.00},
            {"date":"2025-01-10", "description": "Buy - VTI", "amount":-1000.00},

        ]
    } 

    account_transactions = transactions.get(account_type.lower(),[])[:Limit]

    if not account_transactions:
        return f"No Transaction found for {account_type}"
    
    result = f" Recent transaction for {account_type}:\n"

    for t in account_transactions:
        sign = "+" if t["amount"] > 0 else ""
        result +=f"{t['date']} : {t['description']} ({sign}${t['amount']:,.2f})\n"
    
    return result

 
     






@tool
def calculate_budget(monthly_income: float, expense_category: str )-> str:
    """
    Calculate recommedned budget allocation for an expense category
    Args:
        monthly_income: User's monthly income
        expense_category: Categories like 'housing','food' etc
    """
    allocations = {
        "housing": 0.30,
        "food" : 0.12,
        "transportation": 0.10,
        "utilities": 0.08,
        "savings": 0.20,
        "entertainment": 0.05,
        "healthcare": 0.05,
        "others": 0.30
    }

    percentage = allocations.get(expense_category.lower())

    if percentage is None:
        return f"Unknow Categories: {expense_category}. Available Categories {', '.join(allocations.keys())}"
    
    recommendation = monthly_income * percentage

    return f"Recommended  {expense_category} budget: ${recommendation:,.2f}/month ({percentage*100:.0f}% of income)"



SYSTEM_PROMPT = """
You are a helpful perosnal finance assistant.

Your Capabilities:
- Check account balance (checking, savings, investment)
- view recent transactions
- Calculate budget recommendations

Guideline:
- Be helpful and informative
- provide clear, actionable advice
- Use tools to get accurate information before responding
- Format monetary values clearly
"""


agent =create_agent( # create_openai_functions_agent( #create_agent(
    model = "gpt-4o",
    tools =[
        get_account_balance,
        get_recent_transaction,
        calculate_budget
    ],
    system_prompt=SYSTEM_PROMPT
)



def main():
    print("="*60)
    print("Stage 1: Simple finance Assistant")
    print("="*60)

    #Test :Queries
    # user_message = "What's my checking account balance"
    # user_message = "Show me my savings balance and recent transactions" # this uses more than one tool (get_account_balance & get_recent_transaction)
    user_message = "I make $5000/month, how much should I spend on housing"

    print(f"\nQuery: {user_message}")
    response = agent.invoke({
        "messages": [{"role":"user", "content": user_message}]
    })

    print(f"Agent: {response['messages'][-1].content}")

 


if __name__=="__main__":
    main()