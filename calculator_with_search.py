"""A basic calculator with a searchable glossary of math concepts."""

import ast
import re
import sys

MATH_GLOSSARY = {
    "addition": "Combines numbers. Example: 2 + 3 = 5.",
    "subtraction": "Finds the difference between numbers. Example: 5 - 2 = 3.",
    "multiplication": "Combines equal groups. Example: 4 * 3 = 12.",
    "division": "Splits a number into equal groups. Example: 12 / 3 = 4.",
    "exponent": "Raises a number to a power. Example: 2 ** 3 = 8.",
    "remainder": "The amount left after division. The % operator finds it: 10 % 3 = 1.",
    "average": "The arithmetic mean: add the values and divide by how many values there are.",
    "area of a rectangle": "Area = length * width.",
    "area of a triangle": "Area = (base * height) / 2.",
    "circumference": "The distance around a circle: circumference = 2 * pi * radius.",
    "pythagorean theorem": "For a right triangle, a ** 2 + b ** 2 = c ** 2.",
    "percentage": "A percentage is a value out of 100. For example, 25% of 80 is (25 / 100) * 80.",
}

OPERATORS = {"+", "-", "*", "/", "**", "%"}


def calculate(first_number: float, operator: str, second_number: float) -> float:
    """Calculate a result for one supported operator."""
    if operator not in OPERATORS:
        raise ValueError(f"Unsupported operator: {operator}")
    if operator == "+":
        return first_number + second_number
    if operator == "-":
        return first_number - second_number
    if operator == "*":
        return first_number * second_number
    if operator == "/":
        if second_number == 0:
            raise ValueError("Cannot divide by zero.")
        return first_number / second_number
    if operator == "**":
        return first_number**second_number
    if second_number == 0:
        raise ValueError("Cannot find a remainder when dividing by zero.")
    return first_number % second_number


def search_math(query: str) -> list[tuple[str, str]]:
    """Return glossary entries whose term or description contains the query."""
    search_text = query.strip().casefold()
    if not search_text:
        return []

    return [
        (term, description)
        for term, description in MATH_GLOSSARY.items()
        if search_text in term.casefold() or search_text in description.casefold()
    ]


def basic_calculate() -> None:
    """Prompt for two numbers and an operator, then print the result."""
    try:
        first_number = float(input("First number: "))
        operator = input("Operator (+, -, *, /, **, %): ").strip()
        second_number = float(input("Second number: "))
        result = calculate(first_number, operator, second_number)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Result: {result:g}")


def run_calculator() -> None:
    basic_calculate()


def equation_solver_menu() -> None:
    """Solve a linear equation in the form ax + b = c."""
    try:
        coefficient = float(input("Coefficient a: "))
        constant = float(input("Constant b: "))
        right_side = float(input("Right side c: "))
    except ValueError as error:
        print(f"Error: {error}")
        return

    if coefficient == 0:
        if constant == right_side:
            print("Every value of x is a solution.")
        else:
            print("This equation has no solution.")
        return

    solution = (right_side - constant) / coefficient
    print(f"Solution: x = {solution:g}")


