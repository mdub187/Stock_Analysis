FROM python:3.13
WORKDIR ./.venv/bin/python3.13

# Install the application dependencies
# COPY requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY /upgrade/main.py ./.github/workflows
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
