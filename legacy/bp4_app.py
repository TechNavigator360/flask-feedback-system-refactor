#!/usr/bin/env python
# coding: utf-8

# Required Imports:
# tkinter: Used for building the graphical user interface (GUI).
import tkinter as tk # `tk`: Provides core GUI components (e.g., windows, labels, buttons).
from tkinter import messagebox # `messagebox`: Displays pop-up dialogs for errors, warnings, and information.
import csv # csv: Handles reading from and writing to CSV files.
import logging # logging: Enables logging of warnings and errors for debugging and monitoring.
import time # time: Provides utilities for working with timestamps and delays.
from datetime import datetime # `datetime`: Used specifically for parsing, formatting, and comparing dates and times.
from src.ui.styles import *
from src.repositories.csv_repository import load_data, save_data
from src.services.auth_service import authenticate_user
from src.services.user_service import create_user
from src.services.feedback_service import create_feedback

# Configure logging for clear, minimal warnings
logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(message)s')

class App(tk.Tk):

    """
    The main application class that manages the entire GUI and navigation between screens.

    - Initializes the application window, loads data, and sets up the ReportGenerator.
    - Manages multiple screens (Login, Agent, Coach, Profile, Feedback) using a frame container.
    - Methods:
        - show_frame(): Displays the specified screen and resets fields or data where necessary.
    """

    def __init__(self):
        super().__init__()
        self.title("Agent and Coach App")
        self.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")
        self.configure(bg=BACKGROUND_COLOR)

        # Initialize current_user as None
        self.current_user = None

        # Load data once and store it in attributes
        self.users, self.feedback_data, self.report_data = load_data() #should become an application state/service layer.

        # Create a ReportGenerator instance with the loaded feedback data
        self.report_generator = ReportGenerator(self.feedback_data) #should become an application state/service layer.

        # Container frame to hold all screens
        container = tk.Frame(self, bg=BACKGROUND_COLOR)
        container.pack(fill="both", expand=True)

        # Configure grid weights for centering
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary to store frames
        self.frames = {}

        # Add each screen frame to the dictionary
        for F in (LoginScreen, AgentMainMenu, CoachMainMenu, ProfileSettings, ViewFeedback, AgentViewFeedback):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start with the login screen after frames are fully initialized
        self.show_frame(LoginScreen)

    def show_frame(self, frame_class):
        """Bring the specified frame to the front of the GUI."""
        frame = self.frames[frame_class]

        # Clear fields when showing the login screen
        if frame_class == LoginScreen:
            frame.clear_fields()

        # Clear password fields when showing profile settings
        elif frame_class == ProfileSettings:
            frame.clear_password_fields()

        # Check if we're showing AgentViewFeedback and refresh feedback on login
        if frame_class == AgentViewFeedback:
            frame.refresh_feedback_on_login()

        # Reset fields or data for specific screens
        if frame_class == ViewFeedback:
            frame.reset_view()  # Reset the ViewFeedback screen

        frame.tkraise()

class LoginScreen(tk.Frame):

    """
    A Tkinter frame for user login, allowing agents and coaches to access their respective menus.

    - Features input fields for username, password, and role selection.
    - Validates user credentials and navigates to the appropriate main menu upon successful login.
    - Methods:
        - login(): Authenticates the user and redirects to the respective main menu based on role.
        - clear_fields(): Clears the username and password fields.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)

        # Configure grid layout for center alignment
        self.grid_rowconfigure(0, weight=1)  # Space above content
        self.grid_rowconfigure(9, weight=1)  # Space below content
        self.grid_columnconfigure(0, weight=1)  # Space to the left
        self.grid_columnconfigure(3, weight=1)  # Space to the right

        # Title Label - centered
        title_label = tk.Label(self, text="Login Screen")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Role selection - aligned side by side
        role_label = tk.Label(self, text="Role")
        apply_label_style(role_label)
        role_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        self.role = tk.StringVar(value="Agent")
        role_menu = tk.OptionMenu(self, self.role, "Agent", "Coach")
        role_menu.configure(font=FONT_MAIN, bg="white")
        role_menu.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Username field - side by side alignment
        username_label = tk.Label(self, text="Username")
        apply_label_style(username_label)
        username_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        self.username_entry = tk.Entry(self)
        apply_entry_style(self.username_entry)
        self.username_entry.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Password field - side by side alignment
        password_label = tk.Label(self, text="Password")
        apply_label_style(password_label)
        password_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        self.password_entry = tk.Entry(self, show="*")
        apply_entry_style(self.password_entry)
        self.password_entry.grid(row=3, column=2, sticky="w", padx=10, pady=5)

        # Login button - centered
        login_button = tk.Button(self, text="Login", command=self.login)
        apply_button_style(login_button)
        add_hover_effect(login_button)
        login_button.configure(width=get_button_width())
        login_button.grid(row=4, column=0, columnspan=4, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role = self.role.get()

        # Search for the user in the list
        user_found = authenticate_user(
            self.controller.users,
            username,
            password,
            role
        )

        # Validate the found user
        if user_found:
            # Set current_user to the full user dictionary upon successful login
            self.controller.current_user = user_found
            if role == "Agent":
                self.controller.show_frame(AgentMainMenu)
            elif role == "Coach":
                self.controller.show_frame(CoachMainMenu)
        else:
            messagebox.showerror("Login Error", "Username not found or incorrect credentials.")

    def clear_fields(self):
        """Clear the username and password fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

