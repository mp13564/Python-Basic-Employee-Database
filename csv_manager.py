import csv
import os


CSV_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "employees.csv"
)


def save_to_csv(employees):
    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "emp_id",
            "name",
            "position",
            "salary"
        ])

        for emp_id, details in employees.items():
            writer.writerow([
                emp_id,
                details["name"],
                details["position"],
                details["salary"]
            ])


def load_from_csv():
    employees = {}

    if not os.path.exists(CSV_FILE):
        return employees

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            try:
                employees[row["emp_id"]] = {
                    "name": row["name"],
                    "position": row["position"],
                    "salary": float(row["salary"])
                }

            except (KeyError, ValueError):
                continue

    return employees