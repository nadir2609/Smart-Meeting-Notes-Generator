#!/bin/bash
echo "Starting Smart Meeting Notes Generator..."
echo ""

# Check if virtual environment exists
if [ ! -d "env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv env
    source env/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    source env/bin/activate
fi

echo ""
echo "Starting Backend Server..."
cd backend
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

sleep 3

echo "Starting Frontend..."
cd frontend
streamlit run streamlit_app.py &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  Smart Meeting Notes Generator"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================"

# Trap Ctrl+C and kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
