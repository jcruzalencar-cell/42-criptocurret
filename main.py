"""Main entry point for the 42 Blockchain Node.

Starts the FastAPI application with uvicorn server.
Handles initialization and shutdown of blockchain state.
"""

import logging
from api.node import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    """Start the blockchain node server."""
    import uvicorn
    
    logger.info("Starting 42 Blockchain Node")
    logger.info("API Documentation available at http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
