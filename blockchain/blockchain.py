"""Blockchain class for the 42 Blockchain Layer 1 implementation.

This module defines the Blockchain class, which manages the chain of blocks,
validates integrity, and coordinates the consensus mechanism.
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from blockchain.block import Block


class Blockchain:
    """Manages the blockchain data structure and validation logic.
    
    Attributes:
        chain (List[Block]): List of blocks forming the blockchain.
        difficulty (int): Number of leading zeros required for proof-of-work.
        pending_data (List[Dict]): Data awaiting inclusion in the next block.
        mining_reward (float): Reward issued when a block is successfully mined.
    """
    
    def __init__(self, difficulty: int = 2) -> None:
        """Initialize a new Blockchain.
        
        Args:
            difficulty: Proof-of-work difficulty level (default: 2).
        """
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.pending_data: List[Dict[str, Any]] = []
        self.mining_reward = 10.0
        
        # Create genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self) -> None:
        """Create and mine the first block (genesis block) of the chain.
        
        The genesis block has index 0, no previous hash, and serves as
        the foundation for all subsequent blocks.
        """
        genesis_block = Block(
            index=0,
            timestamp=datetime.utcnow().isoformat(),
            data={"message": "Genesis Block - 42 Blockchain"},
            prev_hash="0"
        )
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
    
    def get_latest_block(self) -> Block:
        """Retrieve the most recent block in the chain.
        
        Returns:
            Block: The last block in the blockchain.
        """
        return self.chain[-1]
    
    def add_pending_data(self, data: Dict[str, Any]) -> None:
        """Add data to pending pool awaiting mining into a block.
        
        Args:
            data: Transaction or data payload to be included in next block.
        """
        self.pending_data.append(data)
    
    def mine_pending_data(self, miner_address: str) -> Block:
        """Mine pending data into a new block.
        
        Creates a new block containing all pending data, performs proof-of-work,
        appends to chain, and awards mining reward.
        
        Args:
            miner_address: Address or identifier of the miner.
        
        Returns:
            Block: The newly mined and added block.
        
        Raises:
            ValueError: If there is no pending data to mine.
        """
        if not self.pending_data:
            raise ValueError("No pending data to mine")
        
        new_index = len(self.chain)
        latest_block = self.get_latest_block()
        
        # Prepare block data
        block_data = {
            "transactions": self.pending_data,
            "miner": miner_address,
            "reward": self.mining_reward
        }
        
        # Create and mine new block
        new_block = Block(
            index=new_index,
            timestamp=datetime.utcnow().isoformat(),
            data=block_data,
            prev_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        
        # Add to chain and clear pending data
        self.chain.append(new_block)
        self.pending_data = []
        
        return new_block
    
    def validate_chain(self) -> bool:
        """Validate the integrity of the entire blockchain.
        
        Checks that:
        - Each block's hash is correctly calculated.
        - Each block references the correct previous block hash.
        - Each block's proof-of-work meets the difficulty requirement.
        
        Returns:
            bool: True if blockchain is valid, False otherwise.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Verify current block's hash
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Verify chain link
            if current_block.prev_hash != previous_block.hash:
                return False
            
            # Verify proof-of-work
            if not current_block.hash.startswith("0" * self.difficulty):
                return False
        
        return True
    
    def get_chain_as_dict(self) -> List[Dict[str, Any]]:
        """Convert entire blockchain to dictionary representation.
        
        Returns:
            List[Dict[str, Any]]: List of serialized blocks.
        """
        return [block.to_dict() for block in self.chain]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert blockchain metadata to dictionary representation.
        
        Returns:
            Dict[str, Any]: Blockchain statistics and configuration.
        """
        return {
            "chain_length": len(self.chain),
            "difficulty": self.difficulty,
            "is_valid": self.validate_chain(),
            "pending_transactions": len(self.pending_data),
            "mining_reward": self.mining_reward
        }
    
    def replace_chain(self, new_chain_data: List[Dict[str, Any]]) -> bool:
        """Replace current chain with a new one if it's valid and longer.
        
        This implements the consensus rule: the longest valid chain wins.
        Used for synchronizing nodes in a distributed network.
        
        Args:
            new_chain_data: List of serialized blocks to replace chain with.
        
        Returns:
            bool: True if chain was replaced, False if new chain is invalid.
        """
        # Reconstruct blocks from data
        try:
            new_chain = [Block.from_dict(block_dict) for block_dict in new_chain_data]
        except (KeyError, TypeError):
            return False
        
        # Create temporary blockchain to validate
        temp_blockchain = Blockchain(difficulty=self.difficulty)
        temp_blockchain.chain = new_chain
        
        # Replace only if new chain is valid and longer
        if temp_blockchain.validate_chain() and len(new_chain) > len(self.chain):
            self.chain = new_chain
            self.pending_data = []
            return True
        
        return False
