
# Member Names: Jarcel Franz, Ivan Cuyos, Axell Senagan, Paul Sanoria

def get_user_input():
    """Get user input and handle invalid input errors."""
    try:
        
        user_input = int(input("Please enter a number: "))
        return user_input
    except ValueError:
        
        print("Error: Invalid input. Please enter a valid integer.")
        return None

def divide_numbers():
    """Divide two numbers with error handling for division by zero."""
    try:
        
        numerator = float(input("Enter numerator: "))
        denominator = float(input("Enter denominator: "))
        
        
        result = numerator / denominator
        return result
    except ZeroDivisionError:
        
        print("Error: Cannot divide by zero. Please enter a non-zero denominator.")
        return None
    except ValueError:
        
        print("Error: Invalid input. Please enter valid numbers.")
        return None

def api_request():
    """Simulate an API request and handle errors."""
    try:
        
        response = {"status": "success", "data": [1, 2, 3]}  
        if response["status"] != "success":
            raise Exception("API request failed")
        return response["data"]
    except Exception as e:
        # Handle general errors
        print(f"Error: {e}")
        return None


def main():
    
    user_number = get_user_input()
    if user_number is not None:
        print(f"You entered the number: {user_number}")
    
    
    division_result = divide_numbers()
    if division_result is not None:
        print(f"Division result: {division_result}")
    

    api_data = api_request()
    if api_data is not None:
        print(f"API data: {api_data}")
    
if __name__ == "__main__":
    main()
