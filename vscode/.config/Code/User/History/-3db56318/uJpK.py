def calculator():
    print("--- Basic Interactive Calculator ---")
    print("Enter calculations like: 5 + 3 or 10 - 4 = 6\n")
    print("Supported operations: + (add), - (subtract), * (multiply), / (divide)")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            expression = input("Enter a calculation (e.g., 5 + 3): ").strip()

            if not expression:
                continue

            if expression.lower() in ['quit', 'exit', 'q']:
                print("Thank you for using the calculator!")
                break

            # Check for division by zero before evaluation
            if '/' in expression:
                parts = expression.split('=')
                if len(parts) == 2:
                    divisor_str = parts[1]
                    try:
                        divisor = float(divisor_str.strip())
                        if divisor == 0:
                            print("Error: Division by zero is not allowed!")
                            continue
                    except ValueError:
                        pass  # Let Python handle the division error

            # Evaluate expression safely
            result = eval(expression)

            # Format output cleanly (show decimal only when needed)
            if isinstance(result, float):
                print(f"Result: {result:.2f}")
            else:
                print(f"Result: {result}")
                continue

        except ZeroDivisionError:
            print("Error: Division by zero is not allowed!")
            continue
        except SyntaxError:
            print("Error: Invalid expression (e.g., missing = for complex expressions)")
            continue
        except Exception as e:
            print(f"Error: {type(e).__name__} - Please try again")
            continue

if __name__ == "__main__":
    calculator()