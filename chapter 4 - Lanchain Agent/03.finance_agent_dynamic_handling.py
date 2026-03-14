"""
USING MIDDLEWARE
================
Middleware is used to swap model, prompts etc during runtime. It dynamically determine which model or prompt to run at runtime.
- in this example we will swap models and prompts depending on the type of user membership we have. The agent looks at the user membership to determine which prompt and model to use

New Imports
=============

- from langchain.chat_models import init_chat_model   # used to instantiate model

- from langchain.agents.middleware import (   
    wrap_model_call,  # this is a wrapper on a function ( @wrap_model_call). The function determines which model is used
    dynamic_prompt,  # this a wrapper on a function (@dyanmic_prompt). the function determines which prompt will be used
    ModelRequest,  # use this to get the context data through runtime in a function. e.g mdoel_request.runtime.context.user_id
    ModelResponse # used to return the final result from the request using a handler.
)


1. Instantiate each of the models that will be used using the init_chat_model method
=======================================================
from langchain.chat_models import init_chat_model

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

2. Write the function what will swap model. Wrap it with wrap_model_call
==========================================================================

@wrap_model_call
def dynamic_model_selector(request:ModelRequest, handler)->ModelResponse:
    #this function select a model based on user membership

    # get user membership_tier and user_id through the request:ModelRequest function parameter
    tier = request.runtime.context.membership_tier   # get the context membership type
    user_id = request.runtime.context.user_id #get context user_id

    
    # based on the tier, override the model type as defined using init_chat_model (do same for all tiers)
    if tier =="platinum":
        request.override(model=platinum_model)
    
    #return the request as a ModelResponse
    return handler(request)

3. Write the function that swaps prompt based on criteria from the user

@dynamic_prompt
def tier_based_prompt(request:ModelRequest)->str:
    #Generate System Prompt based on Membership Tier

    tier = request.runtime.context.membership_tier
    user_name = request.runtime.context.user_name

    my_prompt = "my basic prompt here" \
    
    #default is my_prompt but if tier is platinum, use another prompt etc
    if tier == "platinum":
       my_prompt += "adding platinum prompt"
    elif tier =="premium":
       my_prompt += "adding premium prompt"

    return my_prompt

4. add the dynamic_model_selector and tier_based_prompt functions as middleware when creating the agent
======================================================================================================
-let the basic_model  be the default model. The middleware will swap them dynamically when needed 

agent = create_agent(
    model = basic_model,
    tools =[
        get_account_balance,
        ...
    ],
    context_schema = UserContext,
    middleware=[
        dynamic_model_selector,
        tier_based_prompt
    ]
)


5. On running,  create the user_data (context), the query. Agent swaps prompt and model according to user membership
====================================================================================================================

matthew_context = UserContext(
        user_id = "user_003",
        user_name="Matthew Johnson",
        membership_tier="premium",
        preferred_currency="USD"
    )

    financial_situation_query = "What's  my financial situation? Check all my accounts and give me advice"
    response = agent.invoke(
        {
            "messages": [{"role":"user","content": financial_situation_query}]
        },
        context = matthew_context  # matthew_context is premium so the system will use the premium prompt and model variation
    )

    print(f"Agent: {response['messages'][-1].content}")

"""
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
    ModelResponse
)


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
        get_personalized_greeting
    ],
    # system_prompt=SYSTEM_PROMPT,
    context_schema = UserContext,
    middleware=[
        dynamic_model_selector,
        tier_based_prompt
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
    financial_situation_query = "What's  my financial situation? Check all my accounts and give me advice"
    print(f"\nQuery: {financial_situation_query}")
    print("*"*40)
    response = agent.invoke(
        {
            "messages": [{"role":"user","content": financial_situation_query}]
        },
        # context = alice_context  # alice_context is platinum so the system will use the platinum prompt and model variation
        context = bob_context  # bob_context is basic so the system will use the basic prompt and model variation
        # context = matthew_context  # matthew_context is premium so the system will use the premium prompt and model variation
    )

    print(f"Agent: {response['messages'][-1].content}")

 


if __name__=="__main__":
    main()