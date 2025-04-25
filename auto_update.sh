#/bin/bash

cd /root/Projects/abytob/python-daily-quiz

source ~/venv/ollama-coding-assistant/bin/activate
python ollama_python_quiz_gen.py

git add .
git commit -m "daily push"
git push

