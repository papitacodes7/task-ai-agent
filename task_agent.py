import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# --------------------------------------------------------------------
# Load environment variables from a .env file
# --------------------------------------------------------------------
# This loads any key=value pairs from .env into the environment
load_dotenv()
# Retrieve the OpenAI API key from environment variables
API_KEY = os.getenv("OPENAI_API_KEY")

# If the API key is missing, inform the user and exit
if not API_KEY:
    print("❌ ERROR: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=API_KEY)

# --------------------------------------------------------------------
# Function: read_tasks
# --------------------------------------------------------------------
# Reads the entire contents of the task file and returns a stripped string.
def read_tasks(filepath: str) -> str:
    """Reads and returns the content of the specified tasks file as a single string."""
    try:
        # Open the file in read mode with UTF-8 encoding
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read all text and strip leading/trailing whitespace/newlines
            return f.read().strip()
    except FileNotFoundError:
        # If the file does not exist, notify and exit
        print(f"❌ ERROR: File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        # Catch any other I/O errors and exit
        print(f"❌ ERROR reading file: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Function: edit_tasks
# --------------------------------------------------------------------
# Allows the user to view current tasks and overwrite the file with new input.
def edit_tasks(filepath: str) -> str:
    """Prompts the user to edit all tasks interactively and saves to file."""
    try:
        # Read current content for display
        with open(filepath, 'r', encoding='utf-8') as f:
            current_tasks = f.read().strip()

        # Display existing tasks or a placeholder if none
        print("\n📋 Current tasks:")
        print(current_tasks if current_tasks else "No tasks available.")

        # Prompt user to enter replacement content until EOF (Ctrl+Z or Ctrl+D)
        print("\n✏️ Enter your edited tasks (press Enter then Ctrl+Z to finish):")
        edited_tasks = []
        while True:
            try:
                # Read a line of input
                line = input()
                edited_tasks.append(line)
            except EOFError:
                # Stop reading when EOF is signaled
                break

        # Join all entered lines into a single text block
        edited_tasks_content = '\n'.join(edited_tasks)

        # Overwrite the original file with the new content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(edited_tasks_content)

        # Return the updated content for further processing
        return edited_tasks_content
    except Exception as e:
        # Handle any unexpected errors during editing
        print(f"❌ ERROR editing file: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Function: append_task
# --------------------------------------------------------------------
# Lets the user add a single new task to the end of the file without losing existing ones.
def append_task(filepath: str) -> None:
    """Prompts for a single new task and appends it to the tasks file."""
    try:
        # Ask the user for the new task text
        new_task = input("➕ Enter the task you want to append: ").strip()
        if new_task:
            # Open the file in append mode and add the new task on a new line
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write('\n' + new_task)
            print("✅ Task appended successfully.")
        else:
            # If input was empty, notify and skip appending
            print("⚠️ No task entered. Skipping append.")
    except Exception as e:
        # Handle any errors during file append
        print(f"❌ ERROR appending task: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Function: summarize_tasks
# --------------------------------------------------------------------
# Uses the OpenAI API to organize tasks into priority categories.
def summarize_tasks(tasks: str) -> str:
    """Sends the list of tasks to OpenAI and returns a categorized summary."""
    # Build the prompt to instruct the model for desired formatting
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
        # Call the chat completion endpoint with a low temperature for consistency
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        # Return the assistant's reply (priority-organized list)
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        # Handle API errors gracefully
        print(f"❌ OpenAI API Error: {e}")
        sys.exit(1)

# --------------------------------------------------------------------
# Main script execution
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Determine the file path (default to 'tasks.txt' if not provided)
    filepath = sys.argv[1] if len(sys.argv) > 1 else "tasks.txt"
    # Read existing tasks (empty string if file empty)
    task_text = read_tasks(filepath)

    # Display current tasks or indicate an empty file
    print("📂 Current tasks in the file:")
    print("-" * 40)
    if task_text:
        print(task_text)
    else:
        print("⚠️ The tasks file is empty.")

    # Branch logic when file has no tasks
    if not task_text:
        edit_choice = input("Do you want to add tasks to the file? (yes/no): ").strip().lower()
        if edit_choice in ('yes', 'y'):
            print("✏️ Adding tasks...")
            task_text = edit_tasks(filepath)
            if not task_text.strip():
                print("⚠️ No tasks added. Exiting.")
                sys.exit(0)
        else:
            print("🚫 No tasks to summarize. Exiting.")
            sys.exit(0)
    else:
        # If tasks exist, offer options: append, edit, or continue
        print("\nWhat would you like to do?")
        print("1. Append a new task")
        print("2. Edit all tasks")
        print("3. Continue with current tasks")
        user_choice = input("Enter choice (1/2/3): ").strip()

        if user_choice == '1':
            append_task(filepath)
            # Refresh the task list from file after appending
            task_text = read_tasks(filepath)
        elif user_choice == '2':
            task_text = edit_tasks(filepath)

    # Finally, summarize and print the tasks
    print("\n📋 Task Summary")
    print("-" * 40)
    print(summarize_tasks(task_text))
    print("\n✅ Task summary completed successfully.")
    print("🗂️  You can find the updated tasks in:", filepath)
