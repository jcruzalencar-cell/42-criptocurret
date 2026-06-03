# 42 Blockchain - Layer 1 Implementation

A native blockchain (Layer 1) implementation in Python with proof-of-work consensus, FastAPI REST API, and Docker containerization.

## Features

- **Core Blockchain**: SHA-256 hashing, proof-of-work consensus mechanism
- **Block Structure**: Index, timestamp, data, previous hash, nonce
- **Validation**: Full chain integrity verification
- **REST API**: FastAPI endpoints for mining, transactions, and node management
- **Persistence**: JSON-based state persistence across server restarts
- **Containerization**: Docker and Docker Compose support
- **Clean Code**: Modular architecture, comprehensive docstrings, PEP 8 compliant

## Project Structure

```
42-criptocurret/
├── blockchain/
│   ├── __init__.py
│   ├── block.py           # Block class with hashing and mining
│   ├── blockchain.py      # Blockchain management and validation
│   ├── persistence.py     # JSON-based state persistence
│   └── utils.py           # Utility functions
├── api/
│   ├── __init__.py
│   └── node.py            # FastAPI REST API endpoints
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-container orchestration
└── README.md              # This file
```

## Installation

### Local Setup

```bash
git clone https://github.com/jcruzalencar-cell/42-criptocurret.git
cd 42-criptocurret

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py
```

The API will be available at `http://localhost:8000`

### Docker Setup

```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## API Endpoints

### Health & Status
- `GET /health` - Node health check
- `GET /validate` - Validate blockchain integrity

### Blockchain Operations
- `GET /chain` - Retrieve complete blockchain
- `POST /mine` - Mine a new block

### Transactions
- `POST /transactions` - Submit a transaction
- `GET /transactions/pending` - Get pending transactions

### Network
- `POST /nodes/register` - Register a peer node
- `GET /nodes` - Get registered peer nodes

## API Documentation

Interactive API documentation available at: `http://localhost:8000/docs`

## Dependencies

- FastAPI - Modern web framework for building APIs
- Uvicorn - ASGI web server
- Pydantic - Data validation using Python type hints
- Python 3.11+

## License

MIT License

## Author

Jcruzalencar-cell
