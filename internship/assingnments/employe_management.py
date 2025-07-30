EMPLOYEE_IDS = ("EMP001", "EMP002", "EMP003", "EMP004", "EMP005")
id_counter = 0

# Store employees in a list of dictionaries
employees = []

# Function to add a new employee
def add_employee(data, employee):
    global id_counter
    if id_counter < len(EMPLOYEE_IDS):
        employee['ID'] = EMPLOYEE_IDS[id_counter]
        id_counter += 1
        data.append(employee)
    else:
        print("No more IDs available!")

# Function to get average salary
def get_average_salary(data):
    total_salary = sum(emp['Salary'] for emp in data)
    return total_salary / len(data) if data else 0

# Function to list managers
def list_managers(data):
    return [emp['Name'] for emp in data if emp['Is_Manager']]

# Function to get employees by skill
def get_employee_by_skill(data, skill):
    return [emp['Name'] for emp in data if skill in emp['Skills']]

# Function to delete employee by ID
def delete_employee(data, emp_id):
    for emp in data:
        if emp['ID'] == emp_id:
            data.remove(emp)
            print(f"Employee {emp_id} deleted.")
            return
    print("Employee not found!")

# Function to print final summary
def print_summary(data):
    total_employees = len(data)
    avg_age = sum(emp['Age'] for emp in data) / total_employees if total_employees else 0
    highest_paid = max(data, key=lambda x: x['Salary']) if data else None
    
    # All unique skills
    unique_skills = {skill for emp in data for skill in emp['Skills']}
    
    # Skills count
    skill_count = {}
    for emp in data:
        for skill in emp['Skills']:
            skill_count[skill] = skill_count.get(skill, 0) + 1

    print("\n--- Company Summary ---")
    print("Total Employees:", total_employees)
    print("Average Age:", avg_age)
    if highest_paid:
        print("Highest Paid Employee:", highest_paid['Name'], "-", highest_paid['Salary'])
    print("Unique Skills:", unique_skills)
    print("Skills Count:", skill_count)

# Example usage:

# Adding employees
add_employee(employees, {
    'Name': "najiya",
    'Age': 22,
    'Salary': 50000,
    'Is_Manager': False,
    'Skills': ["Python", "SQL"]
})

add_employee(employees, {
    'Name': "dilfa",
    'Age': 21,
    'Salary': 70000,
    'Is_Manager': True,
    'Skills': ["Management", "Excel"]
})

add_employee(employees, {
    'Name': "Ajmal",
    'Age': 25,
    'Salary': 80000,
    'Is_Manager': True,
    'Skills': ["Python", "Leadership"]
})

# Get employees above 30
above_30 = [emp['Name'] for emp in employees if emp['Age'] > 30]
print("Employees above 30:", above_30)

# Get all unique skills
all_skills = {skill for emp in employees for skill in emp['Skills']}
print("All Unique Skills:", all_skills)

# Test other functions
print(print_summary(employees))
print("Average Salary:", get_average_salary(employees))
print("Managers:", list_managers(employees))
print("Employees with")
