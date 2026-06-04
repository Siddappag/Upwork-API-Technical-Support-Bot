# Upwork API Technical Support AI Bot (RAG)

## 📋 Overview

This is a **Retrieval-Augmented Generation (RAG)** based AI assistant that answers developer questions about the Upwork API documentation. The system retrieves relevant documentation sections and uses DeepInfra's Meta-Llama model to generate accurate answers directly from the provided context.

**Key Features:**
- 📚 Semantic search of Upwork API documentation
- 🧠 LLM-powered answer generation with context awareness
- 🔒 Anti-hallucination guard - only answers from documentation
- ⚡ Response latency tracking
- 📝 Source citation and transparency
- 🎨 Clean Streamlit web interface

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.11+ | Core implementation |
| **Framework** | LangChain | RAG orchestration |
| **Vector DB** | ChromaDB | Local embeddings storage |
| **Embeddings** | sentence-transformers | all-MiniLM-L6-v2 (local) |
| **LLM Provider** | DeepInfra API | meta-llama/Meta-Llama-3.1-8B |
| **Frontend** | Streamlit | Web interface |
| **Env Management** | python-dotenv | Configuration |

---

## 📦 Installation

### 1. Clone/Navigate to Project
```bash
cd upwork-rag-bot
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and add your DeepInfra API key
```

Get your API key from: https://deepinfra.com/

### 5. Prepare Your PDF
Place your Upwork API documentation PDF at:
```
data/upwork_api_reference.pdf
```

---

## 🚀 Quick Start

### Step 1: Ingest Documents
Run this once to load, chunk, embed, and index the PDF:

```bash
python ingest.py
```

**Output:**
- Character count of loaded document
- First 500 characters sample
- Number of chunks created
- Embeddings generated
- ChromaDB database created at `./chroma_db/`

### Step 2: Launch Streamlit App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Step 3: Ask Questions
Type your question and click "Ask Question"

---

## 📁 Project Structure

```
upwork-rag-bot/
├── app.py                          # Streamlit web UI
├── ingest.py                       # Document ingestion pipeline
├── rag.py                          # RAG core logic
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Environment variables template
│
├── data/
│   └── upwork_api_reference.pdf   # Your Upwork API PDF
│
├── utils/
│   ├── loader.py                  # PDF loading & sanity checks
│   ├── embeddings.py              # Embedding generation (local)
│   ├── vectorstore.py             # ChromaDB management
│   └── retriever.py               # Semantic retrieval
│
├── prompts/
│   └── system_prompt.txt          # LLM system prompt
│
├── chroma_db/                      # Persistent vector database (auto-created)
│   └── [chromadb files]
│
└── README.md                       # This file
```

---

## 🔧 Configuration

### Environment Variables (.env)

```env
DEEPINFRA_API_KEY=your_api_key_here
DEEPINFRA_MODEL=meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo
DEEPINFRA_BASE_URL=https://api.deepinfra.com/v1/openai
```

### Tuning Parameters

Edit in source code as needed:

**In `ingest.py`:**
- `chunk_size`: 500 (default) - larger = more context per chunk
- `chunk_overlap`: 50 (default) - prevents losing context across chunks

**In `utils/retriever.py`:**
- `top_k`: 3 (default) - number of chunks to retrieve

**In `rag.py`:**
- `temperature`: 0.7 (default) - model creativity (0-1)
- `max_tokens`: 1024 (default) - max response length

---

## 📚 Module Documentation

### `ingest.py`
**Responsibility:** One-time document preparation

**Process:**
1. Load PDF from `data/upwork_api_reference.pdf`
2. Perform sanity check (character count, sample text)
3. Split into chunks (500 chars, 50 overlap)
4. Generate embeddings locally
5. Store in ChromaDB with persistence

**Run:** `python ingest.py`

---

### `rag.py`
**Responsibility:** Core RAG logic - retrieval + generation

**RAGBot Class:**
- `retrieve_context(query)` - Get top 3 relevant chunks
- `generate_answer(query, chunks)` - LLM answer generation
- `answer_question(query)` - Full pipeline

**API Integration:**
- Uses DeepInfra OpenAI-compatible endpoint
- System prompt enforces documentation-only answers
- Anti-hallucination: Fallback for missing info

---

### `app.py`
**Responsibility:** Streamlit web interface

**Features:**
- Query input field
- Answer display with formatting
- Source chunk viewer
- Response latency display
- Vector DB status in sidebar
- Evaluation questions reference

**Run:** `streamlit run app.py`

---

### `utils/loader.py`
**Functions:**
- `load_pdf(pdf_path)` - Extract text from PDF
- `perform_sanity_check(text)` - Get char count & sample

---

### `utils/embeddings.py`
**Class:** `EmbeddingGenerator`
- `generate_embeddings(texts)` - Embed multiple chunks
- `embed_query(query)` - Embed single query
- Uses: sentence-transformers/all-MiniLM-L6-v2 (local)

---

