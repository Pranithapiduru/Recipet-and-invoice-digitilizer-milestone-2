from ai.gemini_client import ask_gemini


def generate_ai_insights(expense_df) -> str:
    """
    Generate natural language spending insights using Gemini.
    """
    prompt = f"""
    Analyze the following expense data and give clear insights:
    - Spending patterns
    - Highest expense category or merchant
    - Month-over-month trend if visible

    DATA:
    {expense_df.to_string()}
    """

    return ask_gemini(prompt)
