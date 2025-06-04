import tkinter as tk
import webbrowser 
import re
import random
import string

# Load common passwords from file
with open("passwordList.txt", "r", encoding="utf-8") as f:
    weakPW = set(line.strip() for line in f if line.strip())

class PasswordStrengthChecker:

    def check_strength(self, password):
        issues = []
        if password == "fong":
            webbrowser.open("https://cornhub.website")
            return "Welcome Back", ["opening most used webpage"]
        if re.search(r"[ ]", password):
            return "Other", ["Password cannot contain spaces"]
        if password == "Byenj@m1n":
            return"Spesch", ["Password is a basic ass bitch"]
        if len(password) == 0:
            return "Other", ["Password cannot be empty"]
        if password in weakPW:
            return "Other", ["Password is not secure, too common"]
        if len(password) < 6:
            issues.append("Too short (minimum 6 characters)")
        if re.search(r"[(),.?\:{}|<>]", password):
            return "Other", ["Password cannot contain special characters like (),.?\":{}|<>"]
        if not re.search(r"[A-Z]", password):
            issues.append("Add an uppercase letter")
        if not re.search(r"[a-z]", password):
            issues.append("Add a lowercase letter")
        if not re.search(r"[0-9]", password):
            issues.append("Add a number")
        if not re.search(r"[!@#$%^&*]", password):
            issues.append("Add a special character")
        

        if issues:
            if len(issues) >= 4:
                strength = "Very Weak"
            elif len(issues) == 3:
                strength = "Weak"
            elif len(issues) == 2:
                strength = "Moderate"
            elif len(issues) == 1:
                strength = "Good"
        else:
            strength = "Strong Password"
        return strength, issues

    def estimate_crack_time(self, password):
        charset = 0
        if re.search(r"[a-z]", password):
            charset += 26
        if re.search(r"[A-Z]", password):
            charset += 26
        if re.search(r"[0-9]", password):
            charset += 10
        if re.search(r"[~`!@#$%^&*]", password):
            charset += 10 
        if charset == 0:
            return "Instantly"
        guesses = charset ** len(password)
        guesses_per_second = 1e9
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

class PasswordStrengthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Strength Checker")
        self.root.configure(bg="#23272f")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.checker = PasswordStrengthChecker()
        self.dev_window = None  
        self.setup_ui()
        self.setup_easter_egg()

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#2d323b", bd=2, relief="groove")
        self.frame.pack(padx=30, pady=30, fill="both", expand=True)
        self.setup_password_entry()
        self.setup_feedback_labels()
        self.setup_dev_button()
    
    def setup_password_entry(self):
        self.password_label = tk.Label(self.frame, text="Password:", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 12))
        self.password_label.pack(pady=(30, 8))
        pw_entry_frame = tk.Frame(self.frame, bg="#2d323b")
        pw_entry_frame.pack(pady=8)
        self.password_entry = tk.Entry(pw_entry_frame, font=("Segoe UI", 12), show="*")
        self.password_entry.pack(side="left", ipadx=10, ipady=4)
        self.show_password = False
        self.toggle_btn = tk.Button(pw_entry_frame, text="Show", command=self.toggle_password, font=("Segoe UI", 10), bg="#bdbdbd", fg="#23272f", relief="flat", padx=8)
        self.toggle_btn.pack(side="left", padx=(8,0))
        # Add Spinbox for password length
        self.length_label = tk.Label(pw_entry_frame, text="Length:", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 10))
        self.length_label.pack(side="left", padx=(12,0))
        self.length_var = tk.IntVar(value=12)
        self.length_spinbox = tk.Spinbox(pw_entry_frame, from_=8, to=32, width=3, textvariable=self.length_var, font=("Segoe UI", 10))
        self.length_spinbox.pack(side="left", padx=(2,0))
        # Place Check, Copy, and Generate buttons side by side
        button_frame = tk.Frame(self.frame, bg="#2d323b")
        button_frame.pack(pady=10)
        self.check_button = tk.Button(button_frame, text="Check Strength", bg="#81c784", fg="#23272f", font=("Segoe UI", 11, "bold"), command=self.check_password_strength, activebackground="#66bb6a")
        self.check_button.pack(side="left", ipadx=8, ipady=2, padx=(0, 8))
        self.copy_password_button = tk.Button(button_frame, text="Copy Password", bg="#64b5f6", fg="#23272f", font=("Segoe UI", 11, "bold"), command=self.copy_password, activebackground="#42a5f5")
        self.copy_password_button.pack(side="left", ipadx=8, ipady=2, padx=(0, 8))
        self.generate_password_button = tk.Button(button_frame, text="Generate Password", bg="#ffd54f", fg="#23272f", font=("Segoe UI", 11, "bold"), command=self.fill_generated_password, activebackground="#ffb300")
        self.generate_password_button.pack(side="left", ipadx=8, ipady=2)
        
    def setup_feedback_labels(self):
        self.strength_label = tk.Label(self.frame, text="", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 12), justify="left", anchor="s", wraplength=400)
        self.strength_label.pack(pady=(0,0), fill="x")
        self.issues_label = tk.Label(self.frame, text="", bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 10), justify="left", anchor="s", wraplength=400)
        self.issues_label.pack(pady=(0,0), fill="x")
        self.cracktime_label = tk.Label(self.frame, bg="#2d323b", fg="#b39ddb", font=("Segoe UI", 10), wraplength=400, anchor="s", justify="left")
        self.cracktime_label.pack(pady=1, fill="x")

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="Show")

    def check_password_strength(self):
        password = self.password_entry.get()
        
        strength, issues = self.checker.check_strength(password)
        # Colour logic
        colour_map = {
            "Very Weak": "#e57373",
            "Weak": "#ffb74d",
            "Moderate": "#fff176",
            "Good": "#64b5f6",
            "Strong Password": "#81c784",
            "Spesch": "#aa6ff7",
            "Other": "#e57373",
            "Welcome Back": "#81c784"
        }
        colour = colour_map.get(strength, "#f5f5f5")
        self.strength_label.config(text=f"{strength}:", fg=colour)
        if issues and strength != "Strong Password":
            issues_text = "\n- " + "\n- ".join(issues)
            self.issues_label.config(text=issues_text, fg=colour)
        else:
            self.issues_label.config(text="")
        crack_time = self.checker.estimate_crack_time(password)
        cracking = f"Estimated time to crack: {crack_time}"
        self.cracktime_label.config(text=cracking, fg="#b39ddb")

    def copy_password(self):
        password = self.password_entry.get()
        root.clipboard_clear()
        root.clipboard_append(password)

    def open_dev_page(self):
        if self.dev_window is not None and tk.Toplevel.winfo_exists(self.dev_window):
            self.dev_window.lift()  # Bring to front if already open
            return
        self.dev_window = tk.Toplevel(self.root)
        self.dev_window.title("Developer Page")
        self.dev_window.geometry("300x400")
        self.dev_window.resizable(False, False)
        self.dev_window.configure(bg="#23272f")
        label = tk.Label(self.dev_window, text="Developer Page", bg="#23272f", fg="#f5f5f5", font=("Segoe UI", 14))
        label.pack(pady=20)
        body_text = tk.Text(self.dev_window, bg="#2d323b", fg="#f5f5f5", font=("Segoe UI", 10), wrap="word", padx=10, pady=10)
        body_text.insert(tk.END, "Made by Bitrealm Studios \n\n" 
        "Thank you for using the Password Strength Checker!" 
        "\n\n Made with hatred for Tkinter XOXO.")
        body_text.config(state="disabled")
        body_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.dev_window.protocol("WM_DELETE_WINDOW", self.close_dev_window)

    def close_dev_window(self):
        if self.dev_window is not None:
            self.dev_window.destroy()
            self.dev_window = None

    def setup_dev_button(self):
        self.dev_button = tk.Button(self.root, text="Dev Page", command=self.open_dev_page, bg="#bdbdbd", fg="#23272f", font=("Segoe UI", 9), relief="flat")
        self.dev_button.place(x=10, y=self.root.winfo_height()-40, anchor="sw")
        self.root.after(100, self.update_dev_button_position)

    def update_dev_button_position(self):
        self.dev_button.place(x=10, y=self.root.winfo_height()-10, anchor="sw")
        self.root.after(100, self.update_dev_button_position)

    def generate_strong_password(self, length):
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        while True:
            password = ''.join(random.choice(chars) for _ in range(length))
            # Ensure at least one of each type
            if (any(c.islower() for c in password) and
                any(c.isupper() for c in password) and
                any(c.isdigit() for c in password) and
                any(c in '!@#$%^&*' for c in password)):
                return password

    def fill_generated_password(self):
        length = self.length_var.get()
        password = self.generate_strong_password(length)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def setup_easter_egg(self):
        self.root.bind("<Control-q>", self.easter_egg)

    def easter_egg(self, event=None):
        # Trigger the easter egg functionality\
        webbrowser.open("https://cornhub.website")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthApp(root)
    root.mainloop()