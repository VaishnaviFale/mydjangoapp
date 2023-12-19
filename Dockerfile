# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the Django application
EXPOSE 8000

# Define environment variables for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED 1

# Set the STATIC_ROOT environment variable
ENV STATIC_ROOT /app/staticfiles

# Run collectstatic to collect static files
RUN python manage.py collectstatic --noinput

# Install Gunicorn
RUN pip install gunicorn

# Command to run your application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]

