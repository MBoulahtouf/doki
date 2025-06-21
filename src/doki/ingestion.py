# src/doki/ingestion.py
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from . import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_main_content(soup: BeautifulSoup) -> str:
    # This robust extractor is the same one from our debug script
    selectors = ["article[role='main']", "main", "div.main-content", "div.content", "div.body"]
    content_node = None
    for selector in selectors:
        content_node = soup.select_one(selector)
        if content_node:
            break
    
    if not content_node:
        content_node = soup.body

    if content_node is None:
        return ""

    for tag in content_node.find_all(['nav', 'footer', 'script', 'style', 'aside', 'form']):
        tag.decompose()
        
    return content_node.get_text(separator="\n", strip=True)

def read_file_with_encoding(file_path: Path) -> str:
    """Try to read a file with different encodings."""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, try reading as bytes and decode with errors='ignore'
    with open(file_path, 'rb') as f:
        content = f.read()
        return content.decode('utf-8', errors='ignore')

def ingest_from_html(html_source_dir: Path):
    """
    Ingests documents from a directory of saved HTML files.
    """
    logging.info(f"--- Starting ingestion from local HTML files in: {html_source_dir} ---")
    
    html_files = list(html_source_dir.glob("*.html"))
    if not html_files:
        logging.error(f"No HTML files found in {html_source_dir}. Did you run the scraper first?")
        return

    docs = []
    for file_path in html_files:
        try:
            content = read_file_with_encoding(file_path)
            soup = BeautifulSoup(content, "lxml")
            text = extract_main_content(soup)
            if text:
                docs.append(Document(page_content=text, metadata={"source": str(file_path.name)}))
                logging.info(f"Processed: {file_path.name}")
        except Exception as e:
            logging.warning(f"Failed to process {file_path.name}: {e}")
            continue

    if not docs:
        logging.error("Failed to extract any content from the HTML files.")
        return

    logging.info(f"Successfully created {len(docs)} documents from {len(html_files)} HTML files.")

    # Chunk and embed
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(docs)
    logging.info(f"Split into {len(chunks)} chunks.")

    embedding_function = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
    config.DB_PATH.mkdir(parents=True, exist_ok=True)
    db = Chroma.from_documents(chunks, embedding_function, persist_directory=str(config.DB_PATH))
    
    logging.info(f"--- Ingestion complete! Vector store at: {config.DB_PATH} ---")
