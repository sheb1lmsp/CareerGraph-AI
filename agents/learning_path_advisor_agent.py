from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State
from typing import List

# Initialize LLM instance
llm = get_llm()

class LearningPath(BaseModel):
    """Structured schema representing a user's personalized learning roadmap."""
    target_role: str = Field(description="The career goal or target role the user aims to achieve.")
    required_skills: List[str] = Field(description="New or complementary skills the user needs to learn.")
    roadmap_steps: List[str] = Field(description="Ordered learning steps or milestones.")
    recommended_resources: List[str] = Field(description="Suggested learning materials or platforms.")
    summary: str = Field(description="A concise overview of the personalized learning roadmap.")


def learning_path_advisor(state: State) -> State:
    """
    Agent Node: Generates a step-by-step learning roadmap toward the user's target role.

    This agent analyzes the user's background, known skills, and career goals to design
    a progressive, goal-oriented learning plan. It avoids recommending already-known topics
    and emphasizes real-world applicability and measurable growth.
    """
    # Extract key profile elements from the shared state
    user_input = state.get("input_text", "")
    known_skills = ", ".join(state.get("skills", []))
    certifications = state.get("certifications", [])
    education = state.get("education", [])
    experience = state.get("experience", [])
    projects = state.get("projects", [])
    memory_summary = state.get("memory_summary", "") 

    # Build the structured LLM prompt
    learning_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the LearningPath Advisor for CareerGraph AI.
            Your role is to create personalized, practical, and efficient learning roadmaps
            tailored to each user’s profile, skills, and career ambitions.

            ✅ Guidelines:
            - Recommend only NEW or relevant skills (avoid known ones).
            - Exclude any courses, certifications, or topics the user already completed.
            - Keep steps chronological, measurable, and realistic.
            - Include real-world projects, milestones, and portfolio tasks.
            - Use the conversation memory to maintain context continuity.
            - If no goal is provided, infer a likely target role.
            """
        ),
        (
            "human",
            """
            User Query: {user_input}

            Memory Summary: {memory_summary}

            Profile Summary:
            - Known Skills: {known_skills}
            - Certifications: {certifications}
            - Education: {education}
            - Experience: {experience}
            - Projects: {projects}

            Provide a structured learning roadmap with:
            - target_role
            - required_skills (excluding known ones)
            - roadmap_steps (in logical order)
            - recommended_resources
            - summary
            """
        ),
    ])

    # Chain the prompt with structured output schema
    chain = learning_prompt | llm.with_structured_output(LearningPath)

    # Invoke the LLM with user context and memory
    response = chain.invoke({
        "user_input": user_input,
        "known_skills": known_skills,
        "certifications": certifications,
        "education": education,
        "experience": experience,
        "projects": projects,
        "memory_summary": memory_summary,
    })

    # Format output into a user-friendly text block
    formatted_output = (
        f"🎯 Target Role: {response.target_role}\n\n"
        f"🧩 Required Skills: {', '.join(response.required_skills)}\n\n"
        f"🪜 Learning Roadmap:\n" + "\n".join([f"- {step}" for step in response.roadmap_steps]) + "\n\n"
        f"📘 Recommended Resources:\n" + "\n".join([f"- {r}" for r in response.recommended_resources]) + "\n\n"
        f"📝 Summary: {response.summary}"
    )

    # Store result back in shared state
    state["response"] = formatted_output
    return state
