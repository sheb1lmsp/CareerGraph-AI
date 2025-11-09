from models import db, User, Education, Certification, Project, Skill, Experience

def get_user_profile_from_db(user_id: int) -> dict:
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}

    return {
        "user": {"id": user.id, "name": user.name, "email": user.email},
        "education": [
            {"degree": e.degree, "university": e.university,
             "start_date": e.start_date, "end_date": e.end_date, "cgpa": e.cgpa}
            for e in Education.query.filter_by(user_id=user_id).all()
        ],
        "certifications": [
            {"name": c.name, "organization": c.organization}
            for c in Certification.query.filter_by(user_id=user_id).all()
        ],
        "projects": [
            {"name": p.name, "start_date": p.start_date, "end_date": p.end_date, "description": p.description}
            for p in Project.query.filter_by(user_id=user_id).all()
        ],
        "experience": [
            {"title": e.title, "company": e.company, "start_date": e.start_date,
             "end_date": e.end_date, "location": e.location, "description": e.description}
            for e in Experience.query.filter_by(user_id=user_id).all()
        ],
        "skills": [s.name for s in Skill.query.filter_by(user_id=user_id).all()]
    }
