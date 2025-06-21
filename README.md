# 🔬 Doki: RAG-Powered Documentation Chat

Doki is a comprehensive Retrieval-Augmented Generation (RAG) system that allows you to chat with technical documentation. It scrapes documentation websites, processes the content, stores it in a vector database, and provides intelligent answers using a Large Language Model.

## 🚀 Features

- **Web Scraping**: Automated scraping of documentation websites using Scrapy
- **Content Processing**: Intelligent extraction and chunking of documentation content
- **Vector Search**: Semantic search using sentence transformers and ChromaDB
- **RAG Pipeline**: Retrieval-augmented generation with Groq LLM
- **API Interface**: FastAPI backend for programmatic access
- **Web UI**: Beautiful Streamlit interface for interactive chat
- **Real-time Chat**: Maintains conversation history and provides instant responses

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Scraper   │───▶│   Ingestion     │───▶│  Vector Store   │
│   (Scrapy)      │    │   (LangChain)   │    │   (ChromaDB)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │◀───│   FastAPI       │◀───│   RAG Chain     │
│   (Frontend)    │    │   (Backend)     │    │   (LangChain)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **RAG Framework**: LangChain
- **LLM**: Groq (Llama3-8b-8192)
- **Embeddings**: Sentence Transformers (paraphrase-multilingual-MiniLM-L12-v2)
- **Vector Database**: ChromaDB
- **Web Scraping**: Scrapy
- **Content Processing**: BeautifulSoup, lxml
- **Package Management**: Poetry

## 📦 Installation

### Prerequisites

- Python 3.12+
- Poetry
- Groq API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd doki
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```

## 🚀 Quick Start

### 1. Scrape Documentation

First, scrape the documentation you want to chat with:

```bash
# Update the URL in tools/run_scraper.py if needed
poetry run python tools/run_scraper.py
```

This will scrape the RamanSpy documentation and save HTML files to `data/scraped_html/`.

### 2. Ingest Content

Process the scraped content and create the vector database:

```bash
poetry run python tools/run_ingest.py
```

This creates embeddings and stores them in `data/chroma_db/`.

### 3. Start the API

Launch the FastAPI backend:

```bash
poetry run python -m uvicorn doki_api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Start the Streamlit UI

In a new terminal, launch the Streamlit interface:

```bash
poetry run streamlit run streamlit_app.py --server.port 8501
```

### 5. Start Chatting!

Open your browser to `http://localhost:8501` and start asking questions about the documentation!

## 📁 Project Structure

```
doki/
├── data/                          # Data storage
│   ├── scraped_html/             # Scraped HTML files
│   └── chroma_db/                # Vector database
├── scraper/                      # Web scraping components
│   └── scraper/
│       └── docs_spider.py        # Scrapy spider
├── src/doki/                     # Core RAG components
│   ├── chains.py                 # RAG chain creation
│   ├── config.py                 # Configuration
│   ├── ingestion.py              # Content ingestion
│   └── retrieval.py              # Vector retrieval
├── doki_api/                     # FastAPI backend
│   ├── main.py                   # API server
│   └── routes.py                 # API routes
├── tools/                        # Utility scripts
│   ├── run_scraper.py           # Scraping script
│   └── run_ingest.py            # Ingestion script
├── streamlit_app.py              # Streamlit UI
├── pyproject.toml               # Dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Scraping Configuration

Edit `tools/run_scraper.py` to change:
- Target URL
- Output directory
- Crawl depth
- User agent

### RAG Configuration

Edit `src/doki/config.py` to modify:
- Embedding model
- LLM model
- Number of retrieved chunks
- Prompt template

### API Configuration

The API runs on port 8000 by default. Change in `doki_api/main.py` if needed.

## 🎯 Usage Examples

### API Usage

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "How do I load data in RamanSpy?"}
)

answer = response.json()["answer"]
print(answer)
```

### Direct Chain Usage

```python
from src.doki.chains import create_rag_chain

chain = create_rag_chain()
response = chain.invoke({"input": "What preprocessing methods are available?"})
print(response["answer"])
```

## 🔍 Example Questions

Try these questions in the Streamlit UI:

- "How do I load data in RamanSpy?"
- "What preprocessing steps are available?"
- "What denoising methods can I use?"
- "How do I perform baseline correction?"
- "What datasets are included with RamanSpy?"

## 🛠️ Development

### Adding New Documentation Sources

1. Update the URL in `tools/run_scraper.py`
2. Run the scraper: `poetry run python tools/run_scraper.py`
3. Run ingestion: `poetry run python tools/run_ingest.py`
4. Restart the API and UI

### Customizing the RAG Pipeline

- **Embeddings**: Change `EMBEDDING_MODEL_NAME` in `config.py`
- **LLM**: Change `LLM_MODEL_NAME` in `config.py`
- **Prompt**: Modify `PROMPT_TEMPLATE` in `config.py`
- **Retrieval**: Adjust `RETRIEVER_K` in `config.py`

### Extending the API

Add new endpoints in `doki_api/routes.py`:

```python
@router.get("/health")
async def health_check():
    return {"status": "healthy"}
```

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure the uvicorn server is running on port 8000
   - Check that the GROQ_API_KEY is set in your `.env` file

2. **No Data Found**
   - Run the scraper first: `poetry run python tools/run_scraper.py`
   - Then run ingestion: `poetry run python tools/run_ingest.py`

3. **Memory Issues**
   - Reduce `chunk_size` in `ingestion.py`
   - Use a smaller embedding model

4. **Scraping Errors**
   - Check if the target website is accessible
   - Verify the URL in `run_scraper.py`
   - Check robots.txt compliance

### Logs

- **API Logs**: Check the uvicorn console output
- **Scraping Logs**: Check the scraper console output
- **Ingestion Logs**: Check the ingestion console output

## 📊 Performance

- **Scraping**: ~160 HTML files in ~2 minutes
- **Ingestion**: ~1,139 chunks processed in ~2 minutes
- **Query Response**: ~2-5 seconds per question
- **Memory Usage**: ~500MB for embeddings + ~200MB for LLM

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **RamanSpy**: For the excellent documentation
- **LangChain**: For the RAG framework
- **Groq**: For the fast LLM inference
- **ChromaDB**: For the vector database
- **Streamlit**: For the beautiful UI framework

---

**🔬 Happy chatting with your documentation!**
