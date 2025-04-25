import gradio as gr
import json
from datetime import datetime
import re


def load_question(json_file_path):
    """Load question from JSON file for the current date."""
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Get today's date in the format used in the JSON
    today = datetime.now().strftime("%Y-%m-%d")

    # Find the question for today
    question_key = f"q1_{today}"
    if question_key in data:
        # Extract the question text from the markdown-style content
        question_text = data[question_key]["question"]
        # Remove markdown formatting and extra whitespace
        question_text = re.sub(r'\*\*', '', question_text)
        return question_text
    return "No question available for today."


def submit_answer(answer):
    """Handle answer submission."""
    if not answer:
        return "Please enter an answer before submitting."
    return f"Answer submitted: {answer}"


# Create the Gradio interface
def create_quiz_interface():
    # Load the initial question
    initial_question = load_question("resources/python_quiz.json")

    with gr.Blocks(theme=gr.themes.Soft()) as quiz_app:
        gr.Markdown("# Daily Programming Quiz")

        with gr.Row():
            question_box = gr.Textbox(
                value=initial_question,
                label="Question",
                interactive=False,
                lines=10
            )

        with gr.Row():
            answer_input = gr.Textbox(
                label="Your Answer",
                placeholder="Type your answer here...",
                lines=5
            )

        with gr.Row():
            submit_btn = gr.Button("Submit Answer")
            clear_btn = gr.Button("Clear")

        response_box = gr.Textbox(label="Response")

        # Handle interactions
        submit_btn.click(
            fn=submit_answer,
            inputs=[answer_input],
            outputs=[response_box]
        )

        clear_btn.click(
            fn=lambda: "",
            inputs=[],
            outputs=[answer_input]
        )

    return quiz_app


# Launch the app
if __name__ == "__main__":
    quiz_app = create_quiz_interface()
    quiz_app.launch()