#!/usr/bin/env python3
"""
Advanced Interactive Calculator with History & Help
Features:
- Command history
- Clear error messages
- Multiple input formats
- Division by zero protection
- Display menu options
"""

def show_menu():
    """Display main menu options."""
    print("\n" + "=" * 50)
    print("       🧮 CALCULATOR MENU 🧮")
    print("=" * 50)
    print("Options:")
    print("1. Add numbers (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Calculate expression (e.g., 5 + 3 * 2)")
    print("6. Clear history")
    print("7. Show help")
    print("8. Quit\n")

def get_number(prompt):
    """Get valid number input with retry."""
    while True:
        try:
            user_input = input(f"{prompt} ").strip()
            if not user_input:
                print("\n⚠️  Please enter a valid number.")
                continue
            
            # Handle decimal point variations
            user_input = user_input.replace('.', 'x').replace(',', '.')
            
            return float(user_input.replace('x', '.'))
        except ValueError:
            print("❌ That's not a valid number. Try again.\n")

def get_expression():
    """Get and validate expression from user."""
    while True:
        expr = input("\nEnter calculation (e.g., 5 + 3): ").strip()
        if expr.lower() in ['quit', 'exit', 'q']:
            return None
        
        if not expr or expr.isspace():
            print("⚠️  Please enter something.")
            continue
        
        # Check for allowed characters only
        if not all(c.isalnum() or c in '+-*/=.' for c in expr):
            print("❌ Invalid character detected!")
            continue
        
        return expr

def calculate():
    """Main calculation loop with features."""
    history = []  # Store calculations
    max_history = 5  # Keep last 5 results
    
    print("\n" + "=" * 50)
    print("Welcome to the Interactive Calculator!")
    print("=" * 50)
    
    while True:
        show_menu()
        choice = input("Select option (1-8): ").strip()
        
        if choice == '8':
            print("\n👋 Goodbye! Thanks for using the calculator.")
            break
        
        if choice == '6':
            history.clear()
            print("\n✅ History cleared!\n")
            continue
        
        if choice in ['1', '2', '3', '4']:
            # Direct operations (add, subtract, multiply, divide)
            try:
                num1 = get_number(f"Enter first number for {choice}: ")
                
                if choice == '1':  # Add
                    op_symbol = '+'
                    result = num1 + float(get_number("Enter second number (+): "))
                elif choice == '2':  # Subtract
                    op_symbol = '-'
                    result = num1 - float(get_number("Enter number to subtract (-): "))
                elif choice == '3':  # Multiply
                    op_symbol = '*'
                    result = num1 * float(get_number("Enter second number (*): "))
                elif choice == '4':  # Divide
                    op_symbol = '/'
                    divisor = float(get_number("Enter second number (/): "))
                    if divisor == 0:
                        print("⚠️  Cannot divide by zero!")
                        result = None
                        continue
                    else:
                        result = num1 / divisor
                
                # Show rounded result when needed
                if isinstance(result, float):
                    if abs(result) < 0.0001 or result > 1000000000 or result < -1000000000:
                        print(f"\nResult: {result:.2e}")
                    else:
                        print(f"\nResult: {result}")
                else:
                    print(f"\nResult: {result}\n")
                
                # Store in history
                if result is not None:
                    calc_info = f"{num1} {op_symbol} ..."
                    history.append((calc_info, result))
                
            except ZeroDivisionError:
                print("⚠️  Division by zero is not allowed!")
                continue
        
        elif choice == '5':
            # Full expression parser
            expr = get_expression()
            if not expr:
                continue
            
            try:
                result = eval(expr)
                
                if isinstance(result, float):
                    display_result = f"{result:.2f}" if abs(result) >= 0.01 else f"{int(abs(result))}"
                    print(f"\nResult: {display_result}")
                else:
                    print(f"\nResult: {result}\n")
                
                history.append((expr, result))
                
            except ZeroDivisionError:
                print("⚠️  Division by zero is not allowed!\n")
            
            except Exception as e:
                print(f"❌ Invalid expression: {e}")
        
        elif choice == '7':
            # Help section
            help_text = """
CALCULATOR HELP:

• Supported operations: + (add), - (subtract), * (multiply), / (divide)
• Examples: 5 + 3, 10 - 4, 6 * 7, 20 / 4
• Enter 'quit' to exit anytime.
• Type 'help' at any time to see this message.
• Division by zero is not allowed.

💡 Tips:
- Use numbers with +, -, *, or / between them
- You can use parentheses like (5 + 3) * 2
- Results are shown rounded to 2 decimal places when needed
"""
            print(help_text)
    
    # Show history before exiting
    if history:
        print(f"\n📊 Recent calculations ({len(history)} stored):")
        for i, (info, result) in enumerate(history, 1):
            print(f"  {i}. {info} = {result}")

if __name__ == "__main__":
    try:
        calculate()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Thanks for using the calculator!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {type(e).__name__}: {e}")