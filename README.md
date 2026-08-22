# Employee Management System

A simple Employee Management System built with **Python** and **Flet**.

This project allows users to add, search, update, and remove employees while automatically saving employee information to a CSV file.

The project was also structured into separate Python modules to make the application easier to understand, maintain, troubleshoot, and expand in the future.

---

## 📌 Project Overview

The Employee Management System is a desktop application designed to manage basic employee information.

Each employee record currently contains:

- Employee ID
- Name
- Position
- Salary

The application uses a CSV file as its data storage, so employee information remains available even after closing and reopening the application.

---

## ✨ Features

### Employee Management

- Add a new employee
- Search for an employee
- Update employee salary
- Remove an employee
- Clear input fields

### Employee Information

The system currently stores:

| Field | Description |
|---|---|
| Employee ID | Unique identifier for the employee |
| Name | Employee's full name |
| Position | Employee's job position |
| Salary | Employee's salary |

### Data Management

- Automatically loads employee data from CSV
- Automatically saves changes to CSV
- Manually save employee data
- Download a timestamped copy of the CSV file
- Calculates total payroll

### User Interface

The application uses **Flet** to provide a graphical user interface.

The interface includes:

- Input fields
- Buttons
- Employee table
- Status messages
- Total payroll display

---

## 🛠️ Technologies Used

- **Python**
- **Flet**
- **CSV**
- **Object-Oriented Programming (OOP)**
- **VS Code**

### Python Modules Used

The project uses several built-in Python modules:

- `csv`
- `os`
- `shutil`
- `datetime`
- `pathlib`

---

## 📂 Project Structure

```text
Employee Management System
│
├── main.py
├── ui.py
├── employee.py
├── csv_manager.py
├── employees.csv
├── README.md
└── __pycache__/