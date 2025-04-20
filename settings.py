import tkinter as tk
from tkinter import ttk, filedialog
import yaml
from pathlib import Path

class ConfigEditor:
    def __init__(self, master, config_path):
        self.master = master
        self.config_path = Path(config_path)
        self.data = self.load_config()
        self.entries = {}
        
        self.setup_ui()
        
    def load_config(self):
        """Load YAML configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def save_config(self):
        """Save configuration to YAML file"""
        with open(self.config_path, 'w') as f:
            yaml.safe_dump(self.data, f, default_flow_style=False)
        
    def setup_ui(self):
        """Create the configuration editor UI"""
        self.master.title("Configuration Editor")
        self.master.geometry("800x600")
        
        # Create main container
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create widgets for each configuration item
        self.create_widgets(scrollable_frame, self.data)
        
        # Save button
        save_btn = ttk.Button(
            self.master,
            text="Save Configuration",
            command=self.on_save
        )
        save_btn.pack(pady=10)

    def create_widgets(self, parent, data, parent_keys=[]):
        """Recursively create widgets for configuration items"""
        for key, value in data.items():
            frame = ttk.Frame(parent)
            frame.pack(fill=tk.X, padx=5, pady=5)
            
            if isinstance(value, dict):
                # Create section label
                ttk.Label(frame, text=key, font=('Helvetica', 12, 'bold')).pack(anchor='w')
                # Recursively create widgets for nested items
                self.create_widgets(parent, value, parent_keys + [key])
            else:
                # Create label and entry
                ttk.Label(frame, text=key, width=20).pack(side=tk.LEFT)
                entry = ttk.Entry(frame, width=50)
                entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
                
                # Set initial value
                entry.insert(0, str(value))
                
                # Store reference using full key path
                full_key = tuple(parent_keys + [key])
                self.entries[full_key] = entry

    def on_save(self):
        """Handle save button click"""
        for key_path, entry in self.entries.items():
            current = self.data
            # Navigate through nested dictionaries
            for key in key_path[:-1]:
                current = current.setdefault(key, {})
            # Update value
            current[key_path[-1]] = entry.get()
        
        self.save_config()
        tk.messagebox.showinfo("Success", "Configuration saved successfully!")

def open_config_editor(config_path):
    root = tk.Tk()
    editor = ConfigEditor(root, config_path)
    root.mainloop()

if __name__ == "__main__":
    # Example usage - call this from your main application
    open_config_editor("config.yaml")
