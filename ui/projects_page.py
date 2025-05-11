"""
Projects page for Pipes application
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ui.project_form import ProjectForm
import database

class ProjectsPage(tk.Frame):
    """Projects page showing all projects with options to add, edit, and delete"""
    
    def __init__(self, parent):
        """Initialize the projects page
        
        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_projects()
        
    def setup_ui(self):
        """Set up the UI components"""
        # Button frame
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Add project button
        add_button = ttk.Button(button_frame, text="Add Project", command=self.add_project)
        add_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Refresh button
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.load_projects)
        refresh_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Projects treeview
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview columns
        columns = ("id", "name", "location", "created_at")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        
        # Configure column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Project Name")
        self.tree.heading("location", text="Location")
        self.tree.heading("created_at", text="Created At")
        
        # Configure column widths
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("location", width=200)
        self.tree.column("created_at", width=150)
        
        # Pack treeview
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=self.tree.yview)
        
        # Bind events
        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<ButtonRelease-3>", self.on_right_click)
        
    def load_projects(self):
        """Load projects from database and display in treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Get all projects
        projects = database.get_all_projects()
        
        # Add projects to treeview
        for project in projects:
            self.tree.insert("", tk.END, values=(
                project["id"],
                project["name"],
                project["location"],
                project["created_at"]
            ))
            
    def add_project(self):
        """Open form to add a new project"""
        # Create new project form window
        form = ProjectForm(self)
        
        # Wait for form to close
        self.wait_window(form)
        
        # Reload projects
        self.load_projects()
        
    def edit_project(self, project_id):
        """Open form to edit an existing project
        
        Args:
            project_id: ID of project to edit
        """
        # Get project details
        project = database.get_project(project_id)
        
        if project:
            # Create edit project form window
            form = ProjectForm(self, project=project)
            
            # Wait for form to close
            self.wait_window(form)
            
            # Reload projects
            self.load_projects()
            
    def delete_project(self, project_id):
        """Delete a project
        
        Args:
            project_id: ID of project to delete
        """
        # Confirm deletion
        if messagebox.askyesno("Delete Project", "Are you sure you want to delete this project?"):
            # Delete project
            success = database.delete_project(project_id)
            
            if success:
                messagebox.showinfo("Success", "Project deleted successfully")
                self.load_projects()
            else:
                messagebox.showerror("Error", "Failed to delete project")
                
    def on_item_double_click(self, event):
        """Handle double click on treeview item
        
        Args:
            event: Event data
        """
        # Get selected item
        item = self.tree.selection()[0]
        
        # Get project ID from selected item
        project_id = self.tree.item(item, "values")[0]
        
        # Edit project
        self.edit_project(int(project_id))
        
    def on_right_click(self, event):
        """Handle right click on treeview item
        
        Args:
            event: Event data
        """
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            
            # Get project ID from selected item
            project_id = self.tree.item(item, "values")[0]
            
            # Create popup menu
            popup_menu = tk.Menu(self, tearoff=0)
            popup_menu.add_command(label="Edit", command=lambda: self.edit_project(int(project_id)))
            popup_menu.add_command(label="Delete", command=lambda: self.delete_project(int(project_id)))
            
            # Display popup menu
            try:
                popup_menu.tk_popup(event.x_root, event.y_root, 0)
            finally:
                popup_menu.grab_release()