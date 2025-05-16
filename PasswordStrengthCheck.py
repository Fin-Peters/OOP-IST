import tkinter as tk
import re

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.configure(bg="#23272f")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Main frame for content
        self.frame = tk.Frame(root, bg="#2d323b", bd=2, relief="groove")
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Password label and entry
        self.password_label = tk.Label(self.frame, text="Password:", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 12))
        self.password_label.pack(pady=(30, 8))
        self.password_entry = tk.Entry(self.frame, font=("Segoe UI", 12), show="*")
        self.password_entry.pack(pady=8, ipadx=10, ipady=4)

        # Check button
        self.check_button = tk.Button(self.frame, text="Check Strength", bg="#81c784", fg="#23272f", font=("Segoe UI", 11, "bold"), command=self.check_password_strength, activebackground="#66bb6a")
        self.check_button.pack(pady=18, ipadx=8, ipady=2)

        # Feedback labels
        self.strength_label = tk.Label(self.frame, text="", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 11), justify="left")
        self.strength_label.pack(pady=5)
        self.cracktime_label = tk.Label(self.frame, bg="#2d323b", fg="#b39ddb", font=("Segoe UI", 10))
        self.cracktime_label.pack(pady=5)

    def check_password_strength(self):
        issues = []
        password = self.password_entry.get()

        if len(password) == 0:
            self.strength_label.config(text="Password cannot be empty", fg="#e57373")
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

        # Softer color palette
        if issues:
            if len(issues) >= 4:
                strength = "Very Weak"
                colour = "#e57373"
            elif len(issues) == 3:
                strength = "Weak"
                colour = "#ffb74d"
            elif len(issues) == 2:
                strength = "Moderate"
                colour = "#fff176"
            elif len(issues) == 1:
                strength = "Good"
                colour = "#64b5f6"
            feedback = f"{strength}:\n- " + "\n- ".join(issues)
            self.strength_label.config(text=feedback, fg=colour)
        else:
            self.strength_label.config(text="Strong Password", fg="#81c784")

        crack_time = self.estimate_crack_time(password)
        cracking = f"\nEstimated time to crack: {crack_time}"
        self.cracktime_label.config(text=cracking, fg="#b39ddb")

    def estimate_crack_time(self, password):
        charset = 0
        if re.search(r"[a-z]", password):
            charset += 26
        if re.search(r"[A-Z]", password):
            charset += 26
        if re.search(r"[0-9]", password):
            charset += 10
        if re.search(r"[~`!@#$%^&*()-_=+{};:\\|',.<>/?]", password):
            charset += 32  

        if charset == 0:
            return "Instantly"

        guesses = charset ** len(password)
        guesses_per_second = 1e9  # 1 billion guesses per second
        seconds = guesses / guesses_per_second

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
