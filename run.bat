@echo off
echo Starting AI Interview Chatbot...
start "" "http://localhost:8502"
python -m streamlit run app.py --server.headless true --server.port 8502
pause
