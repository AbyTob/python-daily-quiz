import os
import ollama
import csv
import json
import logging
from datetime import datetime
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('quiz_generator.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def generate_response_ollama(user_prompt):
    model = os.environ.get("SELECTED_MODEL", "")
    logger.info(f"model used: {model}")
    response = ollama.chat(
        model=model,
        messages=[
            {
                'role': 'system',
                'content': """You are an expert Python instructor who creates challenging quiz questions. 
                Each question should:
                - Focus on advanced Python concepts (decorators, metaclasses, async/await, etc.)
                - Include code examples where relevant
                - Have a clear correct answer
                - Test deep understanding rather than superficial knowledge
                Format your response in two distinct parts separated by '[ANSWER_SEPARATOR]':
                Part 1 (Question): The question text and code example if any, followed by options A through D
                Part 2 (Answer): The correct answer letter followed by the detailed explanation"""
            },
            {'role': 'user', 'content': user_prompt}
        ])
    return response['message']['content']


def generate_quiz_question():
    prompt = """Generate an advanced Python quiz question. Topics can include but are not limited to:
    - Metaclasses and class decoration
    - Asyncio and coroutines
    - Context managers and descriptors
    - Memory management and garbage collection
    - Advanced generators and iterators
    - Threading and multiprocessing
    - Performance optimization
    Make sure to split your response into question and answer parts using [ANSWER_SEPARATOR]."""
    response = generate_response_ollama(prompt)

    # Split the response into question and answer parts
    parts = response.split('[ANSWER_SEPARATOR]')
    if len(parts) != 2:
        # If separator not found, make a reasonable split at "Correct Answer"
        parts = response.split("Correct Answer:", 1)
        if len(parts) != 2:
            return response.strip(), "Answer format error. Please check the generated content."

    return parts[0].strip(), parts[1].strip()


def extract_topic(question):
    """Extract the main topic from the question text with detailed categorization."""
    topics = {
        # Advanced OOP and Metaprogramming
        "metaclasses": "Python Metaclasses and Class Creation",
        "class decoration": "Class Decorators and Class Modification",
        "descriptors": "Python Descriptors and Attribute Access",
        "inheritance": "Advanced Class Inheritance and Method Resolution",
        "dunder methods": "Special Methods (Dunder Methods) and Operator Overloading",
        "abstract base": "Abstract Base Classes and Interface Definition",
        "multiple inheritance": "Multiple Inheritance and Method Resolution Order",
        "property": "Property Decorators and Attribute Management",
        "classmethod": "Class Methods and Static Methods",
        "singleton": "Singleton Pattern and Class Instantiation Control",
        
        # Advanced Asynchronous Programming
        "asyncio": "Asynchronous Programming with asyncio",
        "coroutines": "Coroutines and Cooperative Multitasking",
        "future": "Futures and Promise-like Objects",
        "task": "Task Management and Scheduling",
        "event loop": "Event Loop Implementation and Control",
        "async context": "Asynchronous Context Managers",
        "async iterator": "Asynchronous Iterators and Generators",
        
        # Advanced Concurrency
        "threading": "Threading and Concurrent Execution",
        "multiprocessing": "Multiprocessing and Parallel Computing",
        "guild": "Guild (Green Threads) and Cooperative Multitasking",
        "queue": "Thread-safe Queues and Communication",
        "lock": "Locks, Semaphores, and Synchronization",
        "deadlock": "Deadlock Prevention and Detection",
        "race condition": "Race Conditions and Thread Safety",
        
        # Advanced Memory Management
        "memory management": "Memory Management and Object Lifecycle",
        "garbage collection": "Garbage Collection and Reference Counting",
        "weakref": "Weak References and Object Finalization",
        "memoryview": "Memory Views and Buffer Protocol",
        "slots": "__slots__ and Memory Optimization",
        
        # Advanced Functional Programming
        "decorators": "Function and Method Decorators",
        "closures": "Closures and Nested Functions",
        "lambda": "Lambda Functions and Anonymous Functions",
        "map": "Map, Filter, and Reduce Operations",
        "functools": "Functional Programming Utilities",
        "partial": "Partial Function Application",
        "compose": "Function Composition and Currying",
        
        # Advanced Type System
        "type hints": "Type Hints and Static Type Checking",
        "typing": "Advanced Type Annotations",
        "protocol": "Protocol Classes and Structural Subtyping",
        "generic": "Generic Types and Type Variables",
        "union": "Union Types and Type Narrowing",
        "literal": "Literal Types and Value Constraints",
        
        # Advanced Data Structures
        "dataclasses": "Data Classes and Object Serialization",
        "namedtuple": "Named Tuples and Immutable Data",
        "enum": "Enumerations and Symbolic Constants",
        "collections": "Advanced Collection Types",
        "defaultdict": "Default Dictionary and Missing Keys",
        "counter": "Counter Objects and Frequency Analysis",
        
        # Advanced Module System
        "import system": "Python Import System and Module Loading",
        "importlib": "Dynamic Module Importing",
        "sys.path": "Python Path Management",
        "package": "Package Structure and Distribution",
        "virtual environments": "Virtual Environments and Dependency Management",
        
        # Advanced Error Handling
        "exceptions": "Exception Handling and Custom Exceptions",
        "contextlib": "Context Management Utilities",
        "traceback": "Stack Traces and Error Reporting",
        "logging": "Advanced Logging Configuration",
        
        # Advanced Performance
        "performance optimization": "Performance Optimization and Profiling",
        "cython": "Cython and Performance Extensions",
        "jit": "Just-In-Time Compilation",
        "profiling": "Code Profiling and Optimization",
        "memory profiling": "Memory Usage Profiling",
        
        # Advanced I/O and Serialization
        "pickle": "Object Serialization with Pickle",
        "json": "JSON Serialization and Deserialization",
        "yaml": "YAML Configuration and Serialization",
        "csv": "CSV File Handling",
        "sqlite": "SQLite Database Integration",
        
        # Advanced Testing
        "unittest": "Unit Testing Framework",
        "pytest": "Pytest Testing Framework",
        "mock": "Mock Objects and Testing",
        "fixture": "Test Fixtures and Setup",
        "coverage": "Code Coverage Analysis",
        
        # Advanced Security
        "security": "Python Security Best Practices",
        "cryptography": "Cryptographic Operations",
        "ssl": "SSL/TLS and Secure Communication",
        "authentication": "Authentication and Authorization"
    }
    
    question_lower = question.lower()
    for keyword, topic in topics.items():
        if keyword in question_lower:
            return topic
            
    # If no specific topic is found, try to identify broader categories
    if any(word in question_lower for word in ["async", "await", "future", "task"]):
        return "Asynchronous Programming Concepts"
    elif any(word in question_lower for word in ["class", "object", "instance"]):
        return "Object-Oriented Programming"
    elif any(word in question_lower for word in ["function", "def", "lambda"]):
        return "Functions and Functional Programming"
    elif any(word in question_lower for word in ["import", "module", "package"]):
        return "Module System and Package Management"
    elif any(word in question_lower for word in ["error", "exception", "try", "except"]):
        return "Error Handling and Exceptions"
    elif any(word in question_lower for word in ["test", "assert", "coverage"]):
        return "Testing and Quality Assurance"
    elif any(word in question_lower for word in ["thread", "process", "concurrent"]):
        return "Concurrency and Parallel Computing"
    elif any(word in question_lower for word in ["memory", "gc", "reference"]):
        return "Memory Management and Optimization"
    
    return "Advanced Python Programming"

def save_metadata(question_id, generation_time, topic):
    """Save question metadata to a CSV file."""
    os.makedirs('resources', exist_ok=True)
    file_path = os.path.join('resources', 'metadata_info.csv')
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
        
        if not file_exists:
            writer.writerow(['question_id', 'generation_time', 'topic'])
        
        writer.writerow([question_id, generation_time, topic])
        logger.info(f"Metadata saved for question {question_id}")

def save_quiz_to_json(question, answer):
    os.makedirs('resources', exist_ok=True)
    file_path = os.path.join('resources', 'python_quiz.json')

    current_datetime = datetime.now().strftime("%Y-%m-%d")

    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            quiz_data = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        quiz_data = {}

    today_questions = [k for k in quiz_data.keys() if k.split('_')[1] == current_datetime]
    next_index = len(today_questions) + 1

    key = f"q{next_index}_{current_datetime}"
    unique_id = f"{int(datetime.now().timestamp())}_{next_index}"
    
    topic = extract_topic(question)

    quiz_data[key] = {
        "id": unique_id,
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic
    }

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)
        
    # Save metadata
    save_metadata(unique_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), topic)


