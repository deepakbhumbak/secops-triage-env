# Use a lightweight Python version
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy all your files into the container
COPY . /app

# Install the required libraries
RUN pip install gymnasium pydantic openai

# Tell it to run your baseline script when it starts
CMD ["python", "baseline.py"]