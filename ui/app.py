"""
Main application window for Pipes
"""
import tkinter as tk
from tkinter import ttk
from ui.projects_page import ProjectsPage

class Application:
    """Main application class handling UI components"""
    
    def __init__(self, root):
        """Initialize the application
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Projects page
        self.projects_page = ProjectsPage(self.notebook)
        self.notebook.add(self.projects_page, text="Projects")
        
        # Status bar
        self.status_bar = tk.Frame(self.root, height=25)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(self.status_bar, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X)
        
    def update_status(self, message):
        """Update status bar message
        
        Args:
            message: Message to display
        """
        self.status_label.config(text=message)
        self.root.update_idletasks()