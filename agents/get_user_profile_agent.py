from state import State
from utils.get_profile import get_user_profile_from_db

def get_user_profile(state: State) -> State:
    """
    Agent Node: Loads the user profile from the database and updates the shared state.

    This function fetches stored user data (skills, education, experience, etc.)
    and injects it into the active CareerGraph AI state for downstream agents to use.

    Args:
        state (State): The current CareerGraph AI state object.

    Returns:
        State: Updated state containing the user profile data.
    """

    # Fetch user profile data from a database or API (to be implemented)
    profile_data: Dict[str, Any] = get_user_profile_from_db()

    # Update the shared state with profile details
    state["skills"] = profile_data.get("skills", [])
    state["education"] = profile_data.get("education", [])
    state["experience"] = profile_data.get("experience", [])
    state["projects"] = profile_data.get("projects", [])
    state["certifications"] = profile_data.get("certifications", [])

    # Return updated state for downstream use
    return state
