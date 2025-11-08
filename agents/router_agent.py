from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

class AgentType(BaseModel):
    """Schema defining which agent should handle the user's query."""
    agent_name: str = Field(
        description="The name of the agent that should handle this query."
    )

def router(state: State) -> State:
    """
    Context-aware router for CareerGraph AI.
    Determines which specialized agent should handle the user's query
    using both the latest input and memory summary for context.
    """

    router_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the **RouterAgent** for CareerGraph AI — an intelligent, LLM-powered career assistant.

            Your goal:
            - Analyze the user's current query and overall context (from memory).
            - Determine which specialized agent should respond next.

            **Available agents:**
            1. "skill_analyzer" → For analyzing or improving the user’s skills.
            2. "project_recommender" → For project ideas, feedback, or inspiration.
            3. "course_recommender" → For course or certification suggestions.
            4. "learning_path_advisor" → For structured learning or career roadmaps.
            5. "resume_builder" → For creating or optimizing resumes.
            6. "interview_coach" → For interview guidance and preparation.
            7. "general" → For general assistance outside the above.

            **Output format:**
            Return ONLY one of the agent names listed above as a plain string (no punctuation, no explanations).
            Example:
            skill_analyzer
            """
        ),
        (
            "human",
            """
            User query: {input_text}

            Memory summary of prior context: {memory_summary}
            """
        )
    ])

    # Chain combines the structured prompt with the Gemini model output
    chain = router_prompt | llm.with_structured_output(AgentType)

    # Invoke router with both input and memory summary
    response = chain.invoke({
        "input_text": state["input_text"],
        "memory_summary": state.get("memory_summary", "")
    })

    # Return updated state with the chosen agent
    return {**state, "agent_action": response.agent_name}
