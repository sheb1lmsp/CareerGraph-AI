from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def project_recommender(state: State) -> State:
    """
    Agent Node: Suggests creative and technically relevant project ideas for the user.

    This agent analyzes the user's profile — skills, education, experience, and goals —
    to recommend unique, high-impact project ideas that improve employability and portfolio depth.
    It ensures that suggestions avoid overlap with existing projects and remain challenging yet achievable.

    Args:
        state (State): The current shared CareerGraph AI state.

    Returns:
        State: Updated state containing project recommendations in 'response'.
    """

    # Extract user info and context from the shared state
    user_skills = ", ".join(state.get("skills", []))
    education = state.get("education", [])
    experience = state.get("experience", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])
    user_query = state.get("input_text", "")
    memory_summary = state.get("memory_summary", "")

    # Define the project recommendation prompt
    project_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the ProjectRecommender Agent for CareerGraph AI.

            Your task:
            - Suggest unique, high-impact project ideas tailored to the user’s skills, experience, and goals.
            - Help the user build portfolio depth and improve employability.

            ⚙️ Rules:
            - Do NOT suggest projects too similar to existing ones.
            - Suggest 3–5 creative, technically strong project ideas.
            - Include a one-line reason why each project is valuable.
            - Prefer ideas slightly above current skill level to encourage growth.
            - Avoid trivial projects (e.g., "To-Do App", "Calculator App").
            - Output plain text only — no markdown, no JSON.

            🎯 Example directions:
            - For AI/ML skills → applied ML, NLP, GenAI, automation.
            - For software/dev → scalable systems, developer tools.
            - For data analytics → dashboards, predictive models, business insights.
            """
        ),
        (
            "human",
            """
            User query or goal:
            {user_query}

            Memory summary (context from prior interactions):
            {memory_summary}

            User profile:
            - Skills: {user_skills}
            - Education: {education}
            - Experience: {experience}
            - Certifications: {certifications}
            - Existing Projects: {projects}

            Recommend 3–5 unique, creative projects the user can build next.
            Each should include:
            1. Project Name — short and creative
            2. Description — one sentence
            3. Why — brief reason of value

            Format strictly:
            1. [Project Name]
               Description: ...
               Why: ...
            """
        ),
    ])

    # Build the chain and invoke with all context
    chain = project_prompt | llm
    response = chain.invoke({
        "user_query": user_query,
        "memory_summary": memory_summary,
        "user_skills": user_skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    })

    # Store generated projects in the state
    state["response"] = response.content.strip()

    # Return the updated state
    return state
