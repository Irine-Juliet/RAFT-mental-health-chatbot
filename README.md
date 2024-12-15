# RAFT-mental-health-chatbot

A RAG-enhanced conversational support system that combines RAFT (Retrieval Augmented Fine-Tuning) with RAG (Retrieval Augmented Generation) for providing empathetic, evidence-based mental health support responses. Built on LLaMA-2, the system is fine-tuned to effectively distinguish relevant context from distracting information while incorporating expert knowledge from mental health resources.

## Architecture
- **Base Model**: LLaMA-2-7B-chat
- **Fine-tuning**: QLoRA (4-bit quantization with LoRA adapters)
- **Vector Store**: Pinecone with HuggingFace embeddings
- **Frontend**: Streamlit chat interface
- **Backend**: FastAPI server hosted on Google Colab
- **Deployment**: ngrok for server exposure

## Key Components
### RAFT Fine-tuning
- Memory-efficient training using QLoRA
- Trained on the RAFT dataset for context discrimination
- Hyperparameters optimized based on QLoRA paper recommendations

### RAG Implementation
- Source documents: Consolidated guides from mental health experts
- Semantic similarity search using Pinecone vector database
- Real-time context retrieval and response generation

### Interactive Interface
- Clean chat interface built with Streamlit
- Maintains conversation history for contextual responses
- Real-time response generation with thinking indicators

## Setup and Usage
[Installation and setup instructions]

## Evaluation
- Evaluated using Azure AI Studio metrics
- Metrics include groundedness, relevance, and F1 scores
- Comparison with baseline model performance

## Limitations
- Not intended for production deployment
- Should not replace professional mental health services
- Research/demonstration purpose only

## Acknowledgments
- RAFT dataset generation and evaluation scripts from the original RAFT paper's implementation
- Expert source material from established mental health authors
- Built using HuggingFace's transformers library and LangChain
