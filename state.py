# Import typing utilities for structured data representation
from typing import TypedDict, Literal, List, Dict, Optional, Any

# Define a schema for user projects
class Project(TypedDict):
    name: str
    start_date: str
    end_date: str
    description: str

# Define a schema for certifications
class Certification(TypedDict):
    name: str
    organization: str

# Define a schema for education details
class Education(TypedDict):
    degree: str
    university: str
    start_date: str
    end_date: str
    cgpa: float

# Define a schema for professional experience
class Experience(TypedDict):
    title: str
    employment_type: str
    company: str
    start_date: str
    end_date: str
    location: str
    description: str

# Define the central state structure used by agents
class State(TypedDict):
    # User input text or query
    input_text: str

    # Indicates which agent should handle the request
    agent_action: Optional[
        Literal[
            "course_recommender",
            "project_recommender",
            "interview_coach",
            "learning_path_advisor",
            "resume_builder",
            "skill_analyzer",
        ]
    ]

    # Structured user information
    skills: Optional[List[str]]
    certifications: Optional[List[Certification]]
    projects: Optional[List[Project]]
    education: Optional[List[Education]]
    experience: Optional[List[Experience]]

    # Memory summary for conversation continuity
    memory_summary: Optional[str]

    # Model-generated response text
    response: Optional[str]

    # Additional metadata or runtime information
    metadata: Optional[Dict]

    # File path to generated resume (if applicable)
    resume_path: Optional[str]
