import tkinter as tk
import re

# Function to check password strength
def check_password_strength():
    issues = []
    password = password_entry.get()
    if len(password) < 6:
        issues.append("Too short (minimum 6 characters)")
    if not re.search(r"[A-Z]", password):
        issues.append("Add an uppercase letter")
    if not re.search(r"[a-z]", password):
        issues.append("Add a lowercase letter")
    if not re.search(r"[0-9]", password):
        issues.append("Add a number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        issues.append("Add a special character")

    if issues:
        if len(issues) >= 4:
            strength = "Very Weak"
            color = "red"
        elif len(issues) == 3:
            strength = "Weak"
            color = "orange"
        elif len(issues) == 2:
            strength = "Moderate"
            color = "gold"
        elif len(issues) == 1:
            strength = "Good"
            color = "blue"
        feedback = f"{strength}:\n- " + "\n- ".join(issues)
        strength_label.config(text=feedback, fg=color)
    else:
        strength_label.config(text="Strong Password", fg="green")

# Create the main application window
app = tk.Tk()
app.title("Password Strength Checker")
app.configure(bg="#2E2E2E")
app.geometry("550x650")
app.resizable(True, True)

#

# Add a label for the password
password_label = tk.Label(app, text="Password:", bg="#2E2E2E", fg="white")
password_label.pack(pady=8)

# Add an entry field for the password
password_entry = tk.Entry(app)
password_entry.pack(pady=8)

# Add a button to check password strength
check_button = tk.Button(app, text="Check Strength", bg="#4CAF50", fg="white", command=check_password_strength)
check_button.pack(pady=10)

# Add a label to display password strength
strength_label = tk.Label(app, text="", bg="#2E2E2E", fg="white")
strength_label.pack(pady=5)

# Run the application
app.mainloop()
