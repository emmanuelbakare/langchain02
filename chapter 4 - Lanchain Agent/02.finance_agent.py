# a Financial Assistant Agent based on user context
# it get a user and use the user data to answer the financial information

from langchain.agents import create_agent
from langchain.tools import tool

from dataclasses import dataclass
from transaction_data import USER_DATABASE  #import the data in transaction_data.py
from transaction_data import SYSTEM_PROMPT
from langchain.tools import ToolRuntime

from dotenv import load_dotenv

load_dotenv()


# create data class
@dataclass
class UserContext:
    user_id: str
    user_name: str 
    membership_tier: str # basic, premium, platinum
    preferred_currency: str 


@tool
def get_account_balance(
    account_type:str, 
    runtime: ToolRuntime[UserContext]
    )->str:
    """
     GEt the current balance for a specific account
     Args: 
        account_type: Type of account = 'checking', saving',or 'investment'
    """
    user_id = runtime.context.user_id
    currency = runtime.context.preferred_currency
    user_data = USER_DATABASE.get(user_id,{})

    balance =user_data.get("accounts", {}).get(account_type.lower())

    if balance is not None:
        if currency == "EUR":
            balance = balance * 0.92
        return f"Your {account_type} account balance is ${balance:,.2f}"
    return f"Unknown account type ({account_type}) Available account types are checking, savings and investment"

     

@tool
def get_recent_transaction(
    account_type: str, 
    Limit: int = 5,
    runtime: ToolRuntime[UserContext] = None) -> str:
    """
     Get recent transactions for an account

     Args:
        account_type: Type of account = 'checking', saving',or 'investment'
        limit: Number of transaction to return. default is 5
    """
    user_id = runtime.context.user_id
    user_data = USER_DATABASE.get(user_id,{})
    account_transactions = user_data.get("transactions", {}).get(account_type.lower(),[])[:Limit]


    if not account_transactions:
        return f"No Transaction found for {account_type}"
    
    result = f" Recent transaction for {account_type}:\n"

    for t in account_transactions:
        sign = "+" if t["amount"] > 0 else ""
        result +=f"{t['date']} : {t['description']} ({sign}${t['amount']:,.2f})\n"
    
    return result

 
     

@tool
def get_personalized_greeting(runtime:ToolRuntime[UserContext]) -> str:
    """
    Get a personalized greeting for the user, No arguents required
    """

    name= runtime.context.user_name 
    tier = runtime.context.membership_tier

    tier_benefits = {
        "basic": "Youo have access to standard features",
        "premium": "As a premium member, you get priority support and davanced analytics",
        "platinum": "Welconme, platinum member! You have access to all features including personal advisor consultations"
    }

    benefit_msg = tier_benefits.get(tier,"")




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


# System Prompt



agent = create_agent(
    model = "gpt-4o",
    tools =[
        get_account_balance,
        get_recent_transaction,
        calculate_budget,
        get_personalized_greeting
    ],
    system_prompt=SYSTEM_PROMPT,
    context_schema = UserContext
)



def main():
    print("="*60)
    print("Stage 1: Simple finance Assistant")
    print("="*60)

    alice_context = UserContext(
        user_id = "user_001",
        user_name="Alice Johnson",
        membership_tier="platinum",
        preferred_currency="USD"
    )

    bob_context = UserContext(
        user_id = "user_002",
        user_name="Bob Smith",
        membership_tier="basic",
        preferred_currency="EUR"
    )

    # Test 1: Check Balance
    balance_message = "What's my checking account balance?"

    print(f"\nQuery: {balance_message}")
    response = agent.invoke(
        {
            "messages": [{"role":"user","content": balance_message}]
        },
        context = alice_context
    )

    print(f"Agent: {response['messages'][-1].content}")

 


if __name__=="__main__":
    main()