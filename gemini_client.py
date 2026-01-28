import google.generativeai as genai

def summarize_receipt(api_key, text):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-pro")
    return model.generate_content(text).text
