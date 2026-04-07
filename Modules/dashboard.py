from database import (
    get_all_users, delete_user, get_pending_users, approve_user,
    log_action, assign_role, get_logs_by_date, get_logs_by_user
)


# ─────────────────────────────────────────────
# OFFICER DASHBOARD
# ─────────────────────────────────────────────

def officer_dashboard(user):
    while True:
        print(f"\nWelcome {user[1]}")
        print("1. View client loan Applications")
        print("2. Review client documents")
        print("3. Update application status")
        print("4. Logout")

        choice = input("Choose an option: ")
        user_id = user[0]

        if choice == "1":
            print("Displaying client applications...")
            log_action(user_id, "ACCESS_CLIENT_DATABASE")
        elif choice == "2":
            print("Fetching clients from database...")
            log_action(user_id, "ACCESS_CLIENT_DATABASE")
        elif choice == "3":
            print("Fetching clients from database...")
            log_action(user_id, "ACCESS_CLIENT_DATABASE")
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid option.")


# ─────────────────────────────────────────────
# HR DASHBOARD
# ─────────────────────────────────────────────

def hr_dashboard(user):
    while True:
        print("\n--- HR Dashboard ---")
        print("1. View Payroll")
        print("2. Manage Employees")
        print("3. Logout")

        choice = input("Choose option: ")
        user_id = user[0]

        if choice == "1":
            print("Payroll system (demo)")
            log_action(user_id, "ACCESS_PAYROLL_SYSTEM")
        elif choice == "2":
            print("Employee management (demo)")
            log_action(user_id, "ACCESS_EMPLOYEE_SYSTEM")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid option")


# ─────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────

def admin_dashboard(user):
    admin_id = user[0]
    admin_username = user[1]  # used to prevent self-deletion

    while True:
        print(f"\nWelcome {admin_username} (Admin)")
        print("1. View All Users")
        print("2. Approve pending users")
        print("3. Assign Roles")
        print("4. Logs")
        print("5. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            users = get_all_users()
            print("\n--- All Users ---")
            for u in users:
                print(u)

            action = input("\nType username to delete or press Enter to go back: ").strip()

            if not action:
                # User pressed Enter — go back without doing anything
                continue
            elif action == admin_username:
                # FIX: compare against the actual logged-in admin's username
                print("You cannot delete yourself!")
            else:
                delete_user(action)
                print(f"User '{action}' deleted.")
                log_action(admin_id, f"DELETE_USER:{action}")

        elif choice == "2":
            pending = get_pending_users()

            if not pending:
                print("No pending users.")
                continue  # FIX: was 'return' — that exited the whole dashboard

            print("\n--- Pending Users ---")
            for u in pending:
                print(f"  ID: {u[0]}  Username: {u[1]}")

            username = input("Enter username to approve: ").strip()

            if not username:
                continue

            approve_user(username)
            print(f"User '{username}' approved.")
            log_action(admin_id, f"APPROVE_USER:{username}")

        elif choice == "3":
            role_assignment()
            log_action(admin_id, "ASSIGN_ROLE")

        elif choice == "4":
            logs_menu()

        elif choice == "5":
            print("Logging out...")
            break

        else:
            print("Invalid option.")


# ─────────────────────────────────────────────
# ROLE ASSIGNMENT
# ─────────────────────────────────────────────

def role_assignment():
    username = input("Enter username: ").strip()

    print("Available roles:")
    print("1. Loan Officer")
    print("2. HR")
    print("3. Admin")

    choice = input("Choose role: ")

    if choice == "1":
        role = "officer"
    elif choice == "2":
        role = "hr"
    elif choice == "3":
        role = "admin"
    else:
        print("Invalid role.")
        return

    assign_role(username, role)
    print(f"Role '{role}' assigned to '{username}' successfully.")


# ─────────────────────────────────────────────
# LOGS MENU
# ─────────────────────────────────────────────

def logs_menu():
    while True:
        print("\n--- Logs Menu ---")
        print("1. View Logs (by User ID)")
        print("2. Generate Report (by Date)")
        print("3. Back")

        choice = input("Choose option: ")

        if choice == "1":
            user_id = input("Enter user ID to filter: ").strip()
            logs = get_logs_by_user(user_id)
            if not logs:
                print("No logs found for that user.")
            for log in logs:
                print(log)

        elif choice == "2":
            generate_report()

        elif choice == "3":
            break

        else:
            print("Invalid option")


def generate_report():
    """Print all logs for a given date."""
    date = input("Enter date (YYYY-MM-DD): ").strip()
    logs = get_logs_by_date(date)

    print("\n<<< Log Report >>>")
    if not logs:
        print("No logs found for that date.")
    for log in logs:
        print(log)