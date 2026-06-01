.PHONY: install backend frontend test lint demo

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && uvicorn main:app --reload

frontend:
	cd frontend && npm run dev

test:
	cd backend && PYTHONPATH=. pytest -v

lint:
	cd frontend && npm run lint

demo:
	echo "Run 'make backend' in one terminal and 'make frontend' in another."
