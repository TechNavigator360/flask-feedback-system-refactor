from flask import Flask, render_template, request, redirect, url_for, session, flash

from src.repositories.csv_repository import load_data, save_data
from src.services.auth_service import authenticate_user
from src.services.user_service import create_user
from src.services.feedback_service import create_feedback

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

        print("INPUT:", username, password, role)
        print("MATCHES:", [
            u for u in users if u["name"] == username
        ])


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
def agent_dashboard():
    current_user = session.get("current_user")

    if not current_user:
        return redirect(url_for("login"))
    
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
def coach_dashboard():
    current_user = session.get("current_user")

    if not current_user:
        return redirect(url_for("login"))
    
    users, feedback_data, report_data = load_data()
    agents = [user for user in users if user["role"] == "Agent"]

    return render_template(
        "coach_dashboard.html",
        user=current_user, 
        agents=agents, 
        feedback_items=feedback_data
    )


@app.route("/coach/create-account", methods=["POST"])
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
def add_feedback():
    users, feedback_data, report_data = load_data()

    agent = request.form.get("agent", "")
    feedback_text = request.form.get("feedback_get", "")

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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)