class AgentMainMenu(tk.Frame):

    """
    A Tkinter frame for the agent's main menu, providing navigation to key functionalities.

    - Features buttons for managing profiles, viewing feedback, and logging out.
    - Methods:
        - logout(): Clears the current user and navigates back to the login screen.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)

        # Configure grid layout for center alignment
        self.grid_rowconfigure(0, weight=1)  # Space above content
        self.grid_rowconfigure(6, weight=1)  # Space below content
        self.grid_columnconfigure(0, weight=1)  # Space left of content
        self.grid_columnconfigure(2, weight=1)  # Space right of content

        # Title Label
        title_label = tk.Label(self, text="Agent Main Menu")
        apply_label_style(title_label, title=True)
        title_label.grid(row=1, column=1, pady=(20, 10), sticky="n")

        # Profile Button
        profile_button = tk.Button(
            self,
            text="Profile",
            command=lambda: controller.show_frame(ProfileSettings),
        )
        apply_button_style(profile_button)
        add_hover_effect(profile_button)
        profile_button.configure(width=get_button_width())
        profile_button.grid(row=2, column=1, pady=10)

        # View Feedback Button
        view_feedback_button = tk.Button(
            self,
            text="View Feedback",
            command=lambda: controller.show_frame(AgentViewFeedback),
        )
        apply_button_style(view_feedback_button)
        add_hover_effect(view_feedback_button)
        view_feedback_button.configure(width=get_button_width())
        view_feedback_button.grid(row=3, column=1, pady=10)

        # Logout Button
        logout_button = tk.Button(self, text="Logout", command=self.logout)
        apply_button_style(logout_button)
        add_hover_effect(logout_button)
        logout_button.configure(width=get_button_width())
        logout_button.grid(row=4, column=1, pady=10)

    def logout(self):
        """Clear the current user and go back to the login screen."""
        self.controller.current_user = None  # Reset current_user
        self.controller.show_frame(LoginScreen)

class CoachMainMenu(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.report_generator = self.controller.report_generator  # Store the ReportGenerator instance
        self.configure(bg=BACKGROUND_COLOR)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Title Label
        title_label = tk.Label(self, text="Coach Main Menu")
        apply_label_style(title_label, title=True)
        title_label.grid(row=1, column=1, pady=10)

        # Profile Button
        profile_button = tk.Button(
            self,
            text="View Profile",
            command=lambda: controller.show_frame(ProfileSettings)
        )
        apply_button_style(profile_button)
        add_hover_effect(profile_button)
        profile_button.configure(width=get_button_width())
        profile_button.grid(row=2, column=1, pady=10)

        # Create Account Button
        create_account_button = tk.Button(
            self,
            text="Create Account",
            command=self.open_create_account_form
        )
        apply_button_style(create_account_button)
        add_hover_effect(create_account_button)
        create_account_button.configure(width=get_button_width())
        create_account_button.grid(row=3, column=1, pady=10)

        # Update Feedback Button
        update_feedback_button = tk.Button(
            self,
            text="Update Feedback",
            command=lambda: controller.show_frame(ViewFeedback)
        )
        apply_button_style(update_feedback_button)
        add_hover_effect(update_feedback_button)
        update_feedback_button.configure(width=get_button_width())
        update_feedback_button.grid(row=4, column=1, pady=10)

        # Input Feedback Button
        input_feedback_button = tk.Button(
            self,
            text="Input Feedback",
            command=self.open_feedback_input_form
        )
        apply_button_style(input_feedback_button)
        add_hover_effect(input_feedback_button)
        input_feedback_button.configure(width=get_button_width())
        input_feedback_button.grid(row=5, column=1, pady=10)

        # Generate Reports Button
        generate_reports_button = tk.Button(
            self,
            text="Generate Reports",
            command=self.generate_reports
        )
        apply_button_style(generate_reports_button)
        add_hover_effect(generate_reports_button)
        generate_reports_button.configure(width=get_button_width())
        generate_reports_button.grid(row=6, column=1, pady=10)

        # Logout Button
        logout_button = tk.Button(
            self,
            text="Logout",
            command=self.logout
        )
        apply_button_style(logout_button)
        add_hover_effect(logout_button)
        logout_button.configure(width=get_button_width())
        logout_button.grid(row=7, column=1, pady=10)

    def open_create_account_form(self):
        # Open the account creation form in a new window
        create_account_window = tk.Toplevel(self)
        create_account_window.title("Create New Account")
        create_account_window.configure(bg=BACKGROUND_COLOR)

        # Set the window size to predefined constants
        create_account_window.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")

        # Configure grid layout for centering
        create_account_window.grid_rowconfigure(0, weight=1)
        create_account_window.grid_rowconfigure(6, weight=1)
        create_account_window.grid_columnconfigure(0, weight=1)
        create_account_window.grid_columnconfigure(3, weight=1)

        # Title Label
        title_label = tk.Label(create_account_window, text="Create New Account")
        apply_label_style(title_label, title=True)  # Apply title styling
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Role selection
        role_label = tk.Label(create_account_window, text="Role")
        apply_label_style(role_label)
        role_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        role_var = tk.StringVar(value="Agent")
        role_menu = tk.OptionMenu(create_account_window, role_var, "Agent", "Coach")
        role_menu.configure(font=FONT_MAIN, bg="white")
        role_menu.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Username input
        username_label = tk.Label(create_account_window, text="Username")
        apply_label_style(username_label)
        username_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        username_entry = tk.Entry(create_account_window)
        apply_entry_style(username_entry)
        username_entry.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Password input
        password_label = tk.Label(create_account_window, text="Password")
        apply_label_style(password_label)
        password_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        password_entry = tk.Entry(create_account_window, show="*")
        apply_entry_style(password_entry)
        password_entry.grid(row=3, column=2, sticky="w", padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(
            create_account_window,
            text="Create Account",
            command=lambda: self.create_account(username_entry.get(), password_entry.get(), role_var.get(), create_account_window)
        )
        apply_button_style(submit_button)
        add_hover_effect(submit_button)
        submit_button.configure(width=get_button_width())  # Use predefined button width
        submit_button.grid(row=4, column=0, columnspan=4, pady=20)

    def create_account(self, username, password, role, window):
        success, message, new_user = create_user(
            self.controller.users, 
            username,
            password,
            role
        )

        if not success:
            messagebox.showerror("Input Error", message)
            return

        # Save changes
        save_data(self.controller.users, self.controller.feedback_data, self.controller.report_data)

        # Refresh UI
        self.controller.frames[ViewFeedback].refresh_agent_dropdown()

        # Close the account creation form
        window.destroy()
        messagebox.showinfo("Account Created", message)

    # Adding new feedback for selected agent
    def open_feedback_input_form(self):
        # Open a new window for feedback input
        feedback_window = tk.Toplevel(self)
        feedback_window.title("Input New Feedback")
        feedback_window.configure(bg=BACKGROUND_COLOR)

        # Set the window size to predefined constants
        feedback_window.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")

        # Configure grid layout for centering
        feedback_window.grid_rowconfigure(0, weight=1)  # Space above content
        feedback_window.grid_rowconfigure(7, weight=1)  # Space below content
        feedback_window.grid_columnconfigure(0, weight=1)  # Space on left
        feedback_window.grid_columnconfigure(3, weight=1)  # Space on right

        # Title Label
        title_label = tk.Label(feedback_window, text="Input New Feedback")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Agent selection dropdown
        agent_label = tk.Label(feedback_window, text="Agent")
        apply_label_style(agent_label)
        agent_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        agent_names = [user['name'] for user in self.controller.users if user['role'] == 'Agent']
        agent_var = tk.StringVar(value="Select Agent")
        agent_dropdown = tk.OptionMenu(feedback_window, agent_var, *agent_names)
        agent_dropdown.configure(font=FONT_MAIN, bg="white")
        agent_dropdown.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Feedback text entry
        feedback_label = tk.Label(feedback_window, text="Feedback Text")
        apply_label_style(feedback_label)
        feedback_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        feedback_text_entry = tk.Entry(feedback_window, width=28)
        apply_entry_style(feedback_text_entry)
        feedback_text_entry.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(
            feedback_window,
            text="Submit Feedback",
            command=lambda: self.add_feedback(agent_var.get(), feedback_text_entry.get(), feedback_window),
        )
        apply_button_style(submit_button)
        add_hover_effect(submit_button)
        submit_button.configure(width=get_button_width())  # Use predefined button width
        submit_button.grid(row=3, column=0, columnspan=4, pady=20)

    def add_feedback(self, agent, feedback_text, window):
        success, message, new_feedback = create_feedback(
            agent,
            feedback_text,
            time.time()
        )

        if not success:
            messagebox.showerror("Input Error", message)
            return

        self.controller.feedback_data.append(new_feedback)
        save_data(self.controller.users, self.controller.feedback_data, self.controller.report_data)

        self.controller.users, self.controller.feedback_data, self.controller.report_data = load_data()
        self.controller.frames[ViewFeedback].populate_feedback_list(self.controller.feedback_data)

        window.destroy()
        messagebox.showinfo("Success", message)

    def generate_reports(self):
        # Open a new window for report generation
        report_window = tk.Toplevel(self)
        report_window.title("Generate Performance Reports")
        report_window.configure(bg=BACKGROUND_COLOR)

        # Set the window size to predefined constants
        report_window.geometry(f"{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}")

        # Configure grid layout for centering
        report_window.grid_rowconfigure(0, weight=1)  # Space above content
        report_window.grid_rowconfigure(7, weight=1)  # Space below content
        report_window.grid_columnconfigure(0, weight=1)  # Space on left
        report_window.grid_columnconfigure(3, weight=1)  # Space on right

        # Title Label
        title_label = tk.Label(report_window, text="Agent Reports")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=0, columnspan=4, pady=20)

        # Agent selection dropdown
        agent_label = tk.Label(report_window, text="Agent")
        apply_label_style(agent_label)
        agent_label.grid(row=1, column=1, sticky="e", padx=10, pady=5)

        agent_names = [user['name'] for user in self.controller.users if user['role'] == 'Agent']
        agent_var = tk.StringVar(value="Select Agent")
        agent_dropdown = tk.OptionMenu(report_window, agent_var, *agent_names)
        agent_dropdown.configure(font=FONT_MAIN, bg="white")
        agent_dropdown.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Date range entries (start and end)
        start_date_label = tk.Label(report_window, text="Start Date (dd/mm/yyyy)")
        apply_label_style(start_date_label)
        start_date_label.grid(row=2, column=1, sticky="e", padx=10, pady=5)

        start_date_entry = tk.Entry(report_window)
        apply_entry_style(start_date_entry)
        start_date_entry.grid(row=2, column=2, sticky="w", padx=10, pady=5)

        end_date_label = tk.Label(report_window, text="End Date (dd/mm/yyyy)")
        apply_label_style(end_date_label)
        end_date_label.grid(row=3, column=1, sticky="e", padx=10, pady=5)

        end_date_entry = tk.Entry(report_window)
        apply_entry_style(end_date_entry)
        end_date_entry.grid(row=3, column=2, sticky="w", padx=10, pady=5)

        # Generate button
        generate_button = tk.Button(
            report_window,
            text="Generate Report",
            command=lambda: self.generate_agent_report(
                agent_var.get(),
                start_date_entry.get(),
                end_date_entry.get(),
                report_window,
            ),
        )
        apply_button_style(generate_button)
        add_hover_effect(generate_button)
        generate_button.configure(width=get_button_width())
        generate_button.grid(row=4, column=0, columnspan=4, pady=20)

    def generate_agent_report(self, agent_name, start_date, end_date, window):
        try:
            # Code that may raise an exception
            # Refresh data to ensure it's up-to-date
            self.controller.users, self.controller.feedback_data, self.controller.report_data = load_data()

            # Convert start and end dates
            self.controller.report_generator.filter_by_date(start_date, end_date)

            # Filter by agent
            agent_report = self.controller.report_generator.report_for_agent_id(agent_name)

            # Save report to CSV
            if agent_report:
                csv_path = f"{agent_name}_report_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                self.controller.report_generator.save_report_to_csv(agent_report, csv_path)
                tk.messagebox.showinfo("Success", f"Report generated as {csv_path}.")
            else:
                tk.messagebox.showwarning("No Data", f"No data for {agent_name} in the selected date range.")

            window.destroy()  # Close the report window

        except ValueError as e:
            # Handles invalid input (e.g., wrong date format).
            # Shows a user-friendly error message without exposing technical details.
            tk.messagebox.showerror("Invalid Date Format", "Enter dates in dd/mm/yyyy format.")
        except Exception as e:
            # Catches any other errors to prevent crashes.
            # Displays the error details to help users or developers identify the issue.
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    def logout(self):
        """Clear the current user and go back to the login screen."""
        self.controller.current_user = None  # Reset current_user
        self.controller.show_frame(LoginScreen)


# In[9]:


class ReportGenerator:

    """
    A class for generating and managing reports from feedback data.

    - Filters feedback data based on a date range.
    - Generates reports for specific agents from filtered feedback.
    - Provides utilities to save reports to a CSV file and summarize feedback by status.
    - Methods:
        - filter_by_date(): Filters feedback data within a given start and end date.
        - report_for_agent_id(): Extracts feedback for a specific agent from the filtered data.
        - save_report_to_csv(): Saves report data to a CSV file (static method).
        - summary_by_status(): Counts feedback items by status in the filtered feedback.
    """

    def __init__(self, feedback_data):
        self.feedback_data = feedback_data
        self.filtered_feedback = []

    def filter_by_date(self, start_date=None, end_date=None):
        """Filter feedback data by a given date range."""
        self.filtered_feedback = []
        try:
            # Parse and normalize start and end dates dd/mm/yyyy format to 00:00:00 and 23:59:59, respectively.
            if start_date:
                start_date = datetime.strptime(start_date, "%d/%m/%Y")  # Convert to datetime
                start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)  # Explicitly set to 00:00:00
            if end_date:
                end_date = datetime.strptime(end_date, "%d/%m/%Y")  # Convert to datetime
                end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)  # Explicitly set to 23:59:59

            # Filters feedback data within the specified date range.
            self.filtered_feedback = [
                entry for entry in self.feedback_data
                if isinstance(entry["updated_at"], datetime) and
                (not start_date or entry["updated_at"] >= start_date) and
                (not end_date or entry["updated_at"] <= end_date)
            ]
        # Raises a ValueError with a clear message if dates are not in the correct format.
        except ValueError as e:
            raise ValueError("Invalid date format. Please use dd/mm/yyyy.") from e

    def report_for_agent_id(self, agent_id):
        """Generate a report for a specific agent from the filtered data."""
        return [entry for entry in self.filtered_feedback if entry["agent"] == agent_id]

    @staticmethod # Not an instance of class! Is utility function within the class.
    def save_report_to_csv(report_data, file_path="agent_report.csv"):
        """Save the report data to a CSV file."""
        fieldnames = ["feedback_id", "agent", "feedback_text", "status", "updated_at"]

        with open(file_path, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for entry in report_data:
                entry["updated_at"] = entry["updated_at"].strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow(entry)

    def summary_by_status(self):
        """Provide a summary count of feedback items by status in the filtered data."""
        summary = {}
        for entry in self.filtered_feedback:
            status = entry["status"]
            summary[status] = summary.get(status, 0) + 1
        return summary


# In[10]:


class ProfileSettings(tk.Frame):

    """
    A Tkinter frame for updating the current user's password and navigating back to the main menu.

    - Allows users to input their current and new passwords.
    - Validates the current password and updates it if correct.
    - Includes a back button to navigate to the appropriate main menu based on user role.
    - Methods:
        - update_password(): Validates and updates the user's password, saving changes to the data.
        - go_back(): Navigates back to the main menu based on the user's role.
        - clear_password_fields(): Clears the password entry fields.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)

        # Configure grid layout for centering
        self.grid_rowconfigure(0, weight=1)  # Space above the content
        self.grid_rowconfigure(6, weight=1)  # Space below the content
        self.grid_columnconfigure(0, weight=1)  # Space to the left
        self.grid_columnconfigure(3, weight=1)  # Space to the right

        # Title Label
        title_label = tk.Label(self, text="Profile Settings")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=1, columnspan=2, pady=(20, 10))

        # Current password field
        current_pw_label = tk.Label(self, text="Current Password")
        apply_label_style(current_pw_label)
        current_pw_label.grid(row=1, column=1, padx=(10, 5), pady=10, sticky="e")

        self.current_password = tk.Entry(self, show="*")
        apply_entry_style(self.current_password)
        self.current_password.grid(row=1, column=2, padx=(5, 10), pady=10, sticky="w")

        # New password field
        new_pw_label = tk.Label(self, text="New Password")
        apply_label_style(new_pw_label)
        new_pw_label.grid(row=2, column=1, padx=(10, 5), pady=10, sticky="e")

        self.new_password = tk.Entry(self, show="*")
        apply_entry_style(self.new_password)
        self.new_password.grid(row=2, column=2, padx=(5, 10), pady=10, sticky="w")

        # Save button
        save_button = tk.Button(self, text="Save Changes", command=self.update_password)
        apply_button_style(save_button)
        add_hover_effect(save_button)
        save_button.configure(width=get_button_width())  # Dynamically adjust button width
        save_button.grid(row=3, column=1, columnspan=2, pady=(20, 10))

        # Back button
        back_button = tk.Button(self, text="Back to Main Menu", command=self.go_back)
        apply_button_style(back_button)
        add_hover_effect(back_button)
        back_button.configure(width=get_button_width())  # Dynamically adjust button width
        back_button.grid(row=4, column=1, columnspan=2, pady=(10, 20))

    def update_password(self):
        current_pw = self.current_password.get()
        new_pw = self.new_password.get()

        # Ensure current_user is a dictionary and has the required attributes
        if not self.controller.current_user:
            messagebox.showerror("Error", "No current user logged in.")
            return

        # Validate current password and update if it matches
        user = self.controller.current_user
        if user["password"] == current_pw:
            user["password"] = new_pw
            try:
                save_data(self.controller.users, self.controller.feedback_data, self.controller.report_data)
                messagebox.showinfo("Profile", "Password updated successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save changes: {e}")
        else:
            messagebox.showerror("Error", "Current password is incorrect.")

    def go_back(self):
        """Navigate back to the correct main menu based on the current user's role."""
        # Access the role directly from current_user
        user_role = self.controller.current_user.get("role")

        # Navigate to the correct frame based on the role
        if user_role == "Coach":
            self.controller.show_frame(CoachMainMenu)
        elif user_role == "Agent":
            self.controller.show_frame(AgentMainMenu)
        else:
            messagebox.showerror("Navigation Error", "Unable to determine user role for navigation.")

    def clear_password_fields(self):
        """Clear the current and new password fields."""
        self.current_password.delete(0, tk.END)
        self.new_password.delete(0, tk.END)


