install:
	echo "Installing..."
	pip install -U pip && \
	pip install -r requirements.txt
run:
	uvicorn main:app --reload