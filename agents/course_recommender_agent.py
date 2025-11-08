from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def course_recommender(state: State) -> State:
    """
    Agent Node: Suggests relevant courses or certifications based on the user's profile.

    This agent analyzes the user's current skills, education, projects, and certifications
    to recommend 3–5 relevant courses or certifications from top learning platforms.
    It avoids recommending duplicates or already-completed certifications.

    Args:
        state (State): The current shared CareerGraph AI state.

    Returns:
        State: Updated state with 'response' containing the course recommendations.
    """

    # Extract key user info from the shared state
    user_skills = state.get("skills", [])
    education = state.get("education", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])
    user_query = state.get("input_text", "")
    memory_summary = state.get("memory_summary", "")

    # Define the prompt with memory and structured context
    course_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the CourseRecommender Agent for CareerGraph AI.

            Your goal is to suggest highly relevant online courses or certifications
            from platforms like Coursera, Udemy, edX, Google, or LinkedIn Learning
            that help the user progress in their desired career path.

            ⚠️ Rules:
            - Do NOT recommend any course or certification the user already has or mentioned.
            - Do NOT repeat known certifications.
            - Focus on next-step or complementary learning.
            - Recommend 3–5 courses only.
            - For each course: include platform and one-line relevance.
            - Output must be plain text (no JSON, no markdown).
            """
        ),
        (
            "human",
            """
            User query or goal:
            {user_query}

            Memory summary (context from previous discussion):
            {memory_summary}

            User profile:
            - Skills: {user_skills}
            - Education: {education}
            - Projects: {projects}
            - Completed Certifications: {certifications}

            Return 3–5 unique, relevant courses in this format:

            1. [Course Name] — [Platform]
               Why: [One-line reason]
            2. [Course Name] — [Platform]
               Why: [One-line reason]
            """
        ),
    ])

    # Build the chain and get model output
    chain = course_prompt | llm
    response = chain.invoke({
        "user_query": user_query,
        "memory_summary": memory_summary,
        "user_skills": user_skills,
        "education": education,
        "projects": projects,
        "certifications": certifications,
    })

    # Store the AI's course recommendations in the shared state
    state["response"] = response.content.strip()

    # Return updated state
    return state
