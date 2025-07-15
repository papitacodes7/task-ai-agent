import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# --------------------------------------------------------------------
# Load environment variables from the .env file
# --------------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

# Check if the API key is available
if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)  # Exit if no key found

# Initialize OpenAI client with API key
client = OpenAI(api_key=API_KEY)

# --------------------------------------------------------------------
# Function to read tasks from a file
# --------------------------------------------------------------------
def read_tasks(filepath: str) -> str:
    """Reads task content from a given file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read().strip()  # Remove leading/trailing whitespace
    except FileNotFoundError:
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR reading file: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Function to interactively edit the task file
# --------------------------------------------------------------------
def edit_tasks(filepath: str) -> str:
    """Allows the user to edit tasks interactively via console."""
    try:
        # Read current tasks from the file
        with open(filepath, 'r', encoding='utf-8') as f:
            current_tasks = f.read().strip()

        print("Current tasks:")
        print(current_tasks if current_tasks else "No tasks available.")

        print("\nEnter your edited tasks (press Enter then Ctrl+Z to finish):")
        edited_tasks = []

        # Continuously read input until EOF (Ctrl+Z)
        while True:
            try:
                line = input()
                edited_tasks.append(line)
            except EOFError:
                break

        # Join all lines into one string
        edited_tasks_content = '\n'.join(edited_tasks)

        # Overwrite the original file with edited content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(edited_tasks_content)

        return edited_tasks_content
    except Exception as e:
        print(f"❌ ERROR editing file: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Function to summarize tasks using OpenAI
# --------------------------------------------------------------------
def summarize_tasks(tasks: str) -> str:
    """Uses OpenAI to categorize tasks into priority buckets."""
    
    # Prompt sent to the AI
    prompt = f"""
You are a smart and efficient task planning assistant.
Given the following list of tasks, organize them into three priority categories:
- High Priority
- Medium Priority
- Low Priority
Only include each task once. Respond strictly in this format:
High Priority:
- Task 1
- Task 2
Medium Priority:
- Task 1
- Task 2
Low Priority:
...
Here are the tasks:
{tasks}
""".strip()

    try:
        # Call OpenAI's chat completion API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # You can also use "gpt-3.5-turbo" if needed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # Lower temperature for more consistent output
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        print(f"❌ OpenAI API Error: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Main script logic
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Get task file path from command-line argument or default to 'tasks.txt'
    filepath = sys.argv[1] if len(sys.argv) > 1 else "tasks.txt"

    # Read task contents from file
    task_text = read_tasks(filepath)

    # If the file is empty, offer to add new tasks
    if not task_text:
        print("⚠️ The tasks file is empty.")
        edit_choice = input("Do you want to add tasks to the file? (yes/no): ").strip().lower()
        if edit_choice in ('yes', 'y'):
            print("✏️ Adding tasks...")
            task_text = edit_tasks(filepath)
            if not task_text.strip():
                print("No tasks added. Exiting.")
                sys.exit(0)
        else:
            print("No tasks to summarize. Exiting.")
            sys.exit(0)

    # Ask if the user wants to edit the existing file
    edit_choice = input("Do you want to edit the tasks file? (yes/no): ").strip().lower()
    if edit_choice in ('yes', 'y'):
        # Let user edit the file and get updated task list
        task_text = edit_tasks(filepath)

    # Call the summarizer
    print("\n📋 Task Summary")
    print("-" * 40)
    print(summarize_tasks(task_text))
    print("\n✅ Task summary completed successfully.")
    print("You can find the updated tasks in:", filepath)
