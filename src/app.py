import os
import ollama
import csv
import json
from datetime import datetime


def generate_response_ollama(user_prompt):
    model = os.environ.get("SELECTED_MODEL", "")
    print(f"model used: {model}")
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


def save_quiz_to_json(question, answer):
    os.makedirs('../resources', exist_ok=True)
    file_path = os.path.join('../resources', 'python_quiz.json')

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d")

    # Load existing data or create new dictionary
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            quiz_data = json.load(jsonfile)
    except (FileNotFoundError, json.JSONDecodeError):
        quiz_data = {}

    # Find the next index for today's date
    today_questions = [k for k in quiz_data.keys() if k.split('_')[1] == current_datetime]
    next_index = len(today_questions) + 1

    # Create unique key combining index and date
    key = f"q{next_index}_{current_datetime}"

    # Add new quiz question
    quiz_data[key] = {
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save updated data
    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(quiz_data, jsonfile, indent=2, ensure_ascii=False)


def save_quiz_to_csv(question, answer):
    os.makedirs('../resources', exist_ok=True)
    file_path = os.path.join('../resources', 'python_quiz.csv')

    file_exists = os.path.isfile(file_path)

    # Get current date and time
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

        if not file_exists:
            writer.writerow(['datetime', 'question', 'answer'])  # Write header if file doesn't exist

        writer.writerow([current_datetime, question, answer])


def read_quiz_from_json(date=None):
    file_path = os.path.join('../resources', 'python_quiz.json')

    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            quiz_data = json.load(jsonfile)

        if date:
            # Filter questions for specific date
            date_questions = {k: v for k, v in quiz_data.items() if date in k}
            return date_questions
        return quiz_data

    except FileNotFoundError:
        print("No quiz data found.")
        return {}
    except json.JSONDecodeError:
        print("Error reading quiz data.")
        return {}


def display_quiz(quiz_data, show_answers=False):
    for key, value in quiz_data.items():
        print(f"\nQuestion {key.split('_')[0]}:")
        print(f"Generated at: {value['timestamp']}")
        print("-" * 30)
        print("Question:")
        print(value['question'])
        if show_answers:
            print("\nAnswer:")
            print(value['answer'])
        print("-" * 50)


def main():
    try:
        question, answer = generate_quiz_question()
        print("\nGenerated Python Quiz Question:")
        print("-" * 50)
        print("Question:")
        print(question)
        print("\nAnswer:")
        print(answer)
        print("-" * 50)

        # Save to both CSV and JSON
        save_quiz_to_csv(question, answer)
        save_quiz_to_json(question, answer)

        print("\nQuiz question saved to resources/python_quiz.csv and resources/python_quiz.json")

        # # Display today's questions
        # today = datetime.now().strftime("%Y-%m-%d")
        # today_questions = read_quiz_from_json(today)
        # if today_questions:
        #     print(f"\nQuestions generated today ({today}):")
        #     display_quiz(today_questions, show_answers=False)
        #
        #     # Ask if user wants to see answers
        #     show_ans = input("\nWould you like to see the answers? (y/n): ").lower().strip()
        #     if show_ans == 'y':
        #         display_quiz(today_questions, show_answers=True)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
