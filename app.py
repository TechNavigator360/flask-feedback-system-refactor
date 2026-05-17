from flask import Flask, render_template, request, redirect, url_for, session, flash

from src.repositories.csv_repository import load_data, save_data
from src.services.auth_service import authenticate_user
from src.services.user_service import create_user
from src.services.feedback_service import create_feedback, update_feedback_status
from src.middleware.auth_middleware import login_required, coach_required, agent_required

import time

app = Flask(__name__)
app.secret_key = "dev-secret-key"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users, feedback_data, report_data = load_data()

        print(users)

        username = request.form.get("username", "")
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        user = authenticate_user(users, username, password, role)
        

        if not user:
            flash("Invalid credentials.")
            return redirect(url_for("login"))

        session["current_user"] = user

        if user["role"] == "Agent":
            return redirect(url_for("agent_dashboard"))

        if user["role"] == "Coach":
            return redirect(url_for("coach_dashboard"))

        flash("Unknown user role.")
        return redirect(url_for("login"))

    return render_template("login.html")
    

@app.route("/agent")
@agent_required
def agent_dashboard():
    current_user = session.get("current_user")
    
    users, feedback_data, report_data = load_data()

    agent_feedback = [
        feedback for feedback in feedback_data
        if feedback["agent"] == current_user["name"]
    ]

    return render_template(
        "agent_dashboard.html",
        user=current_user,
        feedback_items=agent_feedback
    )


@app.route("/coach")
@coach_required
def coach_dashboard():
    current_user = session.get("current_user")
    
    users, feedback_data, report_data = load_data()

    # Retrieve all users with the Agent role
    agents = [
        user for user in users 
        if user["role"] == "Agent"
    ]

    return render_template(
        "coach_dashboard.html",
        user=current_user, 
        agents=agents, 
        feedback_items=feedback_data
    )


@app.route("/coach/create-account", methods=["POST"])
@coach_required
def create_account():
    users, feedback_data, report_data = load_data()

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    role = request.form.get("role", "")

    success, message, new_user = create_user(users, username, password, role)

    if not success:
        flash(message)
        return redirect(url_for("coach_dashboard"))
    
    save_data(users, feedback_data, report_data)
    flash(message)

    return redirect(url_for("coach_dashboard"))

@app.route("/coach/add-feedback", methods=["POST"])
@coach_required
def add_feedback():
    users, feedback_data, report_data = load_data()

    agent = request.form.get("agent", "")
    feedback_text = request.form.get("feedback_text", "")

    success, message, new_feedback = create_feedback(
        agent, 
        feedback_text,
        time.time()
    )

    if not success:
        flash(message)
        return redirect(url_for("coach_dashboard"))
    
    feedback_data.append(new_feedback)
    save_data(users, feedback_data, report_data)
    flash(message)

    return redirect(url_for("coach_dashboard"))

@app.route("/coach/update-feedback-status/<feedback_id>", methods=["POST"])
@coach_required
def update_feedback_status_route(feedback_id):
    
    users, feedback_data, report_data = load_data()

    new_status = request.form.get("status", "")

    success, message = update_feedback_status(
        feedback_data, 
        feedback_id, 
        new_status
    )

    if success:
        save_data(users, feedback_data, report_data)

    flash(message)
    return redirect(url_for("coach_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)