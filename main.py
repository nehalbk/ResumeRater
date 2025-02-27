#!/usr/bin/env python3
"""
Resume Skill Matcher - Main application entry point
"""

import tkinter as tk
from app.gui import ResumeSkillMatcherApp

def main():
    """Application entry point"""
    # Create the main window
    root = tk.Tk()
    # Initialize the application
    app = ResumeSkillMatcherApp(root)
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()