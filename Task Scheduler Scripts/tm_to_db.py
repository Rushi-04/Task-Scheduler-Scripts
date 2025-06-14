#Akshay sir ni dilela code --> status:- Not Working
import subprocess

def get_all_scheduled_tasks():
    try:
        # Run the schtasks command
        result = subprocess.run(['schtasks', '/query', '/fo', 'csv', '/v'], capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            # Optional: You can parse CSV using Python's csv module
            return output
        else:
            print("Error:", result.stderr)
            return None
    except Exception as e:
        print("Exception occurred:", str(e))
        return None

# Example usage
tasks = get_all_scheduled_tasks()
if tasks:
    print(tasks)
    
