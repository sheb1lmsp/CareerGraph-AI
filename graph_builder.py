from langgraph.graph import StateGraph, START, END

# Import all agents and nodes
from agents.router_agent import router
from agents.general_agent import general
from agents.course_recommender_agent import course_recommender
from agents.project_recommender_agent import project_recommender
from agents.interview_coach_agent import interview_coach
from agents.learning_path_advisor_agent import learning_path_advisor
from agents.resume_builder_agent import resume_builder
from agents.skill_analyzer_agent import skill_analyzer
from agents.resume_parser_agent import resume_parser
from agents.job_description_parser_agent import job_description_parser
from agents.get_user_profile_agent import get_user_profile
from state import State 


def build_graph() -> StateGraph:
    """
    Build and compile the full CareerGraph AI workflow using LangGraph.

    This function:
    - Initializes the state graph with the shared `State` class.
    - Adds all agent nodes to the graph.
    - Defines routing and conditional edges for dynamic flow control.
    - Compiles and returns the final executable graph.

    Returns:
        Graph: A compiled LangGraph app instance ready for use.
    """

    # Initialize the graph with the shared state type
    graph = StateGraph(State)

    # Add All Agent Nodes
    graph.add_node("get_user_profile", get_user_profile)       # Fetch or initialize user data
    graph.add_node("router", router)                           # Routes user queries to agents
    graph.add_node("general", general)                         # Handles general/fallback queries
    graph.add_node("course_recommender", course_recommender)   # Suggests learning courses
    graph.add_node("project_recommender", project_recommender) # Recommends projects
    graph.add_node("interview_coach", interview_coach)         # Prepares user for interviews
    graph.add_node("learning_path_advisor", learning_path_advisor) # Suggests learning paths
    graph.add_node("resume_builder", resume_builder)           # Builds or optimizes resumes
    graph.add_node("skill_analyzer", skill_analyzer)           # Analyzes user skills
    graph.add_node("resume_parser", resume_parser)             # Parses resume content
    graph.add_node("job_description_parser", job_description_parser) # Parses job descriptions

    # Define Graph Edges and Logic

    # Entry flow: start from profile setup → router
    graph.add_edge(START, "get_user_profile")
    graph.add_edge("get_user_profile", "router")

    # Conditional routing from router to the appropriate agent
    graph.add_conditional_edges(
        "router",
        lambda state: (
            state["agent_action"]
            if state["agent_action"] not in ["interview_coach", "resume_builder"]
            else "parser"
        ),
        {
            "course_recommender": "course_recommender",
            "project_recommender": "project_recommender",
            "parser": "resume_parser",
            "learning_path_advisor": "learning_path_advisor",
            "skill_analyzer": "skill_analyzer",
            "general": "general",
        },
    )

    # Parser flow: resume → job description → specific agent
    graph.add_edge("resume_parser", "job_description_parser")
    graph.add_conditional_edges(
        "job_description_parser",
        lambda state: state["agent_action"],
        {
            "resume_builder": "resume_builder",
            "interview_coach": "interview_coach",
        },
    )

    # Define Endpoints
    for end_node in [
        "course_recommender",
        "project_recommender",
        "interview_coach",
        "learning_path_advisor",
        "resume_builder",
        "skill_analyzer",
        "general",
    ]:
        graph.add_edge(end_node, END)

    # Compile Final Graph App
    app = graph.compile()

    return app
