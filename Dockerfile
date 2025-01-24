FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

# Install all autogen-related packages together
COPY autogen-magentic-one ./autogen-magentic-one
RUN cd autogen-magentic-one && pip install -e . && \
    pip install 'autogen-core==0.4.0.dev8' \
    'autogen-agentchat==0.4.0.dev8' \
    'autogen-ext==0.4.0.dev8'

# Install and setup Playwright
RUN pip install playwright && \
    playwright install && \
    playwright install-deps


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code/src

EXPOSE 8000

CMD ["python", "main.py"]