# Use an official Python image as a base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# --- THIS IS THE CRUCIAL STEP ---
# Install the system-level libraries that WeasyPrint needs
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    --no-install-recommends

# Copy the Python requirements file
COPY requirements.txt .

# Install the Python dependencies (Flask and WeasyPrint)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Tell Docker that the container listens on port 8080
EXPOSE 8080

# The command to run your Flask application
CMD ["python", "simple_pdf_app.py"]
