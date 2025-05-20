import tkinter as tk
import re

# Load common passwords from file
with open("passwordList.txt", "r", encoding="utf-8") as f:
    weakPW = set(line.strip() for line in f if line.strip())

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

        # Password label and entry (with show/hide button)
        self.password_label = tk.Label(self.frame, text="Password:", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 12))
        self.password_label.pack(pady=(30, 8))
        #makes the password entry field be able to have two things next to eachother
        pw_entry_frame = tk.Frame(self.frame, bg="#2d323b")
        pw_entry_frame.pack(pady=8)
        self.password_entry = tk.Entry(pw_entry_frame, font=("Segoe UI", 12), show="*")
        self.password_entry.pack(side="left", ipadx=10, ipady=4)
        self.show_password = False
        #adds a button to the right of the password entry field
        self.toggle_btn = tk.Button(pw_entry_frame, text="Show", command=self.toggle_password, font=("Segoe UI", 10), bg="#bdbdbd", fg="#23272f", relief="flat", padx=8)
        self.toggle_btn.pack(side="left", padx=(8,0))

        # Check button
        self.check_button = tk.Button(self.frame, text="Check Strength", bg="#81c784", fg="#23272f", font=("Segoe UI", 11, "bold"), command=self.check_password_strength, activebackground="#66bb6a")
        self.check_button.pack(pady=18, ipadx=8, ipady=2)

        # Feedback labels
        self.strength_label = tk.Label(
            self.frame,
            text="",
            bg="#2d323b",
            fg="#f5f5f5",
            font=("Segoe UI", 12),
            justify="left",
            anchor="s",
            wraplength=400
        )
        self.strength_label.pack(pady=2, fill="x")
        self.issues_label = tk.Label(
            self.frame,
            text="",
            bg="#2d323b",
            fg="#f5f5f5",
            font=("Segoe UI", 10),
            justify="left",
            anchor="s",
            wraplength=400
        )
        self.issues_label.pack(pady=1, fill="x")
        self.cracktime_label = tk.Label(
            self.frame,
            bg="#2d323b",
            fg="#b39ddb",
            font=("Segoe UI", 10),
            wraplength=400,
            anchor="s",
            justify="left"
        )
        self.cracktime_label.pack(pady=2, fill="x")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="Show")

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
        if password == "Byenj@m1n":
            issues.append("Password is a basic ass bitch")
        if password in weakPW:
            issues.append("Youza Basic Bitch")

        # shows password strength depending on the number of issues
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
            feedback = f"{strength}:"  # Only strength in this label
            self.strength_label.config(text=feedback, fg=colour)
            # Show issues in a separate label below
            issues_text = "\n- " + "\n- ".join(issues)
            self.issues_label.config(text=issues_text, fg=colour)
        else:
            self.strength_label.config(text="Strong Password", fg="#81c784")
            self.issues_label.config(text="")

        crack_time = self.estimate_crack_time(password)
        cracking = f"Estimated time to crack: {crack_time}"
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
