"""
GUI module for the Resume Skill Matcher application
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import pandas as pd

from core.extractor import extract_text_from_file
from core.matcher import match_skills
from core.scorer import calculate_score

class ResumeSkillMatcherApp:
    """Main application class for Resume Skill Matcher"""
    
    def __init__(self, root):
        """Initialize the application with root window"""
        self.root = root
        self.root.title("Resume Skill Matcher")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.skills_file_path = tk.StringVar()
        self.resume_files = []
        self.processing_done = False
        self.results = []
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        """Create and setup all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File Selection Frame
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.pack(fill=tk.X, pady=10)
        
        # Skills CSV file selection
        ttk.Label(file_frame, text="Skills CSV:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.skills_file_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_skills_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Resume files selection
        ttk.Label(file_frame, text="Resumes:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.resume_files_label = ttk.Label(file_frame, text="No files selected")
        self.resume_files_label.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_resume_files).grid(row=1, column=2, padx=5, pady=5)
        
        # Process button
        self.process_button = ttk.Button(main_frame, text="Process Resumes", command=self.process_resumes)
        self.process_button.pack(pady=10)
        
        # Progress bar
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=10)
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.pack(side=tk.TOP, anchor=tk.W)
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10", )
        results_frame.pack(fill=tk.BOTH, expand='yes', pady=10)
        
        # Create treeview for results
        columns = ("Resume", "Score", "Matched Skills", "Missing Skills")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Set column headings
        self.results_tree.heading("Resume", text="Resume Name")
        self.results_tree.heading("Score", text="Score (%)")
        self.results_tree.heading("Matched Skills", text="Matched Skills")
        self.results_tree.heading("Missing Skills", text="Missing Skills")
        
        # # Set column widths
        self.results_tree.column("Resume", width=150, anchor=tk.W,stretch=False)
        self.results_tree.column("Score", width=80, anchor=tk.CENTER,stretch=False)
        self.results_tree.column("Matched Skills", width=300, anchor=tk.CENTER,stretch=False)
        self.results_tree.column("Missing Skills", width=300, anchor=tk.CENTER,stretch=False)
        
        # Add scrollbar
        xscrollbar = ttk.Scrollbar(self.results_tree, orient=tk.HORIZONTAL, command=self.results_tree.xview)
        self.results_tree.configure(xscroll=xscrollbar.set)
        
        yscrollbar = ttk.Scrollbar(self.results_tree, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=yscrollbar.set)
        
        # Pack treeview and scrollbar
        self.results_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Export button
        self.export_button = ttk.Button(main_frame, text="Export Results", command=self.export_results)
        self.export_button.pack(pady=10)
        self.export_button.state(["disabled"])
    
    def browse_skills_file(self):
        """Open file dialog to select skills CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select Skills CSV File",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if file_path:
            self.skills_file_path.set(file_path)
    
    def browse_resume_files(self):
        """Open file dialog to select multiple resume files"""
        files = filedialog.askopenfilenames(
            title="Select Resume Files",
            filetypes=[("Document Files", "*.pdf *.docx"), ("PDF Files", "*.pdf"), ("Word Files", "*.docx"), ("All Files", "*.*")]
        )
        if files:
            self.resume_files = list(files)
            if len(files) == 1:
                self.resume_files_label.config(text=f"1 file selected")
            else:
                self.resume_files_label.config(text=f"{len(files)} files selected")
    
    def process_resumes(self):
        """Validate inputs and start processing thread"""
        # Check if files are selected
        if not self.skills_file_path.get():
            messagebox.showwarning("Warning", "Please select a skills CSV file.")
            return
        
        if not self.resume_files:
            messagebox.showwarning("Warning", "Please select at least one resume file.")
            return
        
        # Disable buttons during processing
        self.process_button.state(["disabled"])
        self.export_button.state(["disabled"])
        self.progress_label.config(text="Loading skills data...")
        
        # Start processing in a separate thread
        threading.Thread(target=self.process_thread, daemon=True).start()
    
    def process_thread(self):
        """Background thread for processing resumes"""
        try:
            # Load skills data
            self.update_progress(0, "Loading skills data...")
            weighted_skills = pd.read_csv(self.skills_file_path.get())
            skill_list = weighted_skills['skills'].tolist()
            
            self.results = []
            total_files = len(self.resume_files)
            
            for i, resume_path in enumerate(self.resume_files):
                # Update progress
                file_name = os.path.basename(resume_path)
                self.update_progress((i / total_files) * 100, f"Processing {file_name}...")
                
                # Extract text based on file type
                resume_text = extract_text_from_file(resume_path)
                
                if(resume_text):
                    # Match skills
                    matched_skills,similarity_threshold = match_skills(resume_text, skill_list)
                    
                    # Calculate score
                    matched, missing, score = calculate_score(weighted_skills, matched_skills,similarity_threshold,max_threshold=0.75)
                else:
                    score=0.0
                    matched=['Unable to process resume.']
                    missing=['Unable to process resume.']

                # Add to results
                self.results.append({
                    "file_name": file_name,
                    "score": score,
                    "matched_skills": list(matched),
                    "missing_skills": list(missing)
                })
            
            # Update UI with results
            self.update_progress(100, "Processing complete!")
            self.root.after(0, self.update_results_tree)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {str(e)}"))
            self.update_progress(0, "Processing failed.")
            self.root.after(0, lambda: self.process_button.state(["!disabled"]))
    
    def update_progress(self, value, message):
        """Update progress bar and label in a thread-safe way"""
        self.root.after(0, lambda: self.progress_bar.config(value=value))
        self.root.after(0, lambda: self.progress_label.config(text=message))
    
    def update_results_tree(self):
        """Update results treeview with processed data"""
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Sort results by score (highest first)
        sorted_results = sorted(self.results, key=lambda x: x["score"], reverse=True)
        
        # Add results to treeview
        for result in sorted_results:
            matched_skills_str = ", ".join(result["matched_skills"]) if result["matched_skills"] else "None"
            missing_skills_str = ", ".join(result["missing_skills"]) if result["missing_skills"] else "None"
            
            self.results_tree.insert("", tk.END, values=(
                result["file_name"],
                f"{result['score']:.2f}",
                matched_skills_str,
                missing_skills_str
            ))
        
        # Enable buttons
        self.process_button.state(["!disabled"])
        self.export_button.state(["!disabled"])
        self.processing_done = True
    
    def export_results(self):
        """Export results to a CSV file"""
        if not self.processing_done or not self.results:
            messagebox.showwarning("Warning", "No results to export.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Export Results",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                # Create DataFrame from results
                results_data = []
                for result in self.results:
                    results_data.append({
                        "Resume": result["file_name"],
                        "Score (%)": f"{result['score']:.2f}",
                        "Matched Skills": ", ".join(result["matched_skills"]),
                        "Missing Skills": ", ".join(result["missing_skills"])
                    })
                
                df = pd.DataFrame(results_data).sort_values(by="Score (%)",ascending=False)
                df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", f"Results exported to {file_path}")
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")