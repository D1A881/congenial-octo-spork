import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from settings_window import SettingsWindow


class ObjectBrowser:
    """Layout Editor / Object Browser"""

    def __init__(self, root, settings=None):
        self.window = root
        self.window.title("Layout Editor")

        # Load settings
        self.settings = settings or self.load_settings()
        self.settings_win = None

        # Apply loaded settings
        self.apply_settings()

        # Build UI
        self.create_ui()

    # ---------------------------------------------------------
    # UI CREATION
    # ---------------------------------------------------------

    def create_ui(self):
        toolbar = ttk.Frame(self.window)
        toolbar.pack(fill=tk.X)

        ttk.Button(
            toolbar,
            text="⚙️ Settings",
            command=self.open_settings_window
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            toolbar,
            text="Reload Settings",
            command=self.reload_settings
        ).pack(side=tk.LEFT, padx=2)

        # Example content area
        self.content = tk.Text(self.window)
        self.content.pack(fill=tk.BOTH, expand=True)

    # ---------------------------------------------------------
    # SETTINGS WINDOW INTEGRATION
    # ---------------------------------------------------------

    def open_settings_window(self):
        """Open settings window and bind save/apply behavior."""

        # Prevent multiple instances
        if self.settings_win and self.settings_win.window.winfo_exists():
            self.settings_win.window.lift()
            return

        # Create settings window
        self.settings_win = SettingsWindow(
            parent=self.window,
            app_instance=self
        )

        # Pass a deep copy so edits don't modify main settings until saved
        self.settings_win.settings = json.loads(json.dumps(self.settings))
        self.settings_win.populate_tree()

        # Wrap original save function
        original_save = self.settings_win.save_settings

        def save_and_apply():
            if original_save():
                self.settings = self.settings_win.settings
                self.apply_settings()
                self.reload_settings_data()
            return True

        self.settings_win.save_settings = save_and_apply

    def apply_settings(self):
        """Apply settings to the layout editor."""

        # Example: editor command
        self.editor_command = self.settings.get(
            "editor", {}
        ).get("editor_command", "notepad")

        # Example: browser max depth
        try:
            self.max_depth = int(
                self.settings.get("browser", {}).get("max_depth", 6)
            )
        except Exception:
            self.max_depth = 6

        # Example: font size
        font_size = self.settings.get("appearance", {}).get("font_size", 10)
        try:
            self.content.configure(font=("Consolas", int(font_size)))
        except Exception:
            self.content.configure(font=("Consolas", 10))

        # Example: theme placeholder
        theme = self.settings.get("appearance", {}).get("theme", "default")
        # You can expand this for ttk theme switching

    def reload_settings_data(self):
        """Reload settings from file and reapply."""
        self.settings = self.load_settings()
        self.apply_settings()
        messagebox.showinfo(
            "Settings Applied",
            "Settings updated and applied."
        )

    # ---------------------------------------------------------
    # SETTINGS FILE HANDLING
    # ---------------------------------------------------------

    def load_settings(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def reload_settings(self):
        self.settings = self.load_settings()
        self.apply_settings()
        messagebox.showinfo(
            "Settings Reloaded",
            "Settings reloaded successfully."
        )


# ---------------------------------------------------------
# RUN STANDALONE
# ---------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectBrowser(root)
    root.mainloop()
