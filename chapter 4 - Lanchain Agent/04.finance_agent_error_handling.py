# a Financial Assistant Agent based on user context
# handle error from tools using wrap_tool_call middleware

from langchain.agents import create_agent
from langchain.tools import tool

from dataclasses import dataclass
from transaction_data import USER_DATABASE  #import the data in transaction_data.py
from transaction_data import SYSTEM_PROMPT
from langchain.tools import ToolRuntime

from langchain.chat_models import init_chat_model
from langchain.agents.middleware import (
    wrap_model_call,
    dynamic_prompt,
    ModelRequest,
    ModelResponse,

    wrap_tool_call
)

from langchain_core.messages import ToolMessage
from langchain.tools.tool_node import ToolCallRequest


from dotenv import load_dotenv
load_dotenv()


# define the different models that can be used
basic_model = init_chat_model(
    "gpt-4o-mini",
    temperature = 0.5,
    max_tokens = 512
)
premium_model = init_chat_model(
    "gpt-4o",
    max_tokens = 2048
)
platinum_model = init_chat_model(
    "gpt-4o"
)



# Define model swapping middleware 



# create data class
@dataclass
class UserContext:
    user_id: str
    user_name: str 
    membership_tier: str # basic, premium, platinum
    preferred_currency: str 


@wrap_tool_call
def handle_tool_errors(request:ToolCallRequest, handler)->ToolMessage:
    """ Gracefully handles tool execution errros"""

    #get the name of the tool that throws the error
    tool_name = request.tool_call["name"]

    try:
        # Attent to execute the tool 
        return handler(request)

    # when attempt fails print to console and also return a ToolMessage with the error 
    except ValueError as e: 
        error_message =f"{tool_name} failed {str(e)}"
        print(f"[ErrorHandler] Caught ValueError: {e}")
        
        return ToolMessage(
            content = error_message,
            tool_call_id = request.tool_call["id"]
        )
    
    except KeyError as e:   
        error_message =f"{tool_name} error: Required data not found -  {str(e)}"
        print(f"[Error Handler] Caught Key Error: {e}")

        return ToolMessage(
            content = error_message,
            tool_call_id = request.tool_call["id"]
        )
    
    except Exception as e: # 
        error_message =f"{tool_name} Encountered an error: Please try again or contact support"
        print(f"[Error Handler] Caught unexpected error: {type(e).__name__} -  {e}")

        return ToolMessage(
            content = error_message,
            tool_call_id = request.tool_call["id"]
        )


@wrap_model_call
def dynamic_model_selector(request:ModelRequest, handler)->ModelResponse:
    """ Select Models based on users membershiop tier"""
    
    tier = request.runtime.context.membership_tier

    if tier =="platinum":
        request.override(model=platinum_model)
        print(f"[middleware] Using PLATINUM model (gpt-40, limiteless)")
    elif tier =="premium":
        request.override(model=premium_model)
        print(f"[middleware] Using PREMIUM model (gpt-40, 2048 tokens)")
    else:
        request.override(model=basic_model)
        print(f"[middleware] Using BASE model (gpt-40, 512 tokens)")

    return handler(request)
        

@dynamic_prompt
def tier_based_prompt(request:ModelRequest)->str:
    """ Generate System Prompt based on Membership Tier"""

    tier = request.runtime.context.membership_tier
    user_name = request.runtime.context.user_name

    base_prompt = f"""You are a personal financial assitant helping {user_name}

        Your Capabilities:
        - Check account balances (checking, savings, investment)
        - View recent transactions
        - Calculate budget recommendations
        - Provide perosnalized greetings
    """

    if tier=="premium":
        return base_prompt + """
        PREMIUM MEMBER BENEFITS:
        - Provide helpful explanations with your response
        - Offer occassional tips for financial improvement
        - Be firendly and informative
        - Balance detail with brevity
    """
    elif tier=="platinum":
        return base_prompt + """
        PLATINUM MEMBER BENEFITS:
        - Provide detailed, comprehensive financial analysis
        - Offer proactive suggestions for wealth growth
        - Include market insights when relevant
        - Be thorough and consultative in your responses
        - Take extra time to explain complex concepts
        """
    else:
        return base_prompt + """

        Guidelines:
        - Be concise and direct
        - Answer questions efficiently
        - Focus on the specific request
        - Keep responses brief but helpful
        """



@tool
def tranfer_money(
    from_account:str,
    to_account:str,
    amount: float,
    runtime:ToolRuntime
):
    """
    Transfer money between accounts

    Args:
        from_account: Source Account ('checking','savings', 'investment)
        to_account: destination account ('checking','savings', 'investment)
        amount: Account to transfer (must be positive)
    """

    if amount <= 0:
        raise ValueError("Transfer amount must be positive")
    if amount > 10000:
        raise ValueError("Transfer amount exceed daily limit $10,000")
    
    if from_account.lower()==to_account.lower():
        raise ValueError("Cannot transfer to the same account")
    
    user_id = runtime.context.user_id
    user_data = USER_DATABASE.get(user_id)
    accounts = user_data.get("accounts",{})

    from_balance = accounts.get(from_account.lower())

    if from_balance is None:
        raise ValueError(f"Source account '{from_account}' NOT FOUMD")
    
    if to_account.lower() not in accounts:
        raise ValueError(f"Destination account '{to_account}' NOT FOUND")
    

    if from_balance < amount:
        raise ValueError(f"Insufficient fund. {from_balance} balance: ${from_balance: .2f}")
    
    #simulate completed transactioin
    return f"Successfully transferred ${amount: .2f} from {from_account} to  {to_account}"
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
    model = basic_model,
    tools =[
        get_account_balance,
        get_recent_transaction,
        calculate_budget,
        get_personalized_greeting,
        tranfer_money
    ],
    # system_prompt=SYSTEM_PROMPT,
    context_schema = UserContext,
    middleware=[
        dynamic_model_selector,
        tier_based_prompt,
        handle_tool_errors
    ]
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

    matthew_context = UserContext(
        user_id = "user_003",
        user_name="Matthew Johnson",
        membership_tier="premium",
        preferred_currency="USD"
    )

    # Test 1: Check Balance
    # balance_message = "What's my checking account balance?"
    # transfer_money_prompt = "Transfer $500 from checking to savings" #successful transfer
    # transfer_money_prompt = "Transfer $5000 from checking to savings" #unsuccessful transfer - insufficient funds
    transfer_money_prompt = "Transfer $5000 from checking to checkings" #unsuccessful transfer - transfer to same account 

    print(f"\nQuery: {transfer_money_prompt}")
    print("*"*40)
    response = agent.invoke(
        {
            "messages": [{"role":"user","content": transfer_money_prompt}]
        },
        context=alice_context
    )

    print(f"Agent: {response['messages'][-1].content}")

 


if __name__=="__main__":
    main()