# In[11]:


class ViewFeedback(tk.Frame):

    """
    A Tkinter frame for coaches to view, filter, and update agent feedback.

    - Allows selection of an agent and displays their feedback in a listbox.
    - Provides options to filter feedback by agent and assign/update feedback status.
    - Includes buttons for saving changes and navigating back to the main menu.
    - Methods:
        - filter_feedback_by_agent(): Filters feedback by selected agent.
        - refresh_agent_dropdown(): Updates the agent dropdown menu.
        - populate_feedback_list(): Displays filtered feedback in the listbox.
        - on_agent_selection(): Handles agent selection from the dropdown.
        - update_feedback_status(): Updates the status of selected feedback and saves changes.
        - reset_view(): Resets the view to its default state.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=BACKGROUND_COLOR)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)  # Space above content
        self.grid_rowconfigure(7, weight=1)  # Space below content
        self.grid_columnconfigure(0, weight=1)  # Space to the left
        self.grid_columnconfigure(2, weight=1)  # Space to the right

        # Title Label
        title_label = tk.Label(self, text="View & Update Feedback")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # Agent selection label
        agent_label = tk.Label(self, text="Select Agent")
        apply_label_style(agent_label)
        agent_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        # Agent selection dropdown menu
        self.agent_var = tk.StringVar(value="Select Agent")
        agent_names = [agent['name'] for agent in self.controller.users if agent['role'] == 'Agent']
        self.agent_dropdown = tk.OptionMenu(self, self.agent_var, *agent_names, command=self.filter_feedback_by_agent)
        self.agent_dropdown.configure(font=FONT_MAIN, bg="white")
        self.agent_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Listbox label
        feedback_label = tk.Label(self, text="Select feedback to update!")
        apply_label_style(feedback_label)
        feedback_label.grid(row=2, column=0, columnspan=3, pady=10)

        # Listbox to display feedback
        self.feedback_listbox = tk.Listbox(self, width=30, height=10)
        apply_entry_style(self.feedback_listbox)
        self.feedback_listbox.grid(row=3, column=0, columnspan=3, padx=20, pady=5, sticky="ew")

        # Assign status label
        status_label = tk.Label(self, text="Assign Status")
        apply_label_style(status_label)
        status_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

        # Assign status dropdown menu
        self.status_var = tk.StringVar(value="Not Integrated")
        self.status_dropdown = tk.OptionMenu(self, self.status_var, "Not Integrated", "Integrated")
        self.status_dropdown.configure(font=FONT_MAIN, bg="white")
        self.status_dropdown.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Save button to update feedback status
        save_button = tk.Button(self, text="Save Status", command=self.update_feedback_status)
        apply_button_style(save_button)
        add_hover_effect(save_button)
        save_button.configure(width=get_button_width())
        save_button.grid(row=5, column=0, columnspan=3, pady=(20, 10))

        # Back button to return to the main menu
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(CoachMainMenu))
        apply_button_style(back_button)
        add_hover_effect(back_button)
        back_button.configure(width=get_button_width())
        back_button.grid(row=6, column=0, columnspan=3, pady=(10, 20))

    def filter_feedback_by_agent(self, agent_name):
        """Filter feedback based on selected agent."""
        if agent_name == "Select Agent" or not agent_name:
            # Clear the feedback list if no valid agent is selected
            self.populate_feedback_list([])
            return

        # Filter feedback data for the selected agent
        feedback_data = [fb for fb in self.controller.feedback_data if fb["agent"] == agent_name]
        self.populate_feedback_list(feedback_data)

    def refresh_agent_dropdown(self):
        """Refresh the agent dropdown menu to include all current agents."""
        agent_names = [agent['name'] for agent in self.controller.users if agent['role'] == 'Agent']
        menu = self.agent_dropdown["menu"]
        menu.delete(0, "end")  # Clear the current menu
        for agent_name in agent_names:
            menu.add_command(
                label=agent_name,
                command=lambda value=agent_name: self.on_agent_selection(value)
            )

    def populate_feedback_list(self, feedback_data):
        """Display feedback entries for the selected agent in the listbox."""
        self.feedback_listbox.delete(0, tk.END)
        for feedback in feedback_data:
            feedback_text = f"{feedback['feedback_id']}: {feedback['feedback_text']} (Status: {feedback['status']})"
            self.feedback_listbox.insert(tk.END, feedback_text)

    def on_agent_selection(self, agent_name):
        """Handle dropdown agent selection and trigger feedback filtering."""
        self.agent_var.set(agent_name)
        self.filter_feedback_by_agent(agent_name)

    def update_feedback_status(self):
        """Update the selected feedback's status and save it."""
        try:
            selected_index = self.feedback_listbox.curselection()[0]
            feedback_id = self.feedback_listbox.get(selected_index).split(":")[0]  # Extract feedback_id from selected entry

            # Find the exact feedback entry in self.controller.feedback_data by feedback_id
            selected_feedback = next((fb for fb in self.controller.feedback_data if fb["feedback_id"] == feedback_id), None)

            if selected_feedback is not None:
                # Update the selected feedback's status and timestamp
                selected_feedback["status"] = self.status_var.get()
                selected_feedback["updated_at"] = time.time()

                # Save the updated data
                save_data(self.controller.users, self.controller.feedback_data, self.controller.report_data)
                messagebox.showinfo("Success", "Feedback status updated successfully.")

                # Reapply the filter for the selected agent after updating
                selected_agent = self.agent_var.get()
                self.filter_feedback_by_agent(selected_agent)
            else:
                messagebox.showerror("Update Error", "Could not find the selected feedback entry.")

        except IndexError:
            messagebox.showerror("Selection Error", "Please select a feedback entry to update.")

    def reset_view(self):
        """Reset the feedback view to its initial state."""
        self.agent_var.set("Select Agent")  # Reset the dropdown to default
        self.populate_feedback_list([])    # Clear the feedback list


