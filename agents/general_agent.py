from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def general(state: State) -> State:
    """
    Agent Node: Responds to general or uncategorized user queries that don't match
    specific agents like skill_analyzer, course_recommender, etc.
    If the query is not career-related, it explicitly refuses to answer.
    """
    # Extract relevant information from the shared state
    input_text = state.get("input_text", "")
    skills = state.get("skills", [])
    education = state.get("education", [])
    experience = state.get("experience", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])
    memory_summary = state.get("memory_summary", "")

    # Build a general-purpose prompt for free-form conversation
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the General Agent for CareerGraph AI.

            Your task:
            - Handle general, open-ended, or advisory career-related queries.
            - Use the user's background and memory summary for context.
            - If the query is NOT career-related (e.g., about entertainment, math, jokes, or random facts),
              clearly respond with: "Sorry, I can only help with career-related topics."
            - If it IS career-related, provide relevant, professional, and actionable advice.
            - Always output plain text (no markdown, no JSON).
            """
        ),
        (
            "human",
            """
            User Query: {input_text}

            Memory Summary: {memory_summary}

            Profile Data:
            - Skills: {skills}
            - Education: {education}
            - Experience: {experience}
            - Projects: {projects}
            - Certifications: {certifications}
            """
        ),
    ])

    # Chain the prompt with the LLM
    chain = prompt | llm

    # Invoke the model with user and memory context
    response = chain.invoke({
        "input_text": input_text,
        "memory_summary": memory_summary,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    })

    # Save and return the response
    state["response"] = response.content.strip()
    return state
