import flet as ft

from employee import Employee
from ui import create_page


def main(page: ft.Page):
    employee = Employee()

    create_page(page, employee)


if __name__ == "__main__":
    ft.app(target=main)
    