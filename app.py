from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db, User, Education, Certification, Project, Skill, Experience
from utils.get_profile import get_user_profile_from_db
from config import SECRET_KEY
from conversation_manager import manager

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)
bcrypt = Bcrypt(app)
CORS(app)
app.secret_key = SECRET_KEY

with app.app_context():
    db.create_all()

def format_month_year(date_str: str) -> str:
    """Convert 'YYYY-MM' into 'Month YYYY' (e.g. 2024-03 → March 2024)"""
    try:
        return datetime.strptime(date_str, "%Y-%m").strftime("%B %Y")
    except Exception:
        return ""

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("profile_page"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = bcrypt.generate_password_hash(request.form.get("password")).decode("utf-8")

        if User.query.filter_by(email=email).first():
            flash("⚠️ Email already registered", "error")
            return render_template("register.html")

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("✅ Registered successfully. Please log in.", "success")
        return redirect(url_for("login_page"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect(url_for("profile_page"))
        flash("❌ Invalid credentials", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/profile")
def profile_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    profile = get_user_profile_from_db(session["user_id"])
    return render_template("profile.html", profile=profile)

@app.route("/profile/add", methods=["GET", "POST"])
def add_profile_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    if request.method == "POST":
        section = request.form.get("section")
        user_id = session["user_id"]

        # ---------- Education ----------
        if section == "education":
            degree = request.form.get("degree")
            university = request.form.get("university")
            edu_start = format_month_year(request.form.get("edu_start"))
            edu_end = format_month_year(request.form.get("edu_end"))

            existing = Education.query.filter_by(
                user_id=user_id, degree=degree, university=university
            ).first()
            if existing:
                flash("⚠️ This education record already exists.", "error")
            else:
                db.session.add(Education(
                    user_id=user_id,
                    degree=degree,
                    university=university,
                    start_date=edu_start,
                    end_date=edu_end,
                    cgpa=request.form.get("cgpa")
                ))
                db.session.commit()
                flash("✅ Education added successfully!", "success")

        # ---------- Certification ----------
        elif section == "certification":
            name = request.form.get("cert_name")
            org = request.form.get("cert_org")
            existing = Certification.query.filter_by(user_id=user_id, name=name, organization=org).first()
            if existing:
                flash("⚠️ This certification already exists.", "error")
            else:
                db.session.add(Certification(user_id=user_id, name=name, organization=org))
                db.session.commit()
                flash("✅ Certification added!", "success")

        # ---------- Project ----------
        elif section == "project":
            name = request.form.get("proj_name")
            proj_start = format_month_year(request.form.get("proj_start"))
            proj_end = format_month_year(request.form.get("proj_end"))
            existing = Project.query.filter_by(user_id=user_id, name=name).first()
            if existing:
                flash("⚠️ This project already exists.", "error")
            else:
                db.session.add(Project(
                    user_id=user_id,
                    name=name,
                    start_date=proj_start,
                    end_date=proj_end,
                    description=request.form.get("proj_desc")
                ))
                db.session.commit()
                flash("✅ Project added!", "success")

        # ---------- Experience ----------
        elif section == "experience":
            title = request.form.get("exp_title")
            company = request.form.get("exp_company")
            exp_start = format_month_year(request.form.get("exp_start"))
            exp_end = format_month_year(request.form.get("exp_end"))
            existing = Experience.query.filter_by(
                user_id=user_id, title=title, company=company
            ).first()
            if existing:
                flash("⚠️ This experience already exists.", "error")
            else:
                db.session.add(Experience(
                    user_id=user_id,
                    title=title,
                    company=company,
                    start_date=exp_start,
                    end_date=exp_end,
                    location=request.form.get("exp_location"),
                    description=request.form.get("exp_desc")
                ))
                db.session.commit()
                flash("✅ Experience added!", "success")

        # ---------- Skills ----------
        elif section == "skills":
            skills = [s.strip() for s in request.form.get("skills").split(",")]
            added = []
            for s in skills:
                if not Skill.query.filter_by(user_id=user_id, name=s).first():
                    db.session.add(Skill(user_id=user_id, name=s))
                    added.append(s)
            if added:
                db.session.commit()
                flash(f"✅ Added new skills: {', '.join(added)}", "success")
            else:
                flash("⚠️ All entered skills already exist.", "error")

        return redirect(url_for("add_profile_page"))

    return render_template("add_profile.html")

@app.route("/chat", methods=["GET", "POST"])
def chat_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    # Initialize chat history in session
    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":

        memory = []
        for i in session["chat_history"][-10:]:
            memory.append(f"{i['sender']} : {i['text']}")
        user_message = request.form.get("message", "").strip()

        response = manager(user_message, memory, session["user_id"])

        if user_message:
            # Append user message
            session["chat_history"].append({"sender": "user", "text": user_message})
            
            session["chat_history"].append({"sender": "bot", "text": response})
            session.modified = True  # Important for session updates

    return render_template("chat.html", chat_history=session["chat_history"])
    
if __name__ == "__main__":
    app.run(debug=True)