def _linear_terms(expression: ast.AST) -> tuple[float, float]:
    """Return the coefficient and constant in a linear expression."""
    if isinstance(expression, ast.Constant) and isinstance(
        expression.value, (int, float)
    ):
        return 0, float(expression.value)
    if isinstance(expression, ast.Name) and expression.id == "x":
        return 1, 0
    if isinstance(expression, ast.UnaryOp) and isinstance(
        expression.op, (ast.UAdd, ast.USub)
    ):
        coefficient, constant = _linear_terms(expression.operand)
        if isinstance(expression.op, ast.USub):
            return -coefficient, -constant
        return coefficient, constant
    if isinstance(expression, ast.BinOp):
        left_coefficient, left_constant = _linear_terms(expression.left)
        right_coefficient, right_constant = _linear_terms(expression.right)
        if isinstance(expression.op, ast.Add):
            return (
                left_coefficient + right_coefficient,
                left_constant + right_constant,
            )
        if isinstance(expression.op, ast.Sub):
            return (
                left_coefficient - right_coefficient,
                left_constant - right_constant,
            )
        if isinstance(expression.op, ast.Mult):
            if left_coefficient and right_coefficient:
                raise ValueError("Nonlinear expressions are not supported.")
            if left_coefficient:
                return left_coefficient * right_constant, left_constant * right_constant
            if right_coefficient:
                return right_coefficient * left_constant, right_constant * left_constant
            return 0, left_constant * right_constant
        if isinstance(expression.op, ast.Div):
            if right_coefficient:
                raise ValueError("Division by an expression containing x is not supported.")
            if right_constant == 0:
                raise ValueError("Cannot divide by zero.")
            return left_coefficient / right_constant, left_constant / right_constant
    raise ValueError("Enter a linear equation using numbers, x, and +, -, *, or /.")


def solve_linear_equation(equation: str) -> str:
    """Solve a text equation for x, such as 2x + 3 = 11."""
    sides = equation.split("=")
    if len(sides) != 2:
        raise ValueError("Enter one equation with exactly one '=' sign.")

    terms = []
    for side in sides:
        expression_text = re.sub(
            r"(?<=\d)\s*(?=x\b)", "*", side.casefold().strip()
        )
        try:
            expression = ast.parse(expression_text, mode="eval").body
        except SyntaxError as error:
            raise ValueError("Enter a valid linear equation.") from error
        terms.append(_linear_terms(expression))

    coefficient = terms[0][0] - terms[1][0]
    right_side = terms[1][1] - terms[0][1]
    if coefficient == 0:
        if right_side == 0:
            return "Every value of x is a solution."
        return "This equation has no solution."

    return f"Solution: x = {right_side / coefficient:g}"


def solve_fox_x() -> None:
    """Prompt for a linear equation and print its solution."""
    equation = input("Enter a linear equation (for example, 2x + 3 = 11): ")
    try:
        print(solve_linear_equation(equation))
    except ValueError as error:
        print(f"Error: {error}")


def visualize_search(matches: list[tuple[str, str]]) -> None:
    """Display glossary matches as a numbered text list."""
    if not matches:
        print("No matching math terms found.")
        return

    print("\nSearch results")
    print("=" * 14)
    for index, (term, description) in enumerate(matches, start=1):
        print(f"\n{index}. {term.title()}")
        print(f"   {description}")


def run_search() -> None:
    query = input("Search math terms or formulas: ")
    matches = search_math(query)
    visualize_search(matches)


def main() -> None:
    print("Smart Calculator")
    while True:
        print("\n1. Calculate")
        print("2. Search math terms and formulas")
        print("3. Solve a linear equation (ax + b = c)")
        print("4. Solve for x from an equation")
        print("Q. Quit")
        choice = input("Choose an option: ").strip().casefold()

        if choice == "1":
            run_calculator()
        elif choice == "2":
            run_search()
        elif choice == "3":
            equation_solver_menu()
        elif choice == "4":
            solve_fox_x()
        elif choice in {"q", "quit", "exit"}:
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, 4, or Q.")