def save_quiz_to_csv(question, answer):
    os.makedirs('resources', exist_ok=True)
    file_path = os.path.join('resources', 'python_quiz.csv')

    file_exists = os.path.isfile(file_path)

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        if not file_exists:
            writer.writerow(['datetime', 'question', 'answer'])  # Write header if file doesn't exist

        writer.writerow([current_datetime, question, answer])


def read_quiz_from_json(date=None):
    file_path = os.path.join('resources', 'python_quiz.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            quiz_data = json.load(jsonfile)

        if date:
            date_questions = {k: v for k, v in quiz_data.items() if date in k}
            return date_questions
        return quiz_data

    except FileNotFoundError:
        logger.warning("No quiz data found.")
        return {}
    except json.JSONDecodeError:
        logger.error("Error reading quiz data.")
        return {}


def save_quiz_to_markdown(question, answer, question_id):
    """Save quiz question and answer as a markdown file."""
    os.makedirs('resources/questions', exist_ok=True)
    file_path = os.path.join('resources/questions', f'{question_id}.md')
    
    # Format the markdown content
    markdown_content = f"""# Python Quiz Question

## Question
{question}

## Answer
{answer}

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    
    with open(file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(markdown_content)
    logger.info(f"Markdown file saved: {file_path}")


def main():
    try:
        question, answer = generate_quiz_question()
        logger.info("\nGenerated Python Quiz Question:")
        logger.info("-" * 50)
        logger.info("Question:")
        logger.info(question)
        logger.info("\nAnswer:")
        logger.info(answer)
        logger.info("-" * 50)

        # Generate a unique ID using timestamp and index
        current_datetime = datetime.now().strftime("%Y-%m-%d")
        timestamp = int(datetime.now().timestamp())
        
        # Find the next index for today's date
        quiz_data = read_quiz_from_json()
        today_questions = [k for k in quiz_data.keys() if k.split('_')[1] == current_datetime]
        next_index = len(today_questions) + 1
        
        # Create the unique ID in the same format as used in JSON
        unique_id = f"{timestamp}_{next_index}"

        # Save to all formats
        save_quiz_to_csv(question, answer)
        save_quiz_to_json(question, answer)
        save_quiz_to_markdown(question, answer, unique_id)

        logger.info("Quiz question saved to resources/python_quiz.csv and resources/python_quiz.json")
        logger.info("Metadata saved to resources/metadata_info.csv")
        logger.info(f"Markdown file saved to resources/questions/{unique_id}.md")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
