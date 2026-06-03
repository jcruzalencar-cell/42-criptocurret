"""Block class for the 42 Blockchain Layer 1 implementation.

This module defines the Block class, which represents a single block
in the blockchain. Each block contains cryptographic hashing, proof-of-work
mechanism, and immutability guarantees.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any


class Block:
    """Represents a single block in the 42 blockchain.
    
    Attributes:
        index (int): The position of the block in the blockchain.
        timestamp (str): ISO 8601 formatted timestamp of block creation.
        data (Dict[str, Any]): Transaction or data payload for this block.
        prev_hash (str): SHA-256 hash of the previous block.
        nonce (int): Proof-of-work counter for difficulty adjustment.
        hash (str): SHA-256 hash of the current block.
    """
    
    def __init__(
        self,
        index: int,
        timestamp: str,
        data: Dict[str, Any],
        prev_hash: str,
        nonce: int = 0
    ) -> None:
        """Initialize a new Block.
        
        Args:
            index: Position of the block in the chain.
            timestamp: ISO 8601 formatted creation time.
            data: Transaction or data payload.
            prev_hash: Hash of the previous block.
            nonce: Proof-of-work counter (default: 0).
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Calculate SHA-256 hash of the block.
        
        The hash is computed from the block's index, timestamp, data,
        previous hash, and nonce. This ensures immutability and enables
        efficient integrity verification.
        
        Returns:
            str: SHA-256 hash as hexadecimal string.
        """
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_content, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """Perform proof-of-work by finding a nonce that satisfies difficulty.
        
        Mining adjusts the nonce counter until the block's hash contains
        a leading zeros matching the difficulty level. This is the core
        consensus mechanism ensuring computational cost for block creation.
        
        Args:
            difficulty: Number of leading zeros required in the hash.
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary representation.
        
        Returns:
            Dict[str, Any]: Block data including hash and proof-of-work info.
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "prev_hash": self.prev_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @staticmethod
    def from_dict(block_dict: Dict[str, Any]) -> 'Block':
        """Create a Block instance from dictionary representation.
        
        Args:
            block_dict: Dictionary containing block data.
        
        Returns:
            Block: Reconstructed block instance.
        """
        block = Block(
            index=block_dict["index"],
            timestamp=block_dict["timestamp"],
            data=block_dict["data"],
            prev_hash=block_dict["prev_hash"],
            nonce=block_dict["nonce"]
        )
        block.hash = block_dict["hash"]
        return block
