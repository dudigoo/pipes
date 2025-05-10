"""
Project model for Pipes application
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Project:
    """Project data model"""
    name: str
    location: str
    id: Optional[int] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data):
        """Create a Project instance from a dictionary
        
        Args:
            data: Dictionary containing project data
            
        Returns:
            Project instance
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            location=data.get("location"),
            created_at=data.get("created_at")
        )
    
    def to_dict(self):
        """Convert project to dictionary
        
        Returns:
            Dictionary representation of project
        """
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "created_at": self.created_at
        }