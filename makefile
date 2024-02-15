install:
	echo "Installing..."
	pip install -U pip && \
	pip install -r requirements.txt
run:
	uvicorn app.main:app --reload