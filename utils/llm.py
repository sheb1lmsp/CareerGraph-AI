from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm(model_name: str = "gemini-2.5-flash"):
    """
    Initialize and return a Google Generative AI (Gemini) model instance.

    Args:
        model_name (str, optional): Model name to use. Defaults to "gemini-2.5-flash".

    Returns:
        ChatGoogleGenerativeAI: Initialized LLM instance for use across the project.
    """
    # Load environment variables (expects GOOGLE_API_KEY in .env)
    load_dotenv()

    # Initialize the LLM with the specified model name
    llm = ChatGoogleGenerativeAI(model=model_name)

    return llm
