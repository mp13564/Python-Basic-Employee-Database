from csv_manager import load_from_csv, save_to_csv


class Employee:

    def __init__(self):
        self.employee = load_from_csv()

    def add_employee(self, emp_id, name, position, salary):
        if emp_id in self.employee:
            return False, "Employee ID already exists"

        self.employee[emp_id] = {
            "name": name,
            "position": position,
            "salary": salary
        }

        save_to_csv(self.employee)

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

            save_to_csv(self.employee)

            return True, "Salary updated successfully"

        return False, "Employee not found"

    def remove_employee(self, emp_id):
        if emp_id in self.employee:
            del self.employee[emp_id]

            save_to_csv(self.employee)

            return True, "Employee removed successfully"

        return False, "Employee not found"

    def total_payroll(self):
        return sum(
            employee["salary"]
            for employee in self.employee.values()
        )


# Test the Employee module
if __name__ == "__main__":
    employee = Employee()

    print("Employee module is working!")
    print(employee.show_employee())