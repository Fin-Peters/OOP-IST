import tkinter as tk
import re

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.configure(bg="#2E2E2E")
        self.root.geometry("550x550")
        self.root.resizable(True, True)

        # Password label and entry
        self.password_label = tk.Label(root, text="Password:", bg="#2E2E2E", fg="white")
        self.password_label.pack(pady=8)
        self.password_entry = tk.Entry(root)
        self.password_entry.pack(pady=8)

        # Check button
        self.check_button = tk.Button(root, text="Check Strength", bg="#4CAF50", fg="white", command=self.check_password_strength)
        self.check_button.pack(pady=10)

        # Feedback labels
        self.strength_label = tk.Label(root, text="", bg="#2E2E2E", fg="white")
        self.strength_label.pack(pady=5)
        self.cracktime_label = tk.Label(root, bg="black", fg="white")
        self.cracktime_label.pack(pady=5)

    def check_password_strength(self):
        issues = []
        password = self.password_entry.get()

        if len(password) == 0:
            self.strength_label.config(text="Password cannot be empty", fg="red")
            self.cracktime_label.config(text="")
            return
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
            self.strength_label.config(text=feedback, fg=colour)
        else:
            self.strength_label.config(text="Strong Password", fg="green")

        crack_time = self.estimate_crack_time(password)
        cracking = f"\nEstimated time to crack: {crack_time}"
        self.cracktime_label.config(text=cracking, fg="purple")

    def estimate_crack_time(self, password):
        charset = 0
        if re.search(r"[a-z]", password):
            charset += 26
        if re.search(r"[A-Z]", password):
            charset += 26
        if re.search(r"[0-9]", password):
            charset += 10
        if re.search(r"[~`!@#$%^&*()-_=+{};:\\|',.<>/?]", password):
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

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    root.mainloop()
