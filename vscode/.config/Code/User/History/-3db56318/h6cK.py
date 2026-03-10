

def calculator():
    print("--- Basic Interactive Calculator ---")
    print("Supported operations: + (add), - (subtract), * (multiply), / (divide)")
    print("Type 'quit' to exit.\n")
    
    while True:
        try:
            # Get user input for the expression
            expression = input("Enter a calculation (e.g., 5 + 3): ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the calculator!")
                break
            
            # Validate the expression
            if not expression or '=' not in expression:
                print("Please enter a valid equation (e.g., 10 + 5 = 15).")
                continue
            
            # Check for division by zero manually before evaluating
            if '/' in expression:
                parts = expression.split('=')
                if len(parts) == 2:
                    dividend, divisor = parts[0].strip(), float(parts[1])
                    if '0' in divisor or divisor == 0:
                        print("Error: Division by zero is not allowed!")
                        continue
            
            # Evaluate the expression safely (avoiding eval() if possible)
            try:
                result = eval(expression, {"__builtins__": {}}, {})
                
                # Check for division errors
                if '/' in expression:
                    dividend_parts = [p.strip() for p in expression.split('/')]
                    if len(dividend_parts) > 1 and int(dividend_parts[1]) == 0:
                        print("Error: Division by zero detected!")
                        continue
                
                # Handle floating-point precision issues
                result = round(result, 2)
                
                # Remove any decimal points from whole numbers for cleaner output
                if isinstance(result, float) and result == int(result):
                    result = int(result)
                
                print(f"Result: {result}\n")
            except ZeroDivisionError:
                print("Error: Division by zero!")
                continue
            
        except Exception as e:
            print(f"Error in expression: {e}")

if __name__ == "__main__":
    calculator()
