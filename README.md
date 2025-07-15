# AI Task Management Agent 🤖

A smart Python-based task management tool that uses OpenAI's GPT to automatically categorize and prioritize your tasks. This agent helps you organize your to-do list by intelligently sorting tasks into High, Medium, and Low priority categories.

## ✨ Features

- **AI-Powered Prioritization**: Uses OpenAI GPT-4o-mini to intelligently categorize tasks
- **Interactive Task Management**: Add, edit, and append tasks through an intuitive command-line interface
- **Flexible File Handling**: Read tasks from any text file (defaults to `tasks.txt`)
- **Priority Categorization**: Automatically organizes tasks into three priority levels
- **User-Friendly Interface**: Clean, emoji-rich console output for better user experience
- **Error Handling**: Robust error handling for file operations and API calls

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- OpenAI API key
- Internet connection for API calls

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task_ai_agent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install openai python-dotenv
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key_here
     ```

### 🔧 Configuration

The application requires an OpenAI API key to function. You can obtain one from the [OpenAI Platform](https://platform.openai.com/api-keys).

**Environment Variables:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)

## 📖 Usage

### Basic Usage

```bash
# Run with default tasks.txt file
python task_agent.py

# Run with a custom task file
python task_agent.py my_tasks.txt
```

### Interactive Features

When you run the application, you'll be presented with several options:

1. **View Current Tasks**: See all tasks currently in your file
2. **Add New Task**: Append a single task to your list
3. **Edit All Tasks**: Modify your entire task list interactively
4. **AI Prioritization**: Get your tasks automatically categorized by priority

### Example Workflow

```bash
$ python task_agent.py
📂 Current tasks in the file:
----------------------------------------
Complete project documentation
Buy groceries
Call mom
Prepare for meeting
Clean the house

What would you like to do?
1. Append a new task
2. Edit all tasks
3. Continue with current tasks
Enter choice (1/2/3): 3

📋 Task Summary
----------------------------------------
High Priority:
- Complete project documentation
- Prepare for meeting

Medium Priority:
- Call mom
- Buy groceries

Low Priority:
- Clean the house

✅ Task summary completed successfully.
🗂️  You can find the updated tasks in: tasks.txt
```

## 🏗️ Project Structure

```
task_ai_agent/
├── task_agent.py      # Main application file
├── tasks.txt          # Default tasks file
├── .env              # Environment variables (create this)
├── .gitignore        # Git ignore file
├── README.md         # This file
└── venv/             # Virtual environment
```

## 🛠️ Functions Overview

- `read_tasks(filepath)`: Reads tasks from a specified file
- `edit_tasks(filepath)`: Allows interactive editing of tasks
- `append_task(filepath)`: Appends a single task to the file
- `summarize_tasks(tasks)`: Uses OpenAI to categorize tasks by priority

## 🔒 Security & Privacy

- API keys are loaded from environment variables (not hardcoded)
- The `.env` file is included in `.gitignore` to prevent accidental commits
- Task data is processed by OpenAI's API - ensure you're comfortable with their data usage policies

## 📝 Task File Format

Tasks should be stored in plain text format, one task per line:

```
Complete project documentation
Buy groceries
Call mom
Prepare for meeting
Clean the house
```

## 🚨 Error Handling

The application handles various error scenarios:
- Missing OpenAI API key
- File not found errors
- OpenAI API errors
- Invalid user input

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues or have questions:

1. Check the error messages - they're designed to be helpful
2. Ensure your OpenAI API key is valid and has sufficient credits
3. Verify your internet connection for API calls
4. Check that all dependencies are properly installed


---

**Made with ❤️ and AI assistance**
