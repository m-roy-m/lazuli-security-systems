from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
from Modules.login import login_user, register_user
from Modules.database import (
    log_action, get_all_users, delete_user, get_pending_users,
    approve_user, assign_role, get_all_logs, get_logs_by_user,
    get_logs_by_date, get_dashboard_stats
)
import os

print("🔥 APP STARTING 🔥")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")


# ── AUTHENTICATOR DECORATOR 

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("Access denied.", "danger")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return wrapper
    return decorator


#AUTHENTICATION ROUTES

@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = login_user(username, password)
        if user:
            session["user_id"] = user[0]
            session["username"] = user[1]
            session["role"] = user[3]
            role, user_id = user[3], user[0]
            if role == "admin":
                log_action(user_id, "ADMIN_LOGIN")
                return redirect(url_for("admin_home"))
            elif role == "hr":
                log_action(user_id, "HR_LOGIN")
                return redirect(url_for("hr_dashboard"))
            else:
                log_action(user_id, "OFFICER_LOGIN")
                return redirect(url_for("officer_dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials or account not approved.")
    return render_template("login.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    confirm  = request.form.get("confirm_password", "").strip()
    if not username or not password:
        return render_template("login.html", reg_error="Username and password are required.")
    if password != confirm:
        return render_template("login.html", reg_error="Passwords do not match.")
    if register_user(username, password):
        return render_template("login.html", reg_success="Account created! Awaiting admin approval.")
    return render_template("login.html", reg_error="Username already exists.")


@app.route("/logout")
def logout():
    user_id = session.get("user_id")
    if user_id:
        log_action(user_id, "LOGOUT")
    session.clear()
    return redirect(url_for("login"))


#ADMIN ROUTES 
@app.route("/admin")
@login_required("admin")
def admin_home():
    stats = get_dashboard_stats()
    return render_template("admin_dashboard.html", username=session["username"], stats=stats)


@app.route("/admin/users")
@login_required("admin")
def admin_users():
    users = get_all_users()
    log_action(session["user_id"], "VIEW_ALL_USERS")
    return render_template("admin_users.html", username=session["username"], users=users)


@app.route("/admin/users/delete", methods=["POST"])
@login_required("admin")
def admin_delete_user():
    target = request.form.get("username", "").strip()
    if not target:
        flash("No username provided.", "danger")
    elif target == session["username"]:
        flash("You cannot delete your own account.", "danger")
    else:
        delete_user(target)
        log_action(session["user_id"], f"DELETE_USER:{target}")
        flash(f"User '{target}' deleted successfully.", "success")
    return redirect(url_for("admin_users"))


@app.route("/admin/pending")
@login_required("admin")
def admin_pending():
    pending = get_pending_users()
    return render_template("admin_pending.html", username=session["username"], pending=pending)


@app.route("/admin/pending/approve", methods=["POST"])
@login_required("admin")
def admin_approve_user():
    target = request.form.get("username", "").strip()
    if target:
        approve_user(target)
        log_action(session["user_id"], f"APPROVE_USER:{target}")
        flash(f"User '{target}' approved.", "success")
    return redirect(url_for("admin_pending"))


@app.route("/admin/roles")
@login_required("admin")
def admin_roles():
    users = get_all_users()
    return render_template("admin_roles.html", username=session["username"], users=users)


@app.route("/admin/roles/assign", methods=["POST"])
@login_required("admin")
def admin_assign_role():
    target = request.form.get("username", "").strip()
    role   = request.form.get("role", "").strip()
    if target and role:
        assign_role(target, role)
        log_action(session["user_id"], f"ASSIGN_ROLE:{target}:{role}")
        flash(f"Role '{role}' assigned to '{target}'.", "success")
    return redirect(url_for("admin_roles"))


@app.route("/admin/logs")
@login_required("admin")
def admin_logs():
    logs = get_all_logs()
    log_action(session["user_id"], "VIEW_ALL_LOGS")
    return render_template("admin_logs.html", username=session["username"],
                           logs=logs, active_tab="all", page_title="All Logs")


@app.route("/admin/logs/filter")
@login_required("admin")
def admin_logs_filter():
    user_id = request.args.get("user_id", "").strip()
    logs = get_logs_by_user(user_id) if user_id else None
    return render_template("admin_logs.html", username=session["username"],
                           logs=logs, active_tab="filter", page_title="Filter Logs",
                           query_user_id=user_id)


@app.route("/admin/logs/report")
@login_required("admin")
def admin_logs_report():
    date = request.args.get("date", "").strip()
    logs = get_logs_by_date(date) if date else None
    return render_template("admin_logs.html", username=session["username"],
                           logs=logs, active_tab="report", page_title="Log Report",
                           query_date=date)


#HR ROUTE

@app.route("/hr")
@login_required("hr")
def hr_dashboard():
    log_action(session["user_id"], "ACCESS_PAYROLL")
    return render_template("hr_dashboard.html", username=session["username"])


#OFFICER ROUTE

@app.route("/officer")
@login_required()
def officer_dashboard():
    log_action(session["user_id"], "VIEW_LOAN_APPLICATIONS")
    return render_template("officer_dashboard.html", username=session["username"])


if __name__ == "__main__":
    app.run(debug=True)