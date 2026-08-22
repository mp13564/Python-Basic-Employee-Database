import shutil
from datetime import datetime
from pathlib import Path

import flet as ft

from csv_manager import save_to_csv, CSV_FILE


def create_page(page: ft.Page, emp):

    # ==================================================
    # PAGE SETTINGS
    # ==================================================

    page.title = "Employee Management System"
    page.window.width = 850
    page.window.height = 700
    page.padding = 25
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # ==================================================
    # INPUT FIELDS
    # ==================================================

    emp_id_field = ft.TextField(
        label="Employee ID",
        width=170
    )

    name_field = ft.TextField(
        label="Name",
        width=200
    )

    position_field = ft.TextField(
        label="Position",
        width=200
    )

    salary_field = ft.TextField(
        label="Salary",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # ==================================================
    # STATUS AND PAYROLL
    # ==================================================

    status_text = ft.Text(
        value="",
        color=ft.Colors.GREEN_700,
        weight=ft.FontWeight.BOLD
    )

    payroll_text = ft.Text(
        value="Total Payroll: 0.00",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # ==================================================
    # EMPLOYEE TABLE
    # ==================================================

    table = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Text("ID")
            ),

            ft.DataColumn(
                ft.Text("Name")
            ),

            ft.DataColumn(
                ft.Text("Position")
            ),

            ft.DataColumn(
                ft.Text("Salary"),
                numeric=True
            ),
        ],

        rows=[],

        border=ft.Border(
            top=ft.BorderSide(
                1,
                ft.Colors.GREY_300
            ),
            right=ft.BorderSide(
                1,
                ft.Colors.GREY_300
            ),
            bottom=ft.BorderSide(
                1,
                ft.Colors.GREY_300
            ),
            left=ft.BorderSide(
                1,
                ft.Colors.GREY_300
            ),
        ),

        border_radius=8,

        heading_row_color=ft.Colors.BLUE_50,
    )

    # ==================================================
    # HELPER FUNCTIONS
    # ==================================================

    def set_status(message, ok=True):

        status_text.value = message

        if ok:
            status_text.color = ft.Colors.GREEN_700
        else:
            status_text.color = ft.Colors.RED_600

        page.update()

    def clear_fields():

        emp_id_field.value = ""
        name_field.value = ""
        position_field.value = ""
        salary_field.value = ""

    def validate_salary(raw):

        try:
            return True, float(raw)

        except (TypeError, ValueError):
            return False, None

    def refresh_table():

        table.rows.clear()

        for emp_id, details in emp.show_employee().items():

            table.rows.append(
                ft.DataRow(
                    cells=[

                        # Employee ID
                        ft.DataCell(
                            ft.Text(emp_id)
                        ),

                        # Name
                        ft.DataCell(
                            ft.Text(
                                details["name"]
                            )
                        ),

                        # Position
                        ft.DataCell(
                            ft.Text(
                                details["position"]
                            )
                        ),

                        # Salary
                        ft.DataCell(
                            ft.Text(
                                f"{details['salary']:.2f}"
                            )
                        ),
                    ]
                )
            )

        payroll_text.value = (
            f"Total Payroll: "
            f"{emp.total_payroll():.2f}"
        )

        page.update()

    # ==================================================
    # ADD EMPLOYEE
    # ==================================================

    def add_click(e):

        employee_id = emp_id_field.value.strip()
        name = name_field.value.strip()
        position = position_field.value.strip()

        valid_salary, salary = validate_salary(
            salary_field.value
        )

        # Check required fields
        if not employee_id or not name or not position:

            set_status(
                "Please enter Employee ID, Name, and Position",
                ok=False
            )

            return

        # Check salary
        if not valid_salary:

            set_status(
                "Salary must be a valid number",
                ok=False
            )

            return

        # Add employee
        success, message = emp.add_employee(
            employee_id,
            name,
            position,
            salary
        )

        set_status(
            message,
            ok=success
        )

        # Refresh after successful addition
        if success:

            clear_fields()

            refresh_table()

    # ==================================================
    # SEARCH EMPLOYEE
    # ==================================================

    def search_click(e):

        employee_id = emp_id_field.value.strip()

        if not employee_id:

            set_status(
                "Enter an Employee ID to search",
                ok=False
            )

            return

        found, details = emp.search_employee(
            employee_id
        )

        if found:

            # Display employee information
            name_field.value = details["name"]

            position_field.value = details["position"]

            salary_field.value = str(
                details["salary"]
            )

            set_status(
                f"Found: {details['name']}",
                ok=True
            )

        else:

            set_status(
                "Employee not found",
                ok=False
            )

        page.update()

    # ==================================================
    # UPDATE SALARY
    # ==================================================

    def update_click(e):

        employee_id = emp_id_field.value.strip()

        valid_salary, salary = validate_salary(
            salary_field.value
        )

        if not employee_id:

            set_status(
                "Enter an Employee ID to update",
                ok=False
            )

            return

        if not valid_salary:

            set_status(
                "Salary must be a valid number",
                ok=False
            )

            return

        success, message = emp.update_salary(
            employee_id,
            salary
        )

        set_status(
            message,
            ok=success
        )

        if success:

            clear_fields()

            refresh_table()

    # ==================================================
    # REMOVE EMPLOYEE
    # ==================================================

    def remove_click(e):

        employee_id = emp_id_field.value.strip()

        if not employee_id:

            set_status(
                "Enter an Employee ID to remove",
                ok=False
            )

            return

        success, message = emp.remove_employee(
            employee_id
        )

        set_status(
            message,
            ok=success
        )

        if success:

            clear_fields()

            refresh_table()

    # ==================================================
    # CLEAR FIELDS
    # ==================================================

    def clear_click(e):

        clear_fields()

        status_text.value = ""

        page.update()

    # ==================================================
    # SAVE CSV
    # ==================================================

    def save_click(e):

        save_to_csv(
            emp.employee
        )

        set_status(
            f"Saved {len(emp.employee)} "
            f"employee(s) to employees.csv",
            ok=True
        )

    # ==================================================
    # DOWNLOAD CSV
    # ==================================================

    def download_click(e):

        if not emp.employee:

            set_status(
                "No employees to download yet",
                ok=False
            )

            return

        # Save latest data first
        save_to_csv(
            emp.employee
        )

        downloads_dir = (
            Path.home() / "Downloads"
        )

        try:

            downloads_dir.mkdir(
                parents=True,
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            destination = (
                downloads_dir
                / f"employees_{timestamp}.csv"
            )

            shutil.copy(
                CSV_FILE,
                destination
            )

            set_status(
                f"Downloaded to {destination}",
                ok=True
            )

        except OSError as error:

            set_status(
                f"Download failed: {error}",
                ok=False
            )

    # ==================================================
    # PAGE LAYOUT
    # ==================================================

    page.add(

        # Application title
        ft.Text(
            "Employee Management System",
            size=26,
            weight=ft.FontWeight.BOLD
        ),

        ft.Divider(),

        # ------------------------------------------------
        # Input fields
        # ------------------------------------------------

        ft.Row(
            [
                emp_id_field,
                name_field,
                position_field,
                salary_field
            ],
            wrap=True
        ),

        # ------------------------------------------------
        # Buttons
        # ------------------------------------------------

        ft.Row(
            [
                ft.ElevatedButton(
                    "Add",
                    icon=ft.Icons.PERSON_ADD,
                    on_click=add_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Search",
                    icon=ft.Icons.SEARCH,
                    on_click=search_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Update Salary",
                    icon=ft.Icons.EDIT,
                    on_click=update_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Remove",
                    icon=ft.Icons.DELETE,
                    on_click=remove_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Clear Fields",
                    icon=ft.Icons.CLEAR,
                    on_click=clear_click,
                    bgcolor=ft.Colors.BLUE_600,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Save",
                    icon=ft.Icons.SAVE,
                    on_click=save_click,
                    bgcolor=ft.Colors.GREEN_700,
                    color=ft.Colors.WHITE
                ),

                ft.ElevatedButton(
                    "Download CSV",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=download_click,
                    bgcolor=ft.Colors.GREEN_600,
                    color=ft.Colors.WHITE
                ),
            ],
            wrap=True
        ),

        # ------------------------------------------------
        # Status message
        # ------------------------------------------------

        status_text,

        ft.Divider(),

        # ------------------------------------------------
        # Employee list
        # ------------------------------------------------

        ft.Text(
            "Employee List",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        table,

        ft.Divider(),

        # ------------------------------------------------
        # Payroll
        # ------------------------------------------------

        payroll_text,
    )

    # Load employee data into the table
    refresh_table()