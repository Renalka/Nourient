from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class IDatabaseClient(ABC):
    """
    Abstract interface for database operations. 
    This ensures our microservices are decoupled from Firestore. 
    If we ever migrate to AlloyDB or PostgreSQL, we just implement this interface.
    """
    
    @abstractmethod
    async def get_document(self, collection: str, document_id: str) -> Optional[Dict[str, Any]]:
        pass
        
    @abstractmethod
    async def save_document(self, collection: str, document_id: str, data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def query_documents(self, collection: str, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

class IAIEngine(ABC):
    """
    Abstract interface for AI model interactions.
    Decouples the business logic from the specific Gemini SDK implementation.
    """
    
    @abstractmethod
    async def extract_structured_data(self, image_bytes: bytes, prompt: str, response_schema: Any) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    async def audit_claims(self, claims: List[str], ingredients: List[str]) -> Dict[str, Any]:
        pass
