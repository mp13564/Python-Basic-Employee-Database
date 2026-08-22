import csv
import os
import shutil
from datetime import datetime
from pathlib import Path
import flet as ft

CSV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "employees.csv")


class Employee:

    def __init__(self, csv_file=CSV_FILE):
        self.employee = {}
        self.csv_file = csv_file
        self.load_from_csv()

    def add_employee(self, emp_id, name, salary):
        if emp_id in self.employee:
            return False, "Employee ID already exists"
        self.employee[emp_id] = {"name": name, "salary": salary}
        self.save_to_csv()
        return True, "Employee added successfully"

    def show_employee(self):
        return self.employee

    def search_employee(self, emp_id):
        if emp_id in self.employee:
            return True, self.employee[emp_id]
        return False, None

    def update_salary(self, emp_id, new_salary):
        if emp_id in self.employee:
            self.employee[emp_id]["salary"] = new_salary
            self.save_to_csv()
            return True, "Salary updated successfully"
        return False, "Employee not found"

    def remove_employee(self, emp_id):
        if emp_id in self.employee:
            del self.employee[emp_id]
            self.save_to_csv()
            return True, "Employee removed successfully"
        return False, "Employee not found"

    def total_payroll(self):
        return sum(e["salary"] for e in self.employee.values())

    # ---------- CSV persistence ----------
    def save_to_csv(self):
        """Write all employees to the CSV file. Called automatically after
        every add/update/remove, and can also be called manually."""
        with open(self.csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["emp_id", "name", "salary"])
            for emp_id, details in self.employee.items():
                writer.writerow([emp_id, details["name"], details["salary"]])

    def load_from_csv(self):
        """Load employees from the CSV file if it exists. Called once on startup."""
        if not os.path.exists(self.csv_file):
            return
        with open(self.csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    self.employee[row["emp_id"]] = {
                        "name": row["name"],
                        "salary": float(row["salary"]),
                    }
                except (KeyError, ValueError):
                    # Skip malformed rows instead of crashing the whole app
                    continue


def main(page: ft.Page):
    page.title = "Employee Management System"
    page.window.width = 780
    page.window.height = 680
    page.padding = 25
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    emp = Employee()

    # ---------- Form fields ----------
    emp_id_field = ft.TextField(label="Employee ID", width=180)
    name_field = ft.TextField(label="Name", width=220)
    salary_field = ft.TextField(label="Salary", width=150, keyboard_type=ft.KeyboardType.NUMBER)

    status_text = ft.Text(value="", color=ft.Colors.GREEN_700, weight=ft.FontWeight.BOLD)
    payroll_text = ft.Text(value="Total Payroll: 0.00", size=16, weight=ft.FontWeight.BOLD)

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Name")),
            ft.DataColumn(ft.Text("Salary"), numeric=True),
        ],
        rows=[],
        border=ft.Border(
            top=ft.BorderSide(1, ft.Colors.GREY_300),
            right=ft.BorderSide(1, ft.Colors.GREY_300),
            bottom=ft.BorderSide(1, ft.Colors.GREY_300),
            left=ft.BorderSide(1, ft.Colors.GREY_300),
        ),
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_50,
    )

    def set_status(message, ok=True):
        status_text.value = message
        status_text.color = ft.Colors.GREEN_700 if ok else ft.Colors.RED_600
        page.update()

    def clear_fields():
        emp_id_field.value = ""
        name_field.value = ""
        salary_field.value = ""

    def refresh_table():
        table.rows.clear()
        for emp_id, details in emp.show_employee().items():
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(emp_id)),
                        ft.DataCell(ft.Text(details["name"])),
                        ft.DataCell(ft.Text(f"{details['salary']:.2f}")),
                    ]
                )
            )
        payroll_text.value = f"Total Payroll: {emp.total_payroll():.2f}"
        page.update()

    def validate_salary(raw):
        try:
            return True, float(raw)
        except (TypeError, ValueError):
            return False, None

    # ---------- Button handlers ----------
    def add_click(e):
        eid, name = emp_id_field.value.strip(), name_field.value.strip()
        ok_sal, salary = validate_salary(salary_field.value)
        if not eid or not name:
            set_status("Please enter Employee ID and Name", ok=False)
            return
        if not ok_sal:
            set_status("Salary must be a valid number", ok=False)
            return
        ok, msg = emp.add_employee(eid, name, salary)
        set_status(msg, ok=ok)
        if ok:
            clear_fields()
            refresh_table()

    def search_click(e):
        eid = emp_id_field.value.strip()
        if not eid:
            set_status("Enter an Employee ID to search", ok=False)
            return
        found, details = emp.search_employee(eid)
        if found:
            name_field.value = details["name"]
            salary_field.value = str(details["salary"])
            set_status(f"Found: {details['name']}", ok=True)
        else:
            set_status("Employee not found", ok=False)
        page.update()

    def update_click(e):
        eid = emp_id_field.value.strip()
        ok_sal, salary = validate_salary(salary_field.value)
        if not eid:
            set_status("Enter an Employee ID to update", ok=False)
            return
        if not ok_sal:
            set_status("Salary must be a valid number", ok=False)
            return
        ok, msg = emp.update_salary(eid, salary)
        set_status(msg, ok=ok)
        if ok:
            clear_fields()
            refresh_table()

    def remove_click(e):
        eid = emp_id_field.value.strip()
        if not eid:
            set_status("Enter an Employee ID to remove", ok=False)
            return
        ok, msg = emp.remove_employee(eid)
        set_status(msg, ok=ok)
        if ok:
            clear_fields()
            refresh_table()

    def clear_click(e):
        clear_fields()
        status_text.value = ""
        page.update()

    def save_click(e):
        emp.save_to_csv()
        set_status(f"Saved {len(emp.employee)} employee(s) to employees.csv", ok=True)

    def download_click(e):
        if not emp.employee:
            set_status("No employees to download yet", ok=False)
            return
        # Make sure the CSV on disk is fully up to date before copying it
        emp.save_to_csv()

        downloads_dir = Path.home() / "Downloads"
        try:
            downloads_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = downloads_dir / f"employees_{timestamp}.csv"
            shutil.copy(emp.csv_file, dest)
            set_status(f"Downloaded to {dest}", ok=True)
        except OSError as ex:
            set_status(f"Download failed: {ex}", ok=False)

    # ---------- Layout ----------
    page.add(
        ft.Text("Employee Management System", size=26, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Row([emp_id_field, name_field, salary_field], wrap=True),
        ft.Row(
            [
                ft.ElevatedButton("Add", icon=ft.Icons.PERSON_ADD, on_click=add_click,
                                   bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),

                ft.ElevatedButton("Search", icon=ft.Icons.SEARCH, on_click=search_click,
                                   bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),

                ft.ElevatedButton("Update Salary", icon=ft.Icons.EDIT, on_click=update_click,
                                   bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),

                ft.ElevatedButton("Remove", icon=ft.Icons.DELETE, on_click=remove_click,
                                   bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),

                ft.ElevatedButton("Clear Fields", icon=ft.Icons.CLEAR, on_click=clear_click,
                                   bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),

                ft.ElevatedButton("Save", icon=ft.Icons.SAVE, on_click=save_click,
                                   bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE),

                ft.ElevatedButton("Download CSV", icon=ft.Icons.DOWNLOAD, on_click=download_click,
                                   bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE),
            ],
            wrap=True,
        ),
        status_text,
        ft.Divider(),
        ft.Text("Employee List", size=18, weight=ft.FontWeight.BOLD),
        table,
        ft.Divider(),
        payroll_text,
    )

    refresh_table()


if __name__ == "__main__":
    ft.app(target=main)