#!/usr/bin/env python3
"""
Object Browser - Complete IDE-style object inspection tool
Recursive scope enumeration with save/load capabilities
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import sys
import inspect
import subprocess
import tempfile
from settings_window import SettingsWindow


class ObjectBrowser:
    """Comprehensive object browser with introspection and persistence"""

    def __init__(self, parent=None, settings=None):
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Object Browser")
        self.window.geometry("1400x900")

        # Object tracking
        self.current_object = None
        self.current_object_path = ""
        self.loaded_objects = {}  # Store loaded objects by name
        
        # Load settings
        self.settings = settings or self.load_settings()
        self.apply_settings()
        self.editor_command = self.settings.get('advanced', {}).get('editor_command', 'notepad {filename}')

        self.create_ui()
        self.populate_full_object_tree()

    def load_settings(self):
        """Load settings from file"""
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    return json.load(f)
            except:
                pass
        return {'advanced': {'editor_command': 'notepad {filename}'}}

def open_settings_window(self):
    """Open settings window and bind save/apply behavior."""
    # If already open, focus it
    try:
        if self.settings_win and self.settings_win.window.winfo_exists():
            self.settings_win.window.lift()
            return
    except AttributeError:
        pass

    # Create and keep a ref
    self.settings_win = SettingsWindow(parent=self.window, app_instance=self)

    # Override save button to also apply settings on save
    orig_save = self.settings_win.save_settings

def reload_settings_data(self):
    """Reload settings from file and reapply them."""
    self.settings = self.load_settings()
    self.apply_settings()
    messagebox.showinfo("Settings Applied", "Settings updated and applied to Object Browser.")

def apply_settings(self):
    """Apply settings from self.settings to the layout editor."""
    # Example: update editor command
    self.editor_command = self.settings.get('editor', {}).get('editor_command', self.editor_command)

    # Example: update tree recursion depth
    try:
        max_depth = int(self.settings.get('browser', {}).get('max_depth', 6))
        self.max_depth = max_depth
    except:
        self.max_depth = 6

    # Font size and theme could be applied here too,
    #   e.g. changing fonts on tree/code widgets.

    # (Add more as needed)

    
    def save_and_apply():
        if orig_save():
            # Reload settings in main app
            self.settings = self.settings_win.settings
            self.apply_settings()
            self.reload_settings_data()

    self.settings_win.save_settings = save_and_apply


    
    def create_ui(self):
        """Create main UI"""
        # Top toolbar
        self.create_toolbar()
        
        # Main container
        main_paned = ttk.PanedWindow(self.window, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)

        # Left: Object Browser
        left_panel = ttk.Frame(main_paned, width=500)
        main_paned.add(left_panel, weight=2)
        self.create_object_browser(left_panel)
        
        # Right: Details Panel
        right_panel = ttk.Frame(main_paned, width=900)
        main_paned.add(right_panel, weight=3)
        self.create_detail_panel(right_panel)
        
        # Bottom status bar
        self.create_status_bar()

    def create_toolbar(self):
        """Create top toolbar"""
        toolbar = ttk.Frame(self.window)
        toolbar.pack(fill=tk.X, padx=5, pady=2)
        
        # Object operations
        ttk.Button(toolbar, text="🔄 Refresh", command=self.populate_full_object_tree).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📝 View Source", command=self.edit_current_object).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        
        # File operations
        ttk.Button(toolbar, text="💾 Save Code", command=self.save_code).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Load Code", command=self.load_code).pack(side=tk.LEFT, padx=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, padx=5, fill=tk.Y)
        ttk.Button(toolbar, text="⚙️ Settings", command=self.open_settings_window).pack(side=tk.LEFT, padx=2)
        
        # Title
        title_label = ttk.Label(toolbar, text="🧠 Object Browser", 
                               font=("Arial", 10, "bold"), foreground="blue")
        title_label.pack(side=tk.RIGHT, padx=10)

    def create_object_browser(self, parent):
        """Create object browser panel"""
        # Title
        ttk.Label(parent, text="Object Hierarchy", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Search bar
        search_frame = ttk.Frame(parent)
        search_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT)
        self.obj_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.obj_search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        search_entry.bind("<KeyRelease>", self.filter_object_tree)
        ttk.Button(search_frame, text="Clear", command=lambda: self.obj_search_var.set("")).pack(side=tk.LEFT, padx=2)
        
        # Tree widget
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.object_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
        self.object_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.object_tree.yview)
        self.object_tree.bind("<<TreeviewSelect>>", self.on_object_selected)

    def create_detail_panel(self, parent):
        """Create detail panel with tabs"""
        # Notebook for different views
        self.detail_notebook = ttk.Notebook(parent)
        self.detail_notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Tab 1: Members (Properties/Methods)
        members_frame = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(members_frame, text="📊 Members")
        
        members_scroll = ttk.Scrollbar(members_frame)
        members_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.members_tree = ttk.Treeview(members_frame, yscrollcommand=members_scroll.set,
                                        columns=("type", "value"), show="tree headings")
        self.members_tree.heading("#0", text="Name")
        self.members_tree.heading("type", text="Type")
        self.members_tree.heading("value", text="Value")
        self.members_tree.column("#0", width=250)
        self.members_tree.column("type", width=150)
        self.members_tree.column("value", width=400)
        self.members_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        members_scroll.config(command=self.members_tree.yview)
        
        # Tab 2: Code View
        code_frame = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(code_frame, text="📝 Code")
        
        self.code_viewer = scrolledtext.ScrolledText(code_frame, font=("Courier", 10), wrap=tk.NONE)
        self.code_viewer.pack(fill=tk.BOTH, expand=True)
        
        # Syntax highlighting tags
        self.code_viewer.tag_config("keyword", foreground="blue", font=("Courier", 10, "bold"))
        self.code_viewer.tag_config("string", foreground="green")
        self.code_viewer.tag_config("comment", foreground="gray", font=("Courier", 10, "italic"))
        self.code_viewer.tag_config("function", foreground="purple", font=("Courier", 10, "bold"))
        
        # Tab 3: Object Info
        info_frame = ttk.Frame(self.detail_notebook)
        self.detail_notebook.add(info_frame, text="ℹ️ Info")
        
        self.info_text = scrolledtext.ScrolledText(info_frame, font=("Courier", 10), wrap=tk.WORD)
        self.info_text.pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        """Create bottom status bar"""
        self.status_bar = ttk.Frame(self.window, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_text = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.status_bar, textvariable=self.status_text, 
                                     font=("Courier", 9), anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=2)

    def update_status(self, obj_path="", obj_type="", source_file="", line_num=""):
        """Update status bar with object information"""
        if obj_path:
            status = f"{obj_path} ({obj_type})"
            if source_file:
                status += f" | {source_file}"
                if line_num:
                    status += f":{line_num}"
            self.status_text.set(status)
        else:
            self.status_text.set("Ready")

    def populate_full_object_tree(self):
        """Recursively populate object tree with full program state"""
        # Clear tree
        for item in self.object_tree.get_children():
            self.object_tree.delete(item)
        
        # Root: ObjectBrowser instance
        root_id = self.object_tree.insert("", "end", text="ObjectBrowser (self)", 
                                         values=("ObjectBrowser", "self", __file__, ""))
        
        # Enumerate all attributes recursively
        self._enumerate_object(self, root_id, "self", depth=0, max_depth=6)
        
        # Add loaded objects section
        if self.loaded_objects:
            loaded_id = self.object_tree.insert("", "end", text=f"📦 Loaded Objects ({len(self.loaded_objects)})",
                                                values=("dict", "self.loaded_objects", "", ""))
            for name, obj in self.loaded_objects.items():
                obj_type = type(obj).__name__
                obj_id = self.object_tree.insert(loaded_id, "end", text=f"{name}: {obj_type}",
                                                values=(obj_type, f"self.loaded_objects['{name}']", "", ""))
                self._enumerate_object(obj, obj_id, f"self.loaded_objects['{name}']", depth=0, max_depth=6)
            self.object_tree.item(loaded_id, open=True)
        
        # Expand root
        self.object_tree.item(root_id, open=True)

    def _enumerate_object(self, obj, parent_id, obj_name, depth=0, max_depth=6):
        """Recursively enumerate object attributes"""
        if depth >= max_depth:
            return
        
        try:
            obj_type = type(obj).__name__
            
            # Handle different types
            if isinstance(obj, dict):
                for key, value in obj.items():
                    key_str = str(key)
                    val_type = type(value).__name__
                    node_text = f"🔑 {key_str}: {val_type}"
                    
                    # Value preview
                    try:
                        if isinstance(value, (str, int, float, bool)):
                            preview = repr(value)[:50]
                            node_text += f" = {preview}"
                    except:
                        pass
                    
                    child_id = self.object_tree.insert(parent_id, "end", text=node_text,
                                                      values=(val_type, f"{obj_name}[{repr(key)}]", "", ""))
                    
                    # Recurse into complex values
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        self._enumerate_object(value, child_id, f"{obj_name}[{repr(key)}]", depth + 1, max_depth)
            
            elif isinstance(obj, (list, tuple)):
                for idx, value in enumerate(obj):
                    val_type = type(value).__name__
                    node_text = f"[{idx}]: {val_type}"
                    
                    try:
                        if isinstance(value, (str, int, float, bool)):
                            preview = repr(value)[:50]
                            node_text += f" = {preview}"
                    except:
                        pass
                    
                    child_id = self.object_tree.insert(parent_id, "end", text=node_text,
                                                      values=(val_type, f"{obj_name}[{idx}]", "", ""))
                    
                    if not isinstance(value, (str, int, float, bool, type(None))):
                        self._enumerate_object(value, child_id, f"{obj_name}[{idx}]", depth + 1, max_depth)
            
            else:
                # Enumerate attributes
                for attr_name in dir(obj):
                    # Skip private at deeper levels
                    if depth > 0 and attr_name.startswith('_'):
                        continue
                    
                    try:
                        attr_value = getattr(obj, attr_name)
                        attr_type = type(attr_value).__name__
                        
                        # Icon/prefix
                        if callable(attr_value):
                            prefix = "⚙️"
                        elif isinstance(attr_value, (str, int, float, bool)):
                            prefix = "📊"
                        elif isinstance(attr_value, dict):
                            prefix = "📁"
                        elif isinstance(attr_value, (list, tuple)):
                            prefix = "📋"
                        else:
                            prefix = "●"
                        
                        node_text = f"{prefix} {attr_name}: {attr_type}"
                        
                        # Value preview for simple types
                        if isinstance(attr_value, (str, int, float, bool)):
                            preview = repr(attr_value)[:50]
                            node_text += f" = {preview}"
                        
                        child_id = self.object_tree.insert(parent_id, "end", text=node_text,
                                                          values=(attr_type, f"{obj_name}.{attr_name}", "", ""))
                        
                        # Recurse into complex attributes
                        if not isinstance(attr_value, (str, int, float, bool, type(None))) and not callable(attr_value):
                            if isinstance(attr_value, (dict, list, tuple)) or hasattr(attr_value, '__dict__'):
                                self._enumerate_object(attr_value, child_id, f"{obj_name}.{attr_name}", depth + 1, max_depth)
                    
                    except:
                        pass
        except:
            pass

    def on_object_selected(self, event=None):
        """Handle object tree selection"""
        selection = self.object_tree.selection()
        if not selection:
            return
        
        values = self.object_tree.item(selection[0], "values")
        if not values:
            return
        
        obj_type = values[0]
        obj_path = values[1]
        
        self.current_object_path = obj_path
        
        # Update status bar
        self.update_status(obj_path, obj_type, __file__, "")
        
        # Try to get the actual object
        try:
            obj = eval(obj_path)
            self.current_object = obj
            
            # Update all tabs
            self.populate_members(obj)
            self.show_object_code(obj, obj_type, obj_path)
            self.show_object_info(obj, obj_type, obj_path)
        
        except Exception as e:
            print(f"Error accessing object: {e}")

    def populate_members(self, obj):
        """Populate members tree"""
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        
        # Properties section
        props_id = self.members_tree.insert("", "end", text="📊 Properties", values=("", ""))
        
        # Methods section
        methods_id = self.members_tree.insert("", "end", text="⚙️ Methods", values=("", ""))
        
        # Special section
        special_id = self.members_tree.insert("", "end", text="🔮 Special/Magic", values=("", ""))
        
        try:
            for attr_name in dir(obj):
                try:
                    attr_value = getattr(obj, attr_name)
                    attr_type = type(attr_value).__name__
                    
                    if callable(attr_value):
                        # Method
                        sig = ""
                        try:
                            sig = str(inspect.signature(attr_value))
                        except:
                            sig = "()"
                        
                        # Special/magic methods
                        if attr_name.startswith('__') and attr_name.endswith('__'):
                            self.members_tree.insert(special_id, "end", text=f"{attr_name}{sig}",
                                                    values=(attr_type, "magic method"))
                        else:
                            self.members_tree.insert(methods_id, "end", text=f"{attr_name}{sig}",
                                                    values=(attr_type, "method"))
                    else:
                        # Property
                        value_preview = ""
                        try:
                            if isinstance(attr_value, (str, int, float, bool)):
                                value_preview = repr(attr_value)[:100]
                            else:
                                value_preview = f"<{attr_type}>"
                        except:
                            value_preview = "<e>"
                        
                        # Special/magic attributes
                        if attr_name.startswith('__') and attr_name.endswith('__'):
                            self.members_tree.insert(special_id, "end", text=attr_name,
                                                    values=(attr_type, value_preview))
                        else:
                            self.members_tree.insert(props_id, "end", text=attr_name,
                                                    values=(attr_type, value_preview))
                except:
                    pass
        except:
            pass
        
        # Expand sections
        self.members_tree.item(props_id, open=True)
        self.members_tree.item(methods_id, open=True)

    def show_object_code(self, obj, obj_type, obj_path):
        """Show code for object"""
        self.code_viewer.delete("1.0", tk.END)
        
        code = f"# Object: {obj_path}\n"
        code += f"# Type: {obj_type}\n"
        code += f"# ID: {id(obj)}\n\n"
        
        # Try to get source code
        try:
            if inspect.isclass(type(obj)) or inspect.isfunction(obj) or inspect.ismethod(obj):
                source = inspect.getsource(obj if callable(obj) else type(obj))
                code += source
            else:
                # Show repr
                code += f"# Value:\n{repr(obj)}\n"
        except Exception as e:
            code += f"# Could not retrieve source code\n# {str(e)}\n"
        
        self.code_viewer.insert("1.0", code)
        self.apply_syntax_highlighting()

    def show_object_info(self, obj, obj_type, obj_path):
        """Show detailed object information"""
        self.info_text.delete("1.0", tk.END)
        
        info = f"Object Information\n{'='*60}\n\n"
        info += f"Path:     {obj_path}\n"
        info += f"Type:     {obj_type}\n"
        info += f"ID:       {id(obj)}\n"
        info += f"Module:   {type(obj).__module__}\n"
        
        # Size info
        try:
            size = sys.getsizeof(obj)
            info += f"Size:     {size:,} bytes\n"
        except:
            pass
        
        # MRO for classes
        try:
            mro = type(obj).__mro__
            info += f"\nMethod Resolution Order:\n"
            for i, cls in enumerate(mro):
                info += f"  {i}. {cls.__name__}\n"
        except:
            pass
        
        # Doc string
        try:
            doc = inspect.getdoc(obj) or inspect.getdoc(type(obj))
            if doc:
                info += f"\nDocumentation:\n{'-'*60}\n{doc}\n"
        except:
            pass
        
        # Source file
        try:
            source_file = inspect.getsourcefile(type(obj))
            if source_file:
                info += f"\nSource File:\n{source_file}\n"
        except:
            pass
        
        self.info_text.insert("1.0", info)

    def apply_syntax_highlighting(self):
        """Apply basic syntax highlighting"""
        keywords = ['def', 'class', 'import', 'from', 'if', 'else', 'elif', 'for', 'while', 
                   'return', 'try', 'except', 'with', 'as', 'pass', 'break', 'continue', 'lambda']
        
        for keyword in keywords:
            start = "1.0"
            while True:
                pos = self.code_viewer.search(f"\\m{keyword}\\M", start, tk.END, regexp=True)
                if not pos:
                    break
                end = f"{pos}+{len(keyword)}c"
                self.code_viewer.tag_add("keyword", pos, end)
                start = end

    def edit_current_object(self):
        """Open current object's source in external editor"""
        if not self.current_object:
            messagebox.showwarning("No Selection", 
                "Please select an object from the Object Browser first.\n\n"
                "Click on any item in the tree to select it.")
            return
        
        obj_type = type(self.current_object).__name__
        obj_path = self.current_object_path
        
        try:
            source_file = None
            line_num = None
            
            # Strategy 1: Try to get source file from the object itself
            try:
                if callable(self.current_object):
                    # It's a function/method
                    source_file = inspect.getsourcefile(self.current_object)
                    try:
                        _, line_num = inspect.getsourcelines(self.current_object)
                    except:
                        pass
                else:
                    # Try to get from its class
                    source_file = inspect.getsourcefile(type(self.current_object))
            except (TypeError, AttributeError):
                pass
            
            # Strategy 2: Check if it's a built-in type
            if not source_file or '<' in str(source_file) or '>' in str(source_file):
                if type(self.current_object).__module__ in ('builtins', '__builtin__'):
                    messagebox.showinfo("Built-in Object",
                        f"Cannot view source for built-in objects.\n\n"
                        f"Object: {obj_path}\n"
                        f"Type: {obj_type}\n"
                        f"Module: {type(self.current_object).__module__}\n\n"
                        f"💡 Built-in objects are implemented in C, not Python.\n"
                        f"Check the Code tab for available information.")
                    return
            
            # Strategy 3: For simple data types, show in temp file
            if not source_file and isinstance(self.current_object, (str, int, float, bool, dict, list, tuple, bytes)):
                # Create temporary file with the object's representation
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(f"# Object: {obj_path}\n")
                    f.write(f"# Type: {obj_type}\n")
                    f.write(f"# Generated temporary view\n\n")
                    
                    if isinstance(self.current_object, str):
                        f.write(f"# String value ({len(self.current_object)} characters):\n")
                        f.write(repr(self.current_object))
                    elif isinstance(self.current_object, (dict, list, tuple)):
                        f.write(f"# {obj_type} value:\n")
                        f.write(json.dumps(self.current_object, indent=2, default=str))
                    else:
                        f.write(f"# Value:\n")
                        f.write(repr(self.current_object))
                    
                    source_file = f.name
                
                messagebox.showinfo("Temporary View",
                    f"Opening temporary view of data object.\n\n"
                    f"Type: {obj_type}\n"
                    f"Temp file: {os.path.basename(source_file)}\n\n"
                    f"⚠️ This is a read-only representation.\n"
                    f"Changes will not affect the original object.")
            
            # Strategy 4: For Tkinter widgets, show informational message
            if not source_file and isinstance(self.current_object, (tk.Widget, ttk.Widget)):
                messagebox.showinfo("GUI Widget",
                    f"GUI widgets don't have viewable Python source.\n\n"
                    f"Widget: {obj_path}\n"
                    f"Type: {obj_type}\n\n"
                    f"💡 Check the Members tab to explore widget properties\n"
                    f"and methods, or view the code that created it.")
                return
            
            # Strategy 5: Last resort - if still no file, show error
            if not source_file or not os.path.exists(source_file):
                messagebox.showwarning("No Source File",
                    f"Cannot find source file for this object.\n\n"
                    f"Object: {obj_path}\n"
                    f"Type: {obj_type}\n"
                    f"Module: {type(self.current_object).__module__}\n\n"
                    f"Possible reasons:\n"
                    f"• Object created dynamically at runtime\n"
                    f"• Object from a compiled extension\n"
                    f"• Source file location unknown\n\n"
                    f"💡 Check the Code and Info tabs for details.")
                return
            
            # Open in external editor
            cmd = self.editor_command.format(filename=source_file)
            subprocess.Popen(cmd, shell=True)
            
            status_msg = f"Opened: {os.path.basename(source_file)}"
            if line_num:
                status_msg += f" (line {line_num})"
            self.update_status(status_msg, "", "", "")
        
        except subprocess.SubprocessError as e:
            messagebox.showerror("Editor Error",
                f"Failed to launch external editor.\n\n"
                f"Command: {self.editor_command}\n"
                f"Error: {str(e)}\n\n"
                f"💡 Check Settings to configure your editor.")
        
        except Exception as e:
            messagebox.showerror("Error",
                f"Unexpected error opening source.\n\n"
                f"Error: {type(e).__name__}\n"
                f"Details: {str(e)}")

    def save_code(self):
        """Save current code view to a .py file"""
        # Get content from code viewer
        content = self.code_viewer.get("1.0", tk.END).strip()
        
        if not content:
            messagebox.showwarning("No Content",
                "The Code tab is empty.\n\n"
                "Select an object to view its source code first.")
            return
        
        # Default filename based on current object
        default_name = "code.py"
        if self.current_object_path:
            # Extract a reasonable filename from the path
            path_parts = self.current_object_path.replace('[', '_').replace(']', '_').replace("'", "").split('.')
            if path_parts:
                default_name = f"{path_parts[-1]}.py"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Code",
            initialfile=default_name
        )
        
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            file_size = os.path.getsize(filename)
            line_count = content.count('\n') + 1
            
            messagebox.showinfo("✓ Code Saved",
                f"Code saved successfully!\n\n"
                f"File: {os.path.basename(filename)}\n"
                f"Size: {file_size:,} bytes\n"
                f"Lines: {line_count:,}\n\n"
                f"Full path:\n{filename}")
            
            self.update_status(f"Saved: {os.path.basename(filename)}", "", "", "")
        
        except IOError as e:
            messagebox.showerror("Save Error",
                f"Cannot write to file!\n\n"
                f"File: {filename}\n"
                f"Error: {str(e)}\n\n"
                f"💡 Check:\n"
                f"• File is not open in another program\n"
                f"• You have write permissions\n"
                f"• Disk is not full")
        
        except Exception as e:
            messagebox.showerror("Error",
                f"Failed to save file!\n\n"
                f"Error: {type(e).__name__}\n"
                f"Details: {str(e)}")

    def load_code(self):
        """Load a .py file and display it in the code viewer"""
        filename = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py"), ("Text files", "*.txt"), ("All files", "*.*")],
            title="Load Python Code"
        )
        
        if not filename:
            return
        
        # Check file exists and is readable
        if not os.path.exists(filename):
            messagebox.showerror("File Not Found",
                f"File does not exist!\n\n{filename}")
            return
        
        if not os.access(filename, os.R_OK):
            messagebox.showerror("Permission Denied",
                f"Cannot read file!\n\n{filename}")
            return
        
        file_size = os.path.getsize(filename)
        
        # Warn about large files
        if file_size > 1024 * 1024:  # 1 MB
            result = messagebox.askyesno("Large File",
                f"This file is {file_size:,} bytes.\n\n"
                f"Loading large files may be slow.\n\n"
                f"Continue?")
            if not result:
                return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Clear current object selection
            self.current_object = None
            self.current_object_path = f"Loaded: {os.path.basename(filename)}"
            
            # Display in code viewer
            self.code_viewer.delete("1.0", tk.END)
            self.code_viewer.insert("1.0", content)
            self.apply_syntax_highlighting()
            
            # Switch to code tab
            self.detail_notebook.select(1)  # Index 1 is Code tab
            
            # Clear members and info
            for item in self.members_tree.get_children():
                self.members_tree.delete(item)
            self.info_text.delete("1.0", tk.END)
            
            line_count = content.count('\n') + 1
            
            messagebox.showinfo("✓ Code Loaded",
                f"Python file loaded!\n\n"
                f"File: {os.path.basename(filename)}\n"
                f"Size: {file_size:,} bytes\n"
                f"Lines: {line_count:,}\n\n"
                f"The code is displayed in the Code tab.\n"
                f"You can now save it or view it.")
            
            self.update_status(f"Loaded: {os.path.basename(filename)}", "", filename, "")
        
        except UnicodeDecodeError:
            messagebox.showerror("Encoding Error",
                f"Cannot read file!\n\n"
                f"File: {os.path.basename(filename)}\n\n"
                f"The file is not a valid UTF-8 text file.\n"
                f"It may be binary or use a different encoding.")
        
        except IOError as e:
            messagebox.showerror("Read Error",
                f"Cannot read file!\n\n"
                f"File: {filename}\n"
                f"Error: {str(e)}")
        
        except MemoryError:
            messagebox.showerror("Out of Memory",
                f"File is too large!\n\n"
                f"Size: {file_size:,} bytes\n\n"
                f"Try a smaller file.")
        
        except Exception as e:
            messagebox.showerror("Load Error",
                f"Failed to load file!\n\n"
                f"File: {os.path.basename(filename)}\n"
                f"Error: {type(e).__name__}\n"
                f"Details: {str(e)}")

    def filter_object_tree(self, event=None):
        """Filter object tree based on search"""
        query = self.obj_search_var.get().lower()
        if not query:
            self.populate_full_object_tree()
            return
        
        def search_tree(item):
            text = self.object_tree.item(item, "text").lower()
            children = self.object_tree.get_children(item)
            
            match = query in text
            child_match = False
            
            for child in children:
                if search_tree(child):
                    child_match = True
            
            if match or child_match:
                self.object_tree.item(item, open=True)
                return True
            return False
        
        for item in self.object_tree.get_children():
            search_tree(item)

    def reload_settings(self):
        """Reload settings from file"""
        self.settings = self.load_settings()
        self.editor_command = self.settings.get('advanced', {}).get('editor_command', 'notepad {filename}')
        messagebox.showinfo("Settings Reloaded", "Settings have been reloaded from file")


def main():
    """Run the Object Browser"""
    app = ObjectBrowser()
    app.window.mainloop()


if __name__ == "__main__":
    main()
