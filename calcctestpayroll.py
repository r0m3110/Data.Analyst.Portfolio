from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical")

        # Result Widget
        self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=35)
        main_layout.add_widget(self.solution)

        # Payroll Widgets
        payroll_layout = BoxLayout(orientation="horizontal")
        loan_amount_input = TextInput(multiline=False, hint_text="Loan Amount", input_type="number", font_size=25)
        interest_rate_input = TextInput(multiline=False, hint_text="Interest Rate", input_type="number", font_size=25)
        loan_term_input = TextInput(multiline=False, hint_text="Loan Term", input_type="number", font_size=25)
        
        # Bolder "Calculate" button
        calculate_button = Button(text="Calculate", pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=25, bold=True)
        calculate_button.bind(on_press=self.on_payroll_calculation)

        payroll_layout.add_widget(loan_amount_input)
        payroll_layout.add_widget(interest_rate_input)
        payroll_layout.add_widget(loan_term_input)
        payroll_layout.add_widget(calculate_button)
        main_layout.add_widget(payroll_layout)

        # Calculator Buttons
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=25)
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        # Equals Button
        equals_button = Button(text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}, font_size=25)
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        try:
            if text:
                solution = str(eval(text))
                self.solution.text = solution
        except (SyntaxError, NameError, TypeError, ZeroDivisionError, ValueError) as e:
            print(f"Error: {e}")
            self.solution.text = "Invalid expression. Please enter a valid mathematical expression."

    def on_payroll_calculation(self, instance):
        try:
            loan_amount_str = self.root.children[1].children[0].text
            interest_rate_str = self.root.children[1].children[1].text
            loan_term_str = self.root.children[1].children[2].text

            print(f"Loan Amount String: {loan_amount_str}")
            print(f"Interest Rate String: {interest_rate_str}")
            print(f"Loan Term String: {loan_term_str}")

            if not loan_amount_str or not interest_rate_str or not loan_term_str:
                raise ValueError("Please enter values for all fields.")

            loan_amount = float(loan_amount_str)
            interest_rate = float(interest_rate_str) / 100  # Convert to decimal
            loan_term = float(loan_term_str) * 12  # Convert years to months

            # Your actual payroll calculation logic here
            monthly_interest_rate = interest_rate / 12
            monthly_payment = (monthly_interest_rate * loan_amount) / (1 - (1 + monthly_interest_rate) ** -loan_term)

            # Display the result in the result widget
            result = f"Monthly Payment: {monthly_payment:.2f}"
            self.solution.text = result
        except ValueError as e:
            print(f"Error: {e}")
            self.solution.text = f"Invalid input. {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.solution.text = "An unexpected error occurred. Please check your input."

if __name__ == "__main__":
    app = MainApp()
    app.run()
