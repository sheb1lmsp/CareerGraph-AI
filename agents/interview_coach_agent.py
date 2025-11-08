from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def interview_coach(state: State) -> State:
    """
    CareerGraph AI — Interview Coach Agent

    Dynamically generates interview guidance depending on available data:
    - If both Job Description & Resume are available → use both for a tailored prep plan  
    - If only Job Description is available → focus on that role and requirements  
    - If only Resume is available → focus on the candidate's background  
    - If none are available → use user's profile information from the state  

    Also leverages conversation memory (`memory_summary`) for personalized continuity.

    Output includes:
    1. Role Context
    2. Key Focus Areas
    3. Likely Technical & Behavioral Questions
    4. Preparation Tips
    5. Bonus Recommendations (optional)
    """

    # Extract available metadata
    metadata = state.get("metadata", {})
    job_description = metadata.get("job_description", {})
    resume_data = metadata.get("resume_data", {})

    # Fallback user profile data
    skills = state.get("skills", [])
    experience = state.get("experience", [])
    education = state.get("education", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])
    memory_summary = state.get("memory_summary", "")
    input_text = state.get("input_text", "")

    # Build the context dynamically based on available data
    context_parts = []

    # If Job Description exists
    if job_description and job_description.get("is_job_description", False):
        context_parts.append(
            "Job Description Details:\n"
            f"- Role: {job_description.get('job_title', 'N/A')}\n"
            f"- Company: {job_description.get('company', 'N/A')}\n"
            f"- Required Skills: {', '.join(job_description.get('required_skills', []))}\n"
            f"- Responsibilities: {', '.join(job_description.get('responsibilities', []))}\n"
            f"- Experience Level: {job_description.get('experience_level', 'N/A')}\n"
            f"- Summary: {job_description.get('summary', 'N/A')}\n"
        )

    # If Resume data exists
    if resume_data and resume_data.get("is_resume", False):
        context_parts.append(
            "Resume Details:\n"
            f"- Name: {resume_data.get('name', 'N/A')}\n"
            f"- Skills: {', '.join(resume_data.get('skills', []))}\n"
            f"- Experience: {', '.join(resume_data.get('experience', []))}\n"
            f"- Projects: {', '.join(resume_data.get('projects', []))}\n"
            f"- Education: {', '.join(resume_data.get('education', []))}\n"
        )

    # Fallback — if neither JD nor Resume is present
    if not context_parts:
        context_parts.append(
            "User Profile Summary:\n"
            f"- Skills: {', '.join(skills)}\n"
            f"- Experience: {', '.join([exp.get('title', 'N/A') + ' at ' + exp.get('company', 'N/A') for exp in experience])}\n"
            f"- Education: {', '.join([edu.get('degree', 'N/A') + ' at ' + edu.get('university', 'N/A') for edu in education])}\n"
            f"- Projects: {', '.join([p.get('name', 'N/A') for p in projects])}\n"
            f"- Certifications: {', '.join([c.get('name', 'N/A') for c in certifications])}\n"
        )

    # Combine all context parts
    combined_context = "\n\n".join(context_parts)

    # Define the LLM prompt
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the **Interview Coach Agent** for CareerGraph AI.

            Your mission:
            - Prepare the user for their upcoming job interview.
            - Use Job Description and/or Resume data if provided.
            - If only user profile info is available, base preparation on that.
            - If `memory_summary` is provided, use it to recall the user's previous interactions.

            Output structure:
            1. Role Context (1–2 lines)
            2. Key Focus Areas
            3. Likely Technical Questions
            4. Behavioral Questions
            5. Preparation Tips
            6. Bonus Recommendations (optional)

            Keep tone professional, supportive, and realistic.
            Output plain text only (no markdown or JSON).
            """
        ),
        (
            "human",
            """
            Memory Summary:
            {memory_summary}

            User Query:
            {input_text}

            Combined Context:
            {combined_context}
            """
        )
    ])

    # Execute the chain with context + memory
    chain = prompt | llm
    response = chain.invoke({
        "input_text": input_text,
        "combined_context": combined_context,
        "memory_summary": memory_summary,
    })

    # Save the LLM response to shared state
    state["response"] = response.content.strip()

    return state
