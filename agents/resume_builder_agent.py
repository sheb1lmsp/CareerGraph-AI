from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from state import State

# Initialize LLM instance
llm = get_llm()

def resume_builder(state: State) -> State:
    """
    CareerGraph AI — Resume Builder Agent (ATS + HR Selection Model)

    Dynamically generates optimized resumes depending on available data:
    - Both Job Description & Resume → Tailor resume precisely to role.
    - Only Job Description → Create resume using profile data, tailored to JD.
    - Only Resume → Improve and optimize that resume.
    - Neither → Build complete resume only from user's profile (skills, experience, etc.).

    Phase 1 — ATS Engine:
        • Produces 5 ATS-optimized variations (technical, managerial, concise, etc.)
    Phase 2 — HR Reviewer:
        • Picks the most impactful version and outputs only that resume.
    """

    # Extract metadata safely
    metadata = state.get("metadata", {})
    job_description = metadata.get("job_description", {})
    resume_data = metadata.get("resume_data", {})

    # Extract general state info
    input_text = state.get("input_text", "")
    memory_summary = state.get("memory_summary", "")
    skills = state.get("skills", [])
    experience = state.get("experience", [])
    education = state.get("education", [])
    projects = state.get("projects", [])
    certifications = state.get("certifications", [])

    context_parts = []
    tailoring_instruction = ""

    # === Case 1: Both JD + Resume present ===
    if job_description.get("is_job_description") and resume_data.get("is_resume"):
        tailoring_instruction = (
            "Both a job description and a resume are provided. "
            "Tailor the resume exactly for this role, aligning achievements and skills "
            "to the job’s required qualifications. Keep ATS optimization and clarity."
        )
        context_parts.append("=== Job Description ===\n")
        context_parts.append(
            f"Role: {job_description.get('job_title', 'N/A')}\n"
            f"Company: {job_description.get('company', 'N/A')}\n"
            f"Required Skills: {', '.join(job_description.get('required_skills', []))}\n"
            f"Responsibilities: {', '.join(job_description.get('responsibilities', []))}\n"
            f"Experience Level: {job_description.get('experience_level', 'N/A')}\n"
            f"Summary: {job_description.get('summary', '')}\n"
        )
        context_parts.append("\n=== Existing Resume ===\n")
        context_parts.append(str(resume_data))

    # === Case 2: Only JD present ===
    elif job_description.get("is_job_description"):
        tailoring_instruction = (
            "Only a job description is available. Use the user’s stored profile "
            "to build a tailored resume aligned to this job’s role and requirements."
        )
        context_parts.append("=== Job Description ===\n")
        context_parts.append(
            f"Role: {job_description.get('job_title', 'N/A')}\n"
            f"Company: {job_description.get('company', 'N/A')}\n"
            f"Required Skills: {', '.join(job_description.get('required_skills', []))}\n"
            f"Responsibilities: {', '.join(job_description.get('responsibilities', []))}\n"
            f"Experience Level: {job_description.get('experience_level', 'N/A')}\n"
        )
        context_parts.append("\n=== User Profile ===\n")
        context_parts.append(
            f"Skills: {', '.join(skills)}\n"
            f"Experience: {', '.join([exp.get('title', 'N/A') + ' at ' + exp.get('company', 'N/A') for exp in experience])}\n"
            f"Education: {', '.join([edu.get('degree', 'N/A') + ' at ' + edu.get('university', 'N/A') for edu in education])}\n"
            f"Projects: {', '.join([p.get('name', 'N/A') for p in projects])}\n"
            f"Certifications: {', '.join([c.get('name', 'N/A') for c in certifications])}\n"
        )

    # === Case 3: Only Resume present ===
    elif resume_data.get("is_resume"):
        tailoring_instruction = (
            "Only a resume is provided. Improve and optimize it for ATS compliance and clarity. "
            "Use user profile data to fill missing gaps or enhance detail."
        )
        context_parts.append("=== Existing Resume ===\n")
        context_parts.append(str(resume_data))
        context_parts.append("\n=== User Profile Supplement ===\n")
        context_parts.append(
            f"Skills: {', '.join(skills)}\n"
            f"Experience: {', '.join([exp.get('title', 'N/A') + ' at ' + exp.get('company', 'N/A') for exp in experience])}\n"
        )

    # === Case 4: No JD or Resume ===
    else:
        tailoring_instruction = (
            "No job description or resume provided. Build a professional, "
            "ATS-optimized resume based solely on user profile data."
        )
        context_parts.append("=== User Profile ===\n")
        context_parts.append(
            f"Skills: {', '.join(skills)}\n"
            f"Experience: {', '.join([exp.get('title', 'N/A') + ' at ' + exp.get('company', 'N/A') for exp in experience])}\n"
            f"Education: {', '.join([edu.get('degree', 'N/A') + ' at ' + edu.get('university', 'N/A') for edu in education])}\n"
            f"Projects: {', '.join([p.get('name', 'N/A') for p in projects])}\n"
            f"Certifications: {', '.join([c.get('name', 'N/A') for c in certifications])}\n"
        )

    combined_context = "\n".join(context_parts)

    # Prompt definition
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            f"""
            You are the Resume Builder Agent for CareerGraph AI.

            {tailoring_instruction}

            Use the information and memory context below to generate your output.

            === PROCESS ===
            Phase 1 — ATS Engine:
              • Generate FIVE unique, ATS-optimized resume drafts (technical, managerial, concise, academic, creative).
              • Each follows this structure:
                ======================
                [FULL NAME]
                [PROFESSIONAL SUMMARY]
                [SKILLS]
                [EXPERIENCE]
                [PROJECTS]
                [EDUCATION]
                [CERTIFICATIONS]
                ======================

            Phase 2 — HR Reviewer:
              • Choose the ONE resume version most likely to pass both ATS and human review.
              • Output ONLY that chosen resume.
              • Do NOT include the other drafts or your reasoning.
              • Keep formatting consistent and professional.
            """
        ),
        (
            "human",
            """
            Memory Summary:
            {memory_summary}

            User Query:
            {input_text}

            Context Information:
            {combined_context}
            """
        )
    ])

    # LLM Execution
    chain = prompt | llm
    response = chain.invoke({
        "input_text": input_text,
        "combined_context": combined_context,
        "memory_summary": memory_summary,
    })

    # Save to state
    state["response"] = response.content.strip()
    return state
