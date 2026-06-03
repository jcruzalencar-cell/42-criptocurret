"""FastAPI node API for the 42 Blockchain.

This module defines the REST API endpoints for blockchain operations:
- Mining new blocks
- Retrieving chain state
- Registering peer nodes
- Submitting transactions
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
from blockchain.blockchain import Blockchain
from blockchain.persistence import BlockchainPersistence
from blockchain.utils import is_valid_address, is_valid_transaction, validate_difficulty

# Initialize FastAPI app and blockchain
app = FastAPI(
    title="42 Blockchain Node",
    description="Layer 1 blockchain implementation with proof-of-work consensus",
    version="1.0.0"
)

# Initialize persistence and blockchain
persistence = BlockchainPersistence()
blockchain = persistence.load_blockchain()

# Store peer node addresses
peer_nodes: set = set()


# Pydantic models for request/response validation
class TransactionRequest(BaseModel):
    """Request model for submitting transactions."""
    sender: str = Field(..., min_length=1, description="Sender address")
    recipient: str = Field(..., min_length=1, description="Recipient address")
    amount: float = Field(..., gt=0, description="Transaction amount")
    
    @validator('sender', 'recipient')
    def validate_addresses(cls, v):
        if not is_valid_address(v):
            raise ValueError('Invalid address format')
        return v


class MineRequest(BaseModel):
    """Request model for mining a block."""
    miner_address: str = Field(..., min_length=1, description="Address of the miner")
    
    @validator('miner_address')
    def validate_miner(cls, v):
        if not is_valid_address(v):
            raise ValueError('Invalid miner address format')
        return v


class NodeRegistrationRequest(BaseModel):
    """Request model for registering peer nodes."""
    node_url: str = Field(..., min_length=1, description="URL of peer node")


class BlockResponse(BaseModel):
    """Response model for block data."""
    index: int
    timestamp: str
    data: Dict[str, Any]
    prev_hash: str
    nonce: int
    hash: str


class ChainResponse(BaseModel):
    """Response model for blockchain state."""
    chain_length: int
    difficulty: int
    is_valid: bool
    pending_transactions: int
    mining_reward: float
    chain: List[BlockResponse]


class HealthResponse(BaseModel):
    """Response model for node health check."""
    status: str
    timestamp: str
    chain_length: int
    pending_transactions: int
    is_valid: bool


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Node"])
def health_check() -> Dict[str, Any]:
    """Check node health and blockchain status.
    
    Returns:
        dict: Node health status and blockchain metrics.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "chain_length": len(blockchain.chain),
        "pending_transactions": len(blockchain.pending_data),
        "is_valid": blockchain.validate_chain()
    }


# Blockchain info endpoint
@app.get("/chain", response_model=ChainResponse, tags=["Blockchain"])
def get_chain() -> Dict[str, Any]:
    """Retrieve the complete blockchain.
    
    Returns:
        dict: Blockchain state including all blocks and metadata.
    """
    blockchain_dict = blockchain.to_dict()
    chain_data = blockchain.get_chain_as_dict()
    
    return {
        **blockchain_dict,
        "chain": [BlockResponse(**block) for block in chain_data]
    }


# Mining endpoint
@app.post("/mine", response_model=BlockResponse, tags=["Mining"])
def mine_block(request: MineRequest) -> Dict[str, Any]:
    """Mine a new block with pending transactions.
    
    Args:
        request: Mining request containing miner address.
    
    Returns:
        dict: The newly mined block.
    
    Raises:
        HTTPException: If no pending data or mining fails.
    """
    if not blockchain.pending_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No pending transactions to mine"
        )
    
    try:
        new_block = blockchain.mine_pending_data(request.miner_address)
        persistence.save_blockchain(blockchain)
        return BlockResponse(**new_block.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Mining failed: {str(e)}"
        )


# Transaction submission endpoint
@app.post("/transactions", tags=["Transactions"])
def submit_transaction(request: TransactionRequest) -> Dict[str, str]:
    """Submit a new transaction to pending pool.
    
    Args:
        request: Transaction request with sender, recipient, and amount.
    
    Returns:
        dict: Confirmation message and transaction details.
    """
    transaction = {
        "sender": request.sender,
        "recipient": request.recipient,
        "amount": request.amount,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if not is_valid_transaction(transaction):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction format"
        )
    
    blockchain.add_pending_data(transaction)
    persistence.save_blockchain(blockchain)
    
    return {
        "status": "pending",
        "message": "Transaction submitted successfully",
        "transaction_id": f"{request.sender}_{request.recipient}_{datetime.utcnow().timestamp()}"
    }


# Node registration endpoint
@app.post("/nodes/register", tags=["Network"])
def register_node(request: NodeRegistrationRequest) -> Dict[str, Any]:
    """Register a new peer node in the network.
    
    Args:
        request: Node registration request with peer node URL.
    
    Returns:
        dict: Updated list of registered nodes.
    """
    peer_nodes.add(request.node_url)
    
    return {
        "message": "Node registered successfully",
        "registered_nodes": list(peer_nodes),
        "total_peers": len(peer_nodes)
    }


# Get pending transactions
@app.get("/transactions/pending", tags=["Transactions"])
def get_pending_transactions() -> Dict[str, Any]:
    """Retrieve all pending transactions.
    
    Returns:
        dict: List of transactions awaiting mining.
    """
    return {
        "pending_count": len(blockchain.pending_data),
        "transactions": blockchain.pending_data
    }


# Get registered peers
@app.get("/nodes", tags=["Network"])
def get_nodes() -> Dict[str, Any]:
    """Retrieve registered peer nodes.
    
    Returns:
        dict: List of connected peer nodes.
    """
    return {
        "total_nodes": len(peer_nodes),
        "nodes": list(peer_nodes)
    }


# Validate blockchain endpoint
@app.get("/validate", tags=["Blockchain"])
def validate_blockchain() -> Dict[str, Any]:
    """Validate blockchain integrity.
    
    Returns:
        dict: Validation result and chain statistics.
    """
    is_valid = blockchain.validate_chain()
    
    return {
        "is_valid": is_valid,
        "chain_length": len(blockchain.chain),
        "message": "Blockchain is valid" if is_valid else "Blockchain is corrupted"
    }


# Shutdown event handler
@app.on_event("shutdown")
def shutdown_event():
    """Save blockchain state on server shutdown."""
    persistence.save_blockchain(blockchain)
