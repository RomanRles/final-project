# Construction Budget Adminisrator

#### Video Demo: <https://youtu.be/FEM_HTi2HLg>

#### Description:

>My version of a Budget Creator for the CS50 final Project, Oriented to construction workers based on my experience working on that field. To help in organizing items, costs, quantities, and profits; also providing storage, and access on the budgets created by the user. This project final objetive is to enhance the process of creating a budget for 2 options: 
1. Materials of construction
2. Labour 


## Contents
- [Distribution Code](#distribution-code)
- [Features](#features)

## Stack of technologies
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Static Badge](https://img.shields.io/badge/SQL-brightgreen?style=for-the-badge&logo=sqlite&logoColor=white&color=%237a0707)

![Static Badge](https://img.shields.io/badge/bootstrap-logo?style=for-the-badge&logo=bootstrap&logoColor=black&color=%237952B3)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Static Badge](https://img.shields.io/badge/html-logo?style=for-the-badge&logo=html5&logoColor=black&color=%23E34F26)
![Static Badge](https://img.shields.io/badge/css3-logo?style=for-the-badge&logo=css3&logoColor=black&color=%231572B6)
![Static Badge](https://img.shields.io/badge/jinja-logo?style=for-the-badge&logo=jinja&logoColor=black&color=white)


![Static Badge](https://img.shields.io/badge/git-logo?style=for-the-badge&logo=git&logoColor=black&color=%23F05032)
![Static Badge](https://img.shields.io/badge/github-logo?style=for-the-badge&logo=github&logoColor=black&color=white)





# Flask Budget Creator

## Distribution Code

- **`app.py`**
- **`static/`**
- **`templates/`**

### `app.py` Overview

This file is the core of the application, handling configurations, routing, and core functionalities:

1. **Imports and Configuration**
   - Imports libraries and initializes Flask app.
   - Configures `Session` and connects to `budget_admin.db`.
   - Sets the `UPLOAD_FOLDER` path for profile images and allowed file types.

2. **Helper Functions**
   - **`allowed_file(filename)`**: Checks file extension (PNG, JPG, GIF).
   - **`inject_user()`**: Makes user profile data globally accessible in templates.

3. **Database Initialization**
   - Initializes the database schema, including tables for users and budgets.

4. **Routes**
   - **`index`**: Main budget entry page, calculates total budget, stores in the database.
   - **`history`**: Displays all user-created budgets.
   - **`view_budget`**: Shows detailed budget info.

5. **User Authentication Routes**
   - **`login`** and **`register`**: Handles user login and registration with hashed passwords.

6. **Profile Management**
   - **`user_profile`**: Displays profile information.
   - **`upload_image`**: Allows users to upload profile images.
   - **`change_password`**: Enables password changes.

7. **Logout**
   - **`logout`**: Clears session and redirects to login.

---

### `static/` Folder Overview

The `static/` folder holds resources that don’t change dynamically:

- **`uploads/`**: Stores user-uploaded profile images.
- **`styles.css`**: Custom CSS for the application, linked in templates.

---

### `templates/` Folder Overview

The `templates/` folder contains HTML templates for each route:

- **`layout.html`**: Base template with navigation and footer.
- **`register.html`**, **`login.html`**: Forms for user registration and login.
- **`index.html`**: Budget creator form.
- **`history.html`**: List of user budgets.
- **`view_budget.html`**: Detailed budget info.
- **`user_profile.html`**: Displays user info and profile image.
- **`change_password.html`**: Form to change password.

---

### `helpers.py` File Overview

Contains utility functions for user authentication:

- **`login_required(f)`**: A decorator ensuring the user is logged in before accessing protected routes.

---
## Features
- [User session management](#user-session-management )
- [Budget Creation](#budget-creation)
- [History Tracking](#history-tracking)



### User Session Management
- **Login and Registration**: Securely handles user login and registration.
  - **Security**: Uses `werkzeug.security` to hash passwords.
  - **Register**: Takes `username`, `password`, and `confirm` fields, storing hashed passwords in `users` table.
  - **Login**: Verifies entered password by comparing with stored hash.
  - **Session**: Stores user ID in session upon successful login.

### Budget Creation
- **Cheat Sheet Template**: For creating and managing budgets.
  - **Inputs**:
    - **Budget Type**: Dropdown to select between "Labor" and "Materials".
    - **Budget Title**: Field to assign a title.
    - **Item Details**: Fields for item description, cost, quantity, and profit percentage.
  - **Total Calculation**: Automatically computes total cost including profit margin:
    ```
    Total = (Item Cost * Quantity) + (Profit Percentage / 100 * Total Item Cost)
    ```

### History Tracking
- **Database Structure**:
  - `users`: Stores user information.
  - `budgets`: Tracks each user-created budget.
  - `budget_items`: Lists items within each budget.
- **History Route**: Displays all user budgets with columns for title, type, total cost, and creation date. Users can click a budget to view detailed information.
- **Budget Detail View**: Shows in-depth budget info including item breakdown, profit margin, and total cost.

### Profile Management
- **User Profile Page**: Displays current user info and profile image.
- **Image Upload**: Allows profile image upload with validation (PNG, JPG, GIF).
- **Change Password**: Lets users update passwords securely, with current and new password fields. Passwords are hashed before storing.
- **Logout**: Clears session data and redirects to login.

These functionalities allow users to securely manage their accounts, create and track budgets, and view budget history details effectively.
