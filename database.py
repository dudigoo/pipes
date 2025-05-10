"""
Database operations for the Pipes application
"""
import os
import sqlite3
from sqlite3 import Error
from typing import List, Dict, Any, Optional

DATABASE_FILE = "pipes.db"

def get_connection():
    """Get a connection to the database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def initialize_database():
    """Initialize the database with required tables"""
    # SQL statements
    create_projects_table = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Execute SQL
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(create_projects_table)
            conn.commit()
            print("Database initialized successfully")
        except Error as e:
            print(f"Error initializing database: {e}")
        finally:
            conn.close()

def get_all_projects() -> List[Dict[str, Any]]:
    """Get all projects from the database"""
    conn = get_connection()
    projects = []
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, location, created_at FROM projects ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            for row in rows:
                projects.append(dict(row))
                
        except Error as e:
            print(f"Error querying projects: {e}")
        finally:
            conn.close()
            
    return projects

def add_project(name: str, location: str) -> Optional[int]:
    """Add a new project to the database"""
    conn = get_connection()
    project_id = None
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (name, location) VALUES (?, ?)",
                (name, location)
            )
            conn.commit()
            project_id = cursor.lastrowid
            print(f"Project added with ID: {project_id}")
        except Error as e:
            print(f"Error adding project: {e}")
        finally:
            conn.close()
            
    return project_id

def update_project(project_id: int, name: str, location: str) -> bool:
    """Update an existing project"""
    conn = get_connection()
    success = False
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE projects SET name = ?, location = ? WHERE id = ?",
                (name, location, project_id)
            )
            conn.commit()
            success = cursor.rowcount > 0
        except Error as e:
            print(f"Error updating project: {e}")
        finally:
            conn.close()
            
    return success

def delete_project(project_id: int) -> bool:
    """Delete a project from the database"""
    conn = get_connection()
    success = False
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
            conn.commit()
            success = cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting project: {e}")
        finally:
            conn.close()
            
    return success

def get_project(project_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific project by ID"""
    conn = get_connection()
    project = None
    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, location, created_at FROM projects WHERE id = ?", 
                (project_id,)
            )
            row = cursor.fetchone()
            
            if row:
                project = dict(row)
                
        except Error as e:
            print(f"Error getting project: {e}")
        finally:
            conn.close()
            
    return project