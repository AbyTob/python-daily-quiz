# python-daily-quiz

A Python-based quiz generator that creates daily advanced Python programming questions using Ollama's AI models. The project automatically generates, categorizes, and stores quiz questions in multiple formats (JSON, CSV, and Markdown) for easy access and review.

## Features

📚 **Comprehensive Topic Coverage**: Our quiz generator creates questions that dive deep into advanced Python concepts. From metaclasses and class decoration to asyncio and coroutines, the questions cover a wide range of topics including context managers, memory management, advanced generators, threading, and performance optimization. Each question is designed to challenge and enhance your understanding of Python's more complex features.

💾 **Multiple Output Formats**: To ensure maximum accessibility and usability, questions are saved in three different formats. The JSON format provides structured data for programmatic access, CSV format enables easy spreadsheet integration, and Markdown format offers a clean, readable presentation of questions and answers.

📊 **Metadata Tracking**: Every generated question comes with comprehensive metadata. This includes a unique identifier, precise generation timestamp, topic categorization, and complete question-answer content. This rich metadata makes it easy to track, organize, and analyze the quiz content over time.

🏷️ **Automated Categorization**: The system automatically analyzes and categorizes each question based on its content. This intelligent categorization helps in organizing questions by topic and difficulty level, making it easier to find relevant content for specific learning needs.

📝 **Logging**: The project maintains detailed logs of all operations, providing transparency and traceability. This comprehensive logging system helps in monitoring the quiz generation process and troubleshooting any issues that might arise.

## Project Structure

- `src/app.py`: Main application file containing the quiz generation logic
- `resources/`: Directory containing generated questions and metadata
  - `python_quiz.json`: JSON format questions
  - `python_quiz.csv`: CSV format questions
  - `metadata_info.csv`: Question metadata
  - `questions/`: Directory containing individual question markdown files

## Makefile Usage

The project includes a Makefile for easy setup and execution. Here are the available commands:

### Setup and Configuration

```bash
# Check and setup Ollama and required models
make check_and_setup_ollama

# Run the quiz generator
make run_quiz_generator

# Complete setup and run (includes git push)
make setup_and_run
```

### Environment Variables

The Makefile uses the following environment variables:
- `QUIZ_PROJECT_DIR`: Path to the project directory
- `OLLAMA_VENV_DIR`: Path to the virtual environment directory
- `SELECTED_MODEL`: Ollama model to use (default: qwen2.5-coder:7b-instruct)

### Available Models

The project is compatible with any model available on [Ollama's model library](https://ollama.com/search). 
While the default configuration uses the `qwen2.5-coder:7b-instruct` model, you can use any model that suits your needs. 

To use a different model, simply set the `SELECTED_MODEL` environment variable to your preferred model name. For example:
```bash
export SELECTED_MODEL=codellama:7b
```

### Makefile

The Makefile serves as an automation tool for setting up and running the app. It handles:

1. **Ollama Setup and Model Management**:
   - The `check_and_setup_ollama` target verifies Ollama installation and installs it if missing
   - It manages multiple AI models, automatically pulling them if not present
   - The service is restarted to ensure proper functionality

2. **Python Environment Management**:
   - Creates and manages a Python virtual environment (default Python 3.11)
   - Installs required dependencies from requirements.txt
   - Handles environment activation and deactivation

3. **Project Execution**:
   - The `run_quiz_generator` target handles the core functionality
   - Sets up the environment and runs the quiz generation script
   - Manages environment variables for model selection

4. **Automated Workflow**:
   - The `setup_and_run` target provides a complete workflow
   - Combines setup, execution, and git operations
   - Ensures proper sequencing of operations

5. **Configuration Management**:
   - Uses environment variables for flexible configuration
   - Supports different model selections
   - Allows customization of project and virtual environment paths

The Makefile ensures consistent setup across different environments and simplifies the deployment process. 
The automation of these tasks reduces the chance of human error and makes the project more maintainable.

### Set-up crontab

```bash
chmod +x cronjob.sh
```

```cron
# m h  dom mon dow   command
0 */8 * * * bash /<your_path>/cronjob.sh >> /<your_path>/cronlog.log 2>&1

```