def run_gui() -> None:
    """Launch the calculator's graphical user interface."""
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Smart Calculator")
    root.minsize(420, 340)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    notebook = ttk.Notebook(root, padding=12)
    notebook.grid(row=0, column=0, sticky="nsew")

    calculator_tab = ttk.Frame(notebook, padding=16)
    notebook.add(calculator_tab, text="Calculator")
    calculator_tab.columnconfigure(1, weight=1)

    first_number = tk.StringVar()
    second_number = tk.StringVar()
    operator = tk.StringVar(value="+")
    calculation_result = tk.StringVar(value="Enter an expression.")

    ttk.Label(calculator_tab, text="First number").grid(
        row=0, column=0, sticky="w", padx=(0, 10), pady=6
    )
    ttk.Entry(calculator_tab, textvariable=first_number).grid(
        row=0, column=1, sticky="ew", pady=6
    )
    ttk.Label(calculator_tab, text="Operator").grid(
        row=1, column=0, sticky="w", padx=(0, 10), pady=6
    )
    ttk.Combobox(
        calculator_tab,
        textvariable=operator,
        values=("+", "-", "*", "/", "**", "%"),
        state="readonly",
        width=8,
    ).grid(row=1, column=1, sticky="w", pady=6)
    ttk.Label(calculator_tab, text="Second number").grid(
        row=2, column=0, sticky="w", padx=(0, 10), pady=6
    )
    ttk.Entry(calculator_tab, textvariable=second_number).grid(
        row=2, column=1, sticky="ew", pady=6
    )

    def calculate_from_form() -> None:
        try:
            result = calculate(
                float(first_number.get()),
                operator.get(),
                float(second_number.get()),
            )
        except (ValueError, OverflowError) as error:
            calculation_result.set(f"Error: {error}")
            return
        calculation_result.set(f"Result: {result:g}")

    ttk.Button(
        calculator_tab, text="Calculate", command=calculate_from_form
    ).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12, 8))
    ttk.Label(calculator_tab, textvariable=calculation_result).grid(
        row=4, column=0, columnspan=2, sticky="w", pady=6
    )

    equation_tab = ttk.Frame(notebook, padding=16)
    notebook.add(equation_tab, text="Solve for x")
    equation_tab.columnconfigure(0, weight=1)
    ttk.Label(
        equation_tab,
        text="Enter a linear equation, for example: 2x + 3 = 11",
    ).grid(row=0, column=0, sticky="w", pady=(0, 8))
    equation = tk.StringVar()
    ttk.Entry(equation_tab, textvariable=equation).grid(
        row=1, column=0, sticky="ew", pady=6
    )
    equation_result = tk.StringVar(value="Enter an equation to solve.")

    def solve_from_form() -> None:
        try:
            equation_result.set(solve_linear_equation(equation.get()))
        except ValueError as error:
            equation_result.set(f"Error: {error}")

    ttk.Button(equation_tab, text="Solve", command=solve_from_form).grid(
        row=2, column=0, sticky="ew", pady=(8, 12)
    )
    ttk.Label(
        equation_tab, textvariable=equation_result, wraplength=360
    ).grid(row=3, column=0, sticky="w")

    search_tab = ttk.Frame(notebook, padding=16)
    notebook.add(search_tab, text="Search math")
    search_tab.columnconfigure(0, weight=1)
    search_tab.rowconfigure(2, weight=1)
    ttk.Label(search_tab, text="Search math terms and formulas").grid(
        row=0, column=0, sticky="w", pady=(0, 8)
    )
    query = tk.StringVar()
    search_entry = ttk.Entry(search_tab, textvariable=query)
    search_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))
    search_results = tk.Text(search_tab, height=10, wrap="word", state="disabled")
    search_results.grid(row=2, column=0, sticky="nsew")
    search_scrollbar = ttk.Scrollbar(
        search_tab, orient="vertical", command=search_results.yview
    )
    search_scrollbar.grid(row=2, column=1, sticky="ns")
    search_results.configure(yscrollcommand=search_scrollbar.set)

    def search_from_form(_event=None) -> None:
        matches = search_math(query.get())
        if matches:
            result_text = "\n\n".join(
                f"{term.title()}\n{description}" for term, description in matches
            )
        else:
            result_text = "No matching math terms found."
        search_results.configure(state="normal")
        search_results.delete("1.0", "end")
        search_results.insert("1.0", result_text)
        search_results.configure(state="disabled")

    ttk.Button(search_tab, text="Search", command=search_from_form).grid(
        row=3, column=0, sticky="ew", pady=(8, 0)
    )
    search_entry.bind("<Return>", search_from_form)

    root.mainloop()


if __name__ == "__main__":
    if "--cli" in sys.argv[1:]:
        main()
    else:
        run_gui()
