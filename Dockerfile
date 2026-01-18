FROM python:3.11-slim

WORKDIR /app

COPY . .

# Set the homepage to the arcade game by renaming it to index.html
RUN mv FrenchArcade.html index.html

# Run a simple python server on the port provided by Railway (or 8000 default)
CMD ["sh", "-c", "python -m http.server ${PORT:-8000}"]