### `utils/vectorstore.py`
**Class:** `VectorStore`
- Manages ChromaDB persistence
- `add_documents(chunks, embeddings)` - Store chunks
- `search(query_embedding, top_k)` - Semantic search
- Cosine similarity search

---

### `utils/retriever.py`
**Class:** `Retriever`
- `retrieve(query)` - Get relevant chunks for query

**Function:**
- `create_chunks(text, chunk_size, chunk_overlap)` - Text splitting

---

## ❓ Evaluation Questions

The system is evaluated on these questions:

### Q1: Rate Limiting
**Question:** What is the specific request-per-second rate limit for the Upwork API, and is it enforced per Key or per IP?

### Q2: OAuth Token Validity
**Question:** How long is an OAuth access token valid for?
**Expected:** 24 hours

### Q3: Client Credentials Grant
**Question:** Can I use a Client Credentials Grant to access a user's private contract details?
**Answer must come only from documentation.**

---

## 🛡️ Hallucination Prevention

The system implements multiple safeguards:

1. **System Prompt Enforcement**
   - Explicit instructions to use only provided context
   - Fallback message for missing information

2. **Context Validation**
   - Checks if retrieval returned valid chunks
   - Returns fallback if context is empty

3. **Structured Prompting**
   - Clear separation of context and query
   - Instructions to cite sources

4. **Fallback Response**
   ```
   "I'm sorry, but the provided documentation does not contain that information."
   ```

---

## ⚡ Performance Tips

1. **Faster Responses:**
   - Reduce `max_tokens` in rag.py
   - Use smaller `top_k` for retrieval (2 instead of 3)
   - Decrease `chunk_size` for faster retrieval

2. **Better Answers:**
   - Increase `chunk_size` for more context
   - Use `chunk_overlap > 50` for technical content
   - Tune `temperature` (lower = more deterministic)

3. **Resource Efficiency:**
   - First run takes time to download embeddings model
   - Subsequent runs are faster (model cached)
   - Vector DB persists - no re-indexing needed

---

## 🐛 Troubleshooting

### Issue: "PDF not found"
```
cd upwork-rag-bot
# Place your PDF at data/upwork_api_reference.pdf
```

### Issue: "DEEPINFRA_API_KEY not set"
```bash
# Create .env file with your key
DEEPINFRA_API_KEY=your_key_here
```

### Issue: "Vector database not initialized"
```bash
# Run ingestion first
python ingest.py
```

### Issue: Slow on first run
- First run downloads sentence-transformers model (~500MB)
- Model is cached locally after
- Subsequent runs are faster

### Issue: API rate limit
- DeepInfra has rate limits on free tier
- Wait a moment and retry
- Consider paid tier for higher limits

---

## 📊 System Architecture

```
User Query
    ↓
[Streamlit UI]
    ↓
[Query Embedding]  ← sentence-transformers
    ↓
[ChromaDB Search]  ← Retrieve top 3 chunks
    ↓
[Prompt Building]  ← Combine context + system prompt + query
    ↓
[DeepInfra API]    ← meta-llama/3.1-8B-Instruct-Turbo
    ↓
[Answer + Sources] ← Display with latency
```

---

## 📝 Example Conversation

**User:** "How do I authenticate with the Upwork API?"

**Bot Retrieval:** 
- Finds 3 relevant chunks about OAuth, authentication headers, etc.

**Bot Generation:**
- Uses LLM to synthesize answer from chunks
- Follows system prompt (documentation-only)

**Response:**
```
Based on the documentation, Upwork API supports OAuth 2.0 for authentication...

⏱️ Response Time: 1.23 seconds

📚 Sources:
[Shows retrieved chunks with formatting]
```

---

## 🔐 Security

✅ **Best Practices Implemented:**
- API keys stored in .env (not in code)
- No keys in .env.example
- Environment variables loaded via python-dotenv
- No credentials logged

⚠️ **Before Production:**
- Regenerate API keys
- Use separate keys for dev/prod
- Implement rate limiting
- Add authentication to Streamlit app
- Use secrets management (AWS Secrets, HashiCorp Vault)

---

## 📈 Future Enhancements

- [ ] Support multiple PDF documents
- [ ] Add question history/conversation memory
- [ ] Web scraping for real-time documentation updates
- [ ] Multi-language support
- [ ] User feedback collection
- [ ] Performance analytics dashboard
- [ ] Fine-tuning on Upwork-specific Q&A pairs
- [ ] Integration with Upwork's official API
- [ ] Docker containerization
- [ ] Production deployment (AWS, GCP, etc.)

---

## 📄 License

This project is part of the Associate AI Developer assignment.

---

## 👤 Author

Created as an assignment demonstration of RAG systems, LangChain integration, and LLM-powered AI applications.

---

## 📞 Support

**Issues with DeepInfra:** https://deepinfra.com/docs
**Issues with LangChain:** https://python.langchain.com/
**Issues with Streamlit:** https://docs.streamlit.io/

---

**Last Updated:** June 2024
**Version:** 1.0
