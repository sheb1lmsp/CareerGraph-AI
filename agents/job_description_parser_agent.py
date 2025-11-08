from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

class JobDescriptionModel(BaseModel):
    """Structured schema representing extracted details from a job description."""
    is_job_description: bool = Field(description="True if the input contains a job description or job post.")
    job_title: str = Field(default="", description="The job title or role name, if mentioned.")
    company: str = Field(default="", description="The company name, if mentioned.")
    required_skills: List[str] = Field(default_factory=list, description="List of technical or soft skills mentioned.")
    responsibilities: List[str] = Field(default_factory=list, description="List of key responsibilities or tasks mentioned.")
    experience_level: str = Field(default="", description="Experience level (e.g., Entry-level, Mid-level, Senior), if detectable.")
    summary: str = Field(default="", description="2-line summary of what the role is about.")


def job_description_parser(state: State) -> State:
    """
    Agent Node: Parses structured job description data from the user's input.

    This agent:
    - Detects whether the text is a job description.
    - Extracts relevant structured information.
    - Stores it under `state['metadata']['job_description']`.
    - Does NOT produce direct output; it's used for internal data enrichment.
    """
    user_query = state.get("input_text", "")

    jd_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the JobDescriptionParser Agent for CareerGraph AI.

            Your task:
            - Detect if the user input contains a job description or job post.
            - If yes, extract:
              • job_title
              • company
              • required_skills
              • responsibilities
              • experience_level
              • summary
            - If not, set is_job_description=False.
            - Be concise, structured, and factual.
            - Return only structured output, no commentary or natural language text.
            """
        ),
        (
            "human",
            "User Input:\n{user_query}"
        )
    ])

    # Structured LLM call
    chain = jd_prompt | llm.with_structured_output(JobDescriptionModel)
    response = chain.invoke({"user_query": user_query})

    # Initialize metadata container if missing
    if state.get("metadata") is None:
        state["metadata"] = {}

    # Store extracted job description details
    state["metadata"]["job_description"] = response.model_dump()

    return state
