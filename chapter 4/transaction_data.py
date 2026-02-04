USER_DATABASE = {
    "user_001": {
        "name": "Alice Johnson",
        "accounts": {
            "checking": 3200.00,
            "savings": 18500.00,
            "investment": 52000.00
        },
        "transactions": {
            "checking": [
                {"date": "2025-02-01", "description": "Supermarket", "amount": -120.75},
                {"date": "2025-01-31", "description": "Salary Deposit", "amount": 3500.00},
            ],
            "savings": [
                {"date": "2025-02-01", "description": "Interest Payment", "amount": 15.20},
            ],
            "investment": [
                {"date": "2025-01-28", "description": "Dividend - AAPL", "amount": 140.00},
            ],
        },
    },

    "user_002": {
        "name": "Bob Smith",
        "accounts": {
            "checking": 1450.00,
            "savings": 6200.00,
            "investment": 9800.00
        },
        "transactions": {
            "checking": [
                {"date": "2025-02-02", "description": "Fuel Station", "amount": -65.00},
                {"date": "2025-01-30", "description": "Freelance Payment", "amount": 1800.00},
            ],
            "savings": [
                {"date": "2025-01-25", "description": "Transfer from Checking", "amount": 500.00},
            ],
            "investment": [
                {"date": "2025-01-20", "description": "Buy - VOO", "amount": -1200.00},
            ],
        },
    },

    "user_003": {
        "name": "Matthew Johnson",
        "accounts": {
            "checking": 4100.00,
            "savings": 22000.00,
            "investment": 30500.00
        },
        "transactions": {
            "checking": [
                {"date": "2025-02-03", "description": "Restaurant", "amount": -90.00},
                {"date": "2025-02-01", "description": "Business Income", "amount": 4200.00},
            ],
            "savings": [
                {"date": "2025-02-01", "description": "Interest Payment", "amount": 18.40},
            ],
            "investment": [
                {"date": "2025-01-18", "description": "Dividend - MSFT", "amount": 110.00},
            ],
        },
    },
}


SYSTEM_PROMPT = """
You are a helpful perosnal finance assistant.

Your Capabilities:
- Check account balance (checking, savings, investment)
- view recent transactions
- Calculate budget recommendations
- PRovide perosnalized greetings

Guideline:
- Be helpful and informative
- provide clear, actionable advice
- Use tools to get accurate information before responding
- Format monetary values clearly

Guidelines:
- Be helpful and informative
- Always start by greeting the user  
- Provide clear, actionable advice
- Use tools to get accurate, user-specific information
- Formart monetary values clearly
- Tailor advice based on the user's membership tier
"""


