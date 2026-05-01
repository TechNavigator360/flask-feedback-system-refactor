# Agent & Coach Feedback Application

## Overview
The Agent and Coach Feedback Application is a Tkinter-based desktop tool developed in Jupyter Notebook. It provides a user-friendly interface to facilitate collaboration between agents and coaches, enabling functionality such as viewing feedback, creating reports, and managing accounts.

## App Creation Details

1. **Programming Language: Python**  
   - The app was built entirely using Python, chosen for its simplicity, readability, and extensive standard library support.

2. **GUI Framework: Tkinter**  
   - A built-in Python library for creating desktop GUI applications. Used to design the graphical user interface, including:
     - **Frames**: For screen layouts like login, main menu, and feedback screens.
     - **Widgets**: Buttons, labels, entry fields, dropdowns, and listboxes for user interaction.
     - **Event Loop (`mainloop`)**: Ensures the app remains responsive to user actions.

3. **Libraries and Standard Modules**  
   - **tkinter**: For the GUI interface.
   - **csv**: For reading and writing tabular data to/from the `data.csv` file.
   - **datetime**: For handling timestamps, date filtering, and report generation.
   - **logging**: For debugging and warning messages, ensuring better error tracking.
   - **time**: For generating unique IDs (based on timestamps).

4. **Data Management**  
   - **CSV Files**: Data is stored and managed using a single `data.csv` file.
     - Includes data for:
       - **Users**: Username, password, and role (Agent or Coach).
       - **Feedback**: Feedback ID, agent, feedback text, status, and timestamps.
   - Reports are exported as new CSV files to the `src` directory.

5. **Application Structure**  
   - **Object-Oriented Design**: Classes were used to encapsulate functionality, improving maintainability and readability:
     - **App**: Manages the application, initializes the GUI, and handles navigation between screens.
     - **Screen Classes** (e.g., `LoginScreen`, `AgentMainMenu`, `CoachMainMenu`): Encapsulate the layout and functionality for each screen.
     - **Utility Classes** (e.g., `ReportGenerator`): Handle specific tasks like generating reports.
   - **Event-Driven Programming**: Tkinter's event-handling system is used to respond to user actions like button clicks and input submissions.

6. **Development Tools**  
   - **Jupyter Notebook**: The app was developed in a Jupyter Notebook as an assignment requirement.

7. **Styling and User Experience**  
   - **Custom Styling**: A consistent design was implemented using predefined colors, fonts, and layout configurations.
   - **Responsive Layout**: Grid-based layouts allow dynamic resizing of components to adapt to different window sizes.

8. **Key Features**  
   - **Role-Based Access**: Agents and Coaches have distinct interfaces tailored to their needs.
   - **Data Persistence**: All changes (e.g., new feedback, updates, and reports) are saved to `data.csv` for persistence.
   - **Report Generation**: Coaches can generate agent-specific performance reports filtered by date range and save them as CSV files.
   - **Profile Management**: Users can update their passwords and manage their accounts.

9. **Limitations**  
   - No encryption for passwords stored in the CSV file.
   - Limited scalability as it relies on CSV for data storage instead of a database.
   - Single-user environment (no support for concurrent users).

---

## Setup and Installation

### Requirements
1. Python 3.8 or higher
2. Jupyter Notebook
3. Required libraries:
   - `tkinter`  
   - `csv`  
   - `logging`  
   - `time`  
   - `datetime`  
   - `from datetime import datetime`

### Installation Steps
1. **Unpack the ZIP File**  
   - Download and extract the ZIP file to a local folder on your computer.
   - Ensure the extracted folder contains the following files:
     - `bp4_app.ipynb`: The Jupyter Notebook with the application code.
     - `data.csv`: Data file for users, feedback, and reports.

2. **Ensure Python is Installed**  
   - Make sure Python (version 3.8 or higher) is installed. To verify, open a terminal or command prompt and run:
     ```
     python --version
     ```
   - If Python is not installed, download and install it from [python.org](https://www.python.org).

3. **Ensure Jupyter Notebook Support**  
   - Install Jupyter Notebook if it isn’t already available:
     ```
     pip install notebook
     ```
   - Verify that Jupyter is installed by running:
     ```
     jupyter --version
     ```

4. **Open the Application in Your IDE**  
   - Import the extracted project folder into your IDE (e.g., PyCharm, Visual Studio Code).

5. **Open the Notebook File**  
   - Use the Jupyter Notebook integration in your IDE (or install a Jupyter plugin if required).
   - Locate and open the `bp4_app.ipynb` file.

6. **Run All Cells**  
   - In your IDE’s Jupyter interface:
     - Execute all cells sequentially to ensure the application initializes.
     - Locate the cell containing:
       ```python
       if __name__ == "__main__":
           app = App()
           app.mainloop()
       ```
     - Execute this cell to start the application. The Tkinter application window will launch, and the login screen will be displayed.

7. **Application Flow**  
   - Use the GUI to navigate through the application:
     - Log in as an Agent or Coach.
     - Perform actions like viewing feedback, generating reports, or managing accounts.

---

## Using the App

### Login
1. Select your role (Agent or Coach) from the dropdown menu.
2. Enter your username and password:
   - **Agent**: Username: `agent1`, Password: `pass123`.
   - **Coach**: Username: `coach1`, Password: `pass456`.
3. Click the "Login" button to proceed to the main menu for your role.

### Agent Main Menu
1. Manage profile settings.
2. View and filter feedback.
3. Logout.

### Coach Main Menu
1. Manage profile settings.
2. Create accounts for agents or other coaches.
3. Update feedback status for agents.
4. Provide feedback for agents.
5. Generate reports based on agent performance.
6. Logout.

---

## File Structure (from ZIP Directory)
```plaintext
LU4/
├── src/
│   ├── bp4_app.ipynb        # Application code
│   ├── data.csv             # Data file
├── Tests/
│   ├── test_app.ipynb       # Test code
│   ├── data.csv             # Test data
└── README.md                # Documentation
```

### Data Management

#### Data Storage
- Data is stored in `data.csv` for simplicity.
  - **Types of Data**:
    - **Users**: Includes username, password, and role. 
    - **Feedback**: Includes feedback ID, agent, text, status, and timestamps.

#### Adding New Data
- Coaches and agents can change their passwords via the profile screen; changes are saved automatically to `data.csv`.
- Coaches can add new accounts or provide feedback and update feedback status directly through the application interface.
- All changes are automatically persisted in `data.csv`.

#### Generated Reports
- Reports are generated directly within the application.
- They are exported as new CSV files to the `src` directory, where they can be accessed and viewed.