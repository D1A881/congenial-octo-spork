# Congenial-Octo-Spork (Object Browser) — Python GUI Introspection & Editor Tool

**Congenial-Octo-Spork** is a standalone Tkinter-based application for exploring, inspecting, and saving Python objects at runtime. It offers an IDE-style interface that lets you:

* Browse object hierarchies recursively
* View properties, methods, and metadata
* Inspect source code and documentation
* Save and load objects in Python or binary formats
* Edit source files in an external editor

This is ideal for debugging, learning, or analyzing complex Python applications.

---

## 🧠 Features

### 🔎 Object Explorer

* Displays the full object hierarchy of the running program
* Supports nested structures (modules, classes, instances, dicts, lists, etc.)
* Recursively expands children up to a configurable depth
* Provides search filtering to locate specific object paths
* Yes, congenial-octo-spork was indeed randomly chosen by github!



---

### 📋 Detailed Views

#### **Members Tab**

Shows all accessible attributes of the selected object:

* Properties (values)
* Methods (callable signatures)
* Special and magic methods

#### **Code Tab**

Displays source code or object representation:

* Extracts Python source when available (functions, classes)
* Highlights syntax for keywords, strings, comments, and functions

#### **Info Tab**

Detailed metadata including:

* Object type and path
* Memory size
* Module and class info
* Method Resolution Order (MRO)
* Docstrings

---

### 💾 Persistence

Save and load objects using:

* **Python pickle** format
* **Binary serialization**
* Standard file dialogs with error handling

Warning dialogs prevent you from pickling unsupported Tkinter widgets.

---

### ✏️ External Editing

Open the source file of the selected object in your favorite editor using a customizable launch command (e.g., `notepad {filename}`).

---

## 📦 Getting Started

### Requirements

* Python 3.x
* Tkinter (included with standard Python installs) ([Wikipedia][1])

No third-party libraries are required.

---

### Running the Tool

```bash
python3 layout_editor.py
```

or on Windows:

```bash
python layout_editor.py
```

Once launched, you can explore objects by clicking any entry in the tree view on the left.

---

## 📂 UI Overview

| Section         | Description                                     |
| --------------- | ----------------------------------------------- |
| **Object Tree** | Left pane that lists all discoverable objects   |
| **Search Bar**  | Filter object tree by name                      |
| **Detail Tabs** | View members, code, and object metadata         |
| **Toolbar**     | Refresh, edit code, load/save objects, settings |
| **Status Bar**  | Shows object path, type, file location, etc.    |

---

## ⚙️ Configuration

Settings are stored (and reloaded) from:

```
settings.json
```

This currently supports customizing the external editor command:

```json
{
  "advanced": {
    "editor_command": "code {filename}"
  }
}
```

---

## 📌 Typical Use Cases

* **Runtime debugging** of object states
* **Exploration** of unfamiliar libraries or modules
* **Learning tool** for Python introspection
* **Quick access** to source code and docs

---

## 🛠️ Notes & Limitations

* Cannot serialize (pickle) Tkinter GUI widgets
* Source retrieval may not work for built-ins or certain compiled modules
* For best results, open files that exist on disk

---

## 📜 License & Attribution
GNU GPL V2
