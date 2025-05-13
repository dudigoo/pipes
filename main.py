#!/usr/bin/env python3
"""
Pipes Project - Main Entry Point
"""
import tkinter as tk
from ui.app import Application
from database import initialize_database
from languages import language_manager

def main():
    """Main entry point for the application"""
    # Initialize database
    initialize_database()
    
    # Create root window
    root = tk.Tk()
    if language_manager.is_rtl:
        root.tk.call("set", "rtl", "1")  # Enable RTL for the root window
    root.title("Pipes - Project Management")
    root.geometry("800x600")
    
    # Create application
    app = Application(root)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()