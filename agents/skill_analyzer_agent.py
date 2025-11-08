from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def skill_analyzer(state: State) -> State:
    """
    Agent Node: Analyzes the user's skills, experience, and projects to identify
    their core strengths, weaknesses, and upskilling opportunities.
    """
    # Extract all relevant information from the state
    input_text = state.get("input_text", "")
    skills = state.get("skills", [])
    education = state.get("education", [])
    experience = state.get("experience", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])
    memory_summary = state.get("memory_summary", "") 

    # Build the structured prompt for the LLM
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the Skill Analyzer Agent for CareerGraph AI.

            Your task:
            - Analyze the user's skills, experience, and projects.
            - Identify their strongest and most relevant skills.
            - Highlight weak or missing skill areas.
            - Recommend next-step upskilling opportunities (tools, frameworks, or soft skills).
            - Use conversation memory to ensure continuity and avoid repeating suggestions.

            Output format (plain text only):
            Core Strengths:
            - ...

            Missing / Weak Skills:
            - ...

            Recommended Upskilling:
            - ...

            Suggested Courses / Certifications:
            - ...
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

    # Chain the prompt with the LLM and generate analysis
    chain = prompt | llm
    response = chain.invoke({
        "input_text": input_text,
        "memory_summary": memory_summary,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    })

    # Store the generated analysis in the state
    state["response"] = response.content.strip()
    return state
