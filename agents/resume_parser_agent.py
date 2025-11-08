from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
from utils.llm import get_llm
from state import State
from utils.extract_resume import extract_resume_text

# Initialize LLM instance
llm = get_llm()

class ResumeModel(BaseModel):
    """Structured schema representing parsed resume information."""
    is_resume: bool = Field(description="True if the input contains a resume.")
    name: str = Field(default="", description="Full name of the candidate, if available.")
    email: str = Field(default="", description="Email address of the candidate, if mentioned.")
    phone: str = Field(default="", description="Phone number, if available.")
    summary: str = Field(default="", description="Brief 2–3 line professional summary.")
    skills: List[str] = Field(default_factory=list, description="List of technical or soft skills.")
    education: List[str] = Field(default_factory=list, description="List of educational qualifications and institutions.")
    experience: List[str] = Field(default_factory=list, description="List of work experience entries or job roles.")
    certifications: List[str] = Field(default_factory=list, description="List of certifications or achievements.")
    projects: List[str] = Field(default_factory=list, description="List of project titles or brief descriptions.")
    total_experience_years: float = Field(default=0.0, description="Approximate total years of experience.")


def resume_parser(state: State) -> State:
    """
    Resume Parser Agent — extracts structured data from resumes.

    This agent uses LLM parsing to convert unstructured resume text into a 
    structured dictionary that downstream agents (like Interview Coach or 
    Resume Builder) can consume.

    Behavior:
    - Reads text from the provided resume file (PDF or DOCX).
    - Parses fields like name, email, skills, experience, etc.
    - Stores results inside `state['metadata']['resume_data']`.
    - Does NOT overwrite main state-level user info.
    """

    # Get the file path to the user's uploaded resume
    resume_path = state.get("resume_path", None)

    # Extract text using the unified loader
    if resume_path is not None:
        resume_text = extract_resume_text(resume_path)
    else:
        resume_text = "None"

    # Build the LLM prompt
    resume_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are the ResumeParser Agent for CareerGraph AI.

            Your task:
            - Analyze the provided resume text.
            - Extract the following structured fields:
              • name
              • email
              • phone
              • summary
              • skills
              • education
              • experience
              • certifications
              • projects
              • total_experience_years (approx)
            - If no resume data is found, make the 'is_resume' field False and leave other fields empty.
            - Return output strictly following the structured schema (ResumeModel).
            """
        ),
        ("human", "Resume text:\n{resume_text}")
    ])

    # Chain the prompt to the LLM with structured output
    chain = resume_prompt | llm.with_structured_output(ResumeModel)
    response = chain.invoke({"resume_text": resume_text})

    # Store parsed data in the metadata section of the state
    if state.get("metadata") is None:
        state["metadata"] = {}

    state["metadata"]["resume_data"] = response.model_dump()

    return state
