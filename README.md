# README

## Project Overview
**Generative Flow** is an innovative framework for image generation that combines the flexibility of node-based interfaces with the power of Retrieval-Augmented Generation (RAG). Designed to simplify the creation and customization of Stable Diffusion workflows, it features an intelligent chatbot that assists users in retrieving and configuring workflows tailored to their specific needs. Additionally, a built-in web search agent automatically locates and downloads workflows when suitable options are not available in the database. By streamlining workflow selection and setup, **Generative Flow** empowers users—regardless of expertise level—to create high-quality, customized artwork with ease.

## Requirements
- **Docker** (version 20.10 or later)
- **Docker Compose** (version 1.29 or later)

---

## Setup Instructions

### 1. Build and Run the Docker Container

#### Using Docker Compose
```bash
# Start services using docker-compose
docker-compose up -d --build
```

---

## Configuration Details

### Environment Variables
Add your OpenAI and Google AI keys to the .env file:

OPENAI_API_KEY=<your_openai_key>
GOOGLE_AI_KEY=<your_google_ai_key>

### Ports
- **8000**: This port is exposed by the application and is mapped to the same port on the host machine.

---

## Application Structure
```
/code
  ├── autogen-magentic-one/  
  ├── requirements.txt       
  ├── modules/                   
      ├── ...            
  ├── src/                  
      ├── main.py       
      ├── ...   
  ├── ...     
```

---