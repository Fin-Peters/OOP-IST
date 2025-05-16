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
            colour = "red"
        elif len(issues) == 3:
            strength = "Weak"
            colour = "orange"
        elif len(issues) == 2:
            strength = "Moderate"
            colour = "gold"
        elif len(issues) == 1:
            strength = "Good"
            colour = "cyan"
        feedback = f"{strength}:\n- " + "\n- ".join(issues)
        strength_label.config(text=feedback, fg=colour)

    else:
        strength_label.config(text="Strong Password", fg="green")
    crack_time = estimate_crack_time(password)
    cracking = f"\nEstimated time to crack: {crack_time}"
    cracktime_label.config(text=cracking, fg= "purple")

def estimate_crack_time(password):
    # Estimate character set size
    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[~`!@#$%^&*()-_=+{};:\|',.<>/?]", password):
        charset += 32  # Approximate number of special chars

    if charset == 0:
        return "Instantly"

    guesses = charset ** len(password)
    guesses_per_second = 1e9  # 1 billion guesses per second
    seconds = guesses / guesses_per_second

    # Convert seconds to human-readable time
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2f} years"

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

# Add a label to display estimated crack time
cracktime_label = tk.Label(app, text="", bg="#2E2E2E", fg="white")
cracktime_label.pack(pady=5)
# Run the application
app.mainloop()
