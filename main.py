#!/usr/bin/env python3
"""
Pipes Project - Main Entry Point
"""
import tkinter as tk
from ui.app import Application
from database import initialize_database

def main():
    """Main entry point for the application"""
    # Initialize database
    initialize_database()
    
    # Create root window
    root = tk.Tk()
    root.title("Pipes - Project Management")
    root.geometry("800x600")
    
    # Create application
    app = Application(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()