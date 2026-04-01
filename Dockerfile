# Use a lightweight Python version
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all your files into the container
COPY . /app

# Install the required libraries (+ fastapi and uvicorn)
RUN pip install gymnasium pydantic openai fastapi uvicorn

# Expose the specific port Hugging Face Spaces uses
EXPOSE 7860

# Start the web server so Scaler's grader can talk to it!
# Start the web server from the new folder location!
CMD ["python", "server/app.py"]