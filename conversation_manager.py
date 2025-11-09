from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from graph_builder import build_graph

# Initialize LLM instance
llm = get_llm()

# Initialize LangGraph Multi-Agent
app = build_graph()

# Exit Detection Prompt
exit_prompt = ChatPromptTemplate.from_template(
    """
    You are a conversation manager.
    Given the user's latest message, decide if the user wants to end the conversation.

    If the user clearly says something like "bye", "thank you", "stop", "exit", "goodnight", etc., 
    respond ONLY with the single word: "exit".
    Otherwise, respond ONLY with the word: "continue"

    User message:
    {user_input}
    """
)

# Combine prompt with the language model
exit_chain = exit_prompt | llm

def manager(user_input: str, memory: list, user_id: int) -> str:
    # Initialize Memory
    memory_summary = ""  # Compressed summary of recent context

    # Check if user wants to end the conversation
    should_continue = exit_chain.invoke({'user_input': user_input}).content.strip()

    if should_continue == "exit":
        return "Goodbye 👋"

    # If there’s existing conversation, summarize it
    if len(memory) != 0:
        summary_prompt = ChatPromptTemplate.from_template(
            "Summarize the key context of this conversation in 5 concise sentences:\n\n{conversation}"
        )
        formatted = "\n".join(memory)
        chain = summary_prompt | llm
        memory_summary = chain.invoke({"conversation": formatted}).content.strip()
    else:
        memory_summary = ""

    # Build the current conversation state
    state = {
        "input_text": user_input,
        "memory_summary": memory_summary,
        "user_id" : user_id
    }

    # Invoke the main LangGraph app (routes to the right agent)
    result = app.invoke(state)
    response = result.get("response", "(No response)")

    # Display AI response
    return response