# In[12]:


class AgentViewFeedback(tk.Frame):

    """
    A Tkinter frame for agents to view and filter their feedback.

    - Displays feedback in a listbox with filtering options by status (All, Integrated, Not Integrated).
    - Allows refreshing the feedback list from CSV data.
    - Includes a back button to navigate to the main menu.
    - Methods:
        - refresh_feedback(): Reloads feedback from CSV and applies the current filter.
        - populate_feedback_list(): Displays filtered feedback for the logged-in agent.
        - filter_feedback(): Filters feedback based on the selected status.
        - refresh_feedback_on_login(): Refreshes feedback view when the agent logs in.
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)  # Space above content
        self.grid_rowconfigure(7, weight=1)  # Space below content
        self.grid_columnconfigure(0, weight=1)  # Space to the left
        self.grid_columnconfigure(2, weight=1)  # Space to the right

        # Title Label
        title_label = tk.Label(self, text="View Feedback")
        apply_label_style(title_label, title=True)
        title_label.grid(row=0, column=0, columnspan=3, pady=(20, 10))  # Centered across three columns

        # Filter by status label and dropdown
        filter_label = tk.Label(self, text="Select Status")
        apply_label_style(filter_label)
        filter_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        # Filter by status dropdown
        self.filter_var = tk.StringVar(value="All")
        self.filter_dropdown = tk.OptionMenu(self, self.filter_var, "All", "Integrated", "Not Integrated", command=self.filter_feedback)
        self.filter_dropdown.configure(font=FONT_MAIN, bg="white")
        self.filter_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="w")

                # Refresh button
        refresh_button = tk.Button(self, text="Refresh to View Selected Feedback", command=self.refresh_feedback)
        apply_button_style(refresh_button)
        add_hover_effect(refresh_button)
        refresh_button.configure(width=get_button_width())
        refresh_button.grid(row=2, column=0, columnspan=3, pady=(10, 10))  # Centered across three columns

        # Feedback Label
        feedback_label = tk.Label(self, text="Feedback")
        apply_label_style(feedback_label)
        feedback_label.grid(row=3, column=0, columnspan=3, pady=10)  # Centered across three columns

        # Feedback listbox
        self.feedback_listbox = tk.Listbox(self, width=50, height=10)
        apply_entry_style(self.feedback_listbox)
        self.feedback_listbox.grid(row=4, column=0, columnspan=3, padx=20, pady=5, sticky="ew")  # Spanning all columns

        # Back button
        back_button = tk.Button(self, text="Back to Main Menu", command=lambda: controller.show_frame(AgentMainMenu))
        apply_button_style(back_button)
        add_hover_effect(back_button)
        back_button.configure(width=get_button_width())
        back_button.grid(row=5, column=0, columnspan=3, pady=(10, 20))  # Centered across three columns

    def refresh_feedback(self):
        """Reload feedback data from CSV and repopulate list based on current filter."""
        # Reload the data from CSV using load_data()
        self.controller.users, self.controller.feedback_data, self.controller.report_data = load_data()
        # Apply the current filter after refreshing
        self.populate_feedback_list(self.filter_var.get())

    def populate_feedback_list(self, filter_status="All"):
        """Display feedback entries filtered by status in the listbox for the logged-in agent."""
        self.feedback_listbox.delete(0, tk.END)  # Clear the listbox

        # Check if current_user is set
        if not self.controller.current_user:
            self.feedback_listbox.insert(tk.END, "No feedback available.")
            return

        # Get the current agent's name from controller
        current_agent = self.controller.current_user['name']

        # Filter feedback data for the current agent and selected status
        feedback_data = [
            fb for fb in self.controller.feedback_data
            if fb["agent"] == current_agent and (filter_status == "All" or fb["status"] == filter_status)
        ]

        # Display filtered feedback entries in the listbox
        if feedback_data:
            for feedback in feedback_data:
                feedback_text = f"{feedback['feedback_id']}: {feedback['feedback_text']} (Status: {feedback['status']})"
                self.feedback_listbox.insert(tk.END, feedback_text)
        else:
            self.feedback_listbox.insert(tk.END, "No feedback available.")

    def filter_feedback(self, selected_filter):
        """Filter feedback based on the selected status in the dropdown menu for the logged-in agent."""
        # Use the selected_filter directly from the OptionMenu selection
        filtered_feedback = [
            entry for entry in self.controller.feedback_data
            if selected_filter == "All" or entry["status"] == selected_filter
        ]
        self.populate_feedback_list(filtered_feedback)

    def refresh_feedback_on_login(self):
        """Clear and refresh feedback for the logged-in agent upon accessing this screen."""
        self.populate_feedback_list(self.filter_var.get())  # Refresh based on current filter status


# In[13]:


if __name__ == "__main__":

    """
    Entry point of the application.
    - Creates an instance of the App class to initialize the GUI.
    - Starts the Tkinter event loop to keep the application running and responsive.
    """

    app = App() # Initialize the application
    app.mainloop() # Start the Tkinter main event loop

