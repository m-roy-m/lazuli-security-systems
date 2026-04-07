from login import login_user, register   # 'register' now exists in login.py
from dashboard import hr_dashboard, officer_dashboard, admin_dashboard
from database import log_action


def main():
    while True:
        print("\n=== Lazuli Ltd. Security Systems ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            register()  # interactive prompt defined inside login.py

        elif choice == "2":
            # FIX: collect credentials here before passing to login_user
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            user = login_user(username, password)

            if user:
                role = user[3]      # role column
                user_id = user[0]   # id column

                if role == "admin":
                    admin_dashboard(user)
                    log_action(user_id, "ACCESS_ADMIN_DASHBOARD")   # FIX: was log_action(user, ...)
                elif role == "hr":
                    hr_dashboard(user)
                    log_action(user_id, "ACCESS_HR_DASHBOARD")
                else:
                    officer_dashboard(user)
                    log_action(user_id, "ACCESS_OFFICER_DASHBOARD")
            else:
                print("Login failed. Please check your credentials or contact an admin.")

        elif choice == "3":
            print("Exiting system...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()