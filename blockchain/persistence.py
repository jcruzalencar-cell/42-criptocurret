"""Persistence layer for blockchain state management.

This module provides simple JSON-based persistence for the blockchain,
ensuring state survives server restarts.
"""

import json
import os
from typing import Dict, List, Any, Optional
from blockchain.blockchain import Blockchain
from blockchain.block import Block


class BlockchainPersistence:
    """Handles saving and loading blockchain state to disk.
    
    Attributes:
        storage_path (str): Path to the JSON file storing blockchain state.
    """
    
    def __init__(self, storage_path: str = "data/blockchain.json") -> None:
        """Initialize persistence manager.
        
        Args:
            storage_path: Path where blockchain state will be persisted.
        """
        self.storage_path = storage_path
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self) -> None:
        """Ensure storage directory exists, create if necessary."""
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    def save_blockchain(self, blockchain: Blockchain) -> None:
        """Persist blockchain state to disk.
        
        Saves the complete chain and configuration to JSON format.
        
        Args:
            blockchain: Blockchain instance to persist.
        """
        state = {
            "chain": blockchain.get_chain_as_dict(),
            "difficulty": blockchain.difficulty,
            "mining_reward": blockchain.mining_reward,
            "pending_data": blockchain.pending_data
        }
        
        with open(self.storage_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_blockchain(self, difficulty: int = 2) -> Blockchain:
        """Load blockchain state from disk or create new.
        
        If persisted state exists, loads it. Otherwise creates a new
        blockchain with genesis block.
        
        Args:
            difficulty: Proof-of-work difficulty if creating new blockchain.
        
        Returns:
            Blockchain: Loaded or newly created blockchain instance.
        """
        blockchain = Blockchain(difficulty=difficulty)
        
        if not os.path.exists(self.storage_path):
            return blockchain
        
        try:
            with open(self.storage_path, 'r') as f:
                state = json.load(f)
            
            # Reconstruct blockchain from persisted state
            blockchain.chain = [
                Block.from_dict(block_dict)
                for block_dict in state.get("chain", [])
            ]
            blockchain.difficulty = state.get("difficulty", difficulty)
            blockchain.mining_reward = state.get("mining_reward", 10.0)
            blockchain.pending_data = state.get("pending_data", [])
            
            return blockchain
        except (json.JSONDecodeError, KeyError, TypeError):
            # If corrupted, return fresh blockchain
            return blockchain
    
    def clear_storage(self) -> None:
        """Delete persisted blockchain state."""
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
