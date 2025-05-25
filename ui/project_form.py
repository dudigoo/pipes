"""
Project form for adding or editing projects
"""
import tkinter as tk
from tkinter import ttk, messagebox
import database
from languages import language_manager
#from reportlab.lib.pagesizes import A4
#from reportlab.pdfgen import canvas
from fpdf import FPDF
import os

class ProjectForm(tk.Toplevel):
    """Form for adding or editing projects"""
    
    def __init__(self, parent, project=None):
        """Initialize the project form
        
        Args:
            parent: Parent widget
            project: Project data for editing (None for new project)
        """
        super().__init__(parent)
        self.parent = parent
        self.project = project
        
        # Set up form
        self.title("Edit Project" if project else "Add Project")
        self.geometry("400x250")
        self.resizable(False, False)
        self.grab_set()  # Make window modal
        
        # Create form fields
        self.setup_ui()
        
        # Center window
        self.center_window()
        
    def setup_ui(self):
        """Set up the UI components"""
        # Main frame
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Project name
        ttk.Label(main_frame, text=language_manager.translate("project_name")).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10)
        
        # Project location
        ttk.Label(main_frame, text=language_manager.translate("location")).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.location_entry = ttk.Entry(main_frame, width=30)
        self.location_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Save button
        ttk.Button(button_frame, text=language_manager.translate("save"), command=self.save_project).pack(side=tk.LEFT, padx=5)
        
        # Cancel button
        ttk.Button(button_frame, text=language_manager.translate("cancel"), command=self.destroy).pack(side=tk.LEFT, padx=5)
        
        # Print button
        ttk.Button(button_frame, text=language_manager.translate("Print"), command=self.on_print).pack(side=tk.LEFT, padx=5)
        
        # If editing existing project, populate fields
        if self.project:
            self.name_entry.insert(0, self.project["name"])
            self.location_entry.insert(0, self.project["location"])
            
        # Set focus to name entry
        self.name_entry.focus()

        if language_manager.is_rtl:
            main_frame.tk.call("tk", "scaling", 1.0)  # Adjust scaling for RTL
            main_frame.tk.call("set", "rtl", "1")  # Enable RTL
        
    def save_project(self):
        """Save the project (add new or update existing)"""
        # Get values from form
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()
        
        # Validate inputs
        if not name:
            messagebox.showerror("Validation Error", "Project name is required")
            self.name_entry.focus()
            return
            
        if not location:
            messagebox.showerror("Validation Error", "Location is required")
            self.location_entry.focus()
            return
        
        try:
            if self.project:  # Editing existing project
                success = database.update_project(self.project["id"], name, location)
                if success:
                    messagebox.showinfo("Success", "Project updated successfully")
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Failed to update project")
            else:  # Adding new project
                project_id = database.add_project(name, location)
                if project_id:
                    messagebox.showinfo("Success", "Project added successfully")
                    self.destroy()
                else:
                    messagebox.showerror("Error", "Failed to add project")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        
        # Get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calculate position
        x = (screen_width - self.winfo_width()) // 2
        y = (screen_height - self.winfo_height()) // 2
        
        # Set geometry
        self.geometry(f"+{x}+{y}")

    def get_current_project_details(self):
        """Return the current project's details as a dict"""
        if self.project:
            return {
                "Name": self.project.get("name", ""),
                "Date": self.project.get("created_at", ""),
                "Location": self.project.get("location", ""),
                "ID": self.project.get("id", "")
            }
        return {}

    def print_project(self, project_details):
        """Generate and open PDF for the given project details using fpdf"""
        filename = "project_details.pdf"
        pdf = FPDF()
        pdf.add_page()
        try:
            # Try to use DejaVu font for Unicode/hebrew support if available
            pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            pdf.set_font('DejaVu', '', 16)
        except Exception:
            pdf.set_font("Arial", size=16)
        pdf.cell(0, 10, "Project Details", ln=True)
        try:
            pdf.set_font('DejaVu', '', 12)
        except Exception:
            pdf.set_font("Arial", size=12)
        for key, value in project_details.items():
            pdf.cell(0, 10, f"{key}: {value}", ln=True)
        pdf.output(filename)
        try:
            # Use platform-independent way to open PDF
            if os.name == "nt":
                os.startfile(filename)
            elif os.name == "posix":
                import subprocess
                subprocess.run(["xdg-open", filename], check=False)
            else:
                messagebox.showinfo("Info", f"PDF saved as {filename}")
        except Exception as e:
            messagebox.showerror("שגיאה", f"שגיאה ביצירת PDF:\n{e}")

    def on_print(self):
        """Handle the print button click"""
        details = self.get_current_project_details()
        self.print_project(details)