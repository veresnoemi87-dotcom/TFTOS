import os
import importlib.util
import subprocess
import sys

# Enable ANSI colors on Windows
os.system("")

# =========================
# PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "Root")
SYSTEM_CMD_DIR = os.path.join(ROOT_DIR, "System", "Commands")

current_dir = ROOT_DIR

os.makedirs(SYSTEM_CMD_DIR, exist_ok=True)

# =========================
# PROTECTION CHECK
# =========================
def is_protected(path):
    try:
        with open(path, "r") as f:
            return f.read().strip().endswith("#SystemGen:1b-TRUE")
    except:
        return False

# =========================
# AUTO CREATE SYSTEM FILES
# =========================
def create_system_files():

    commands = {

        "ls.py": '''# Usage: ls
def run(args, current_dir):
    import os

    BLUE = "\\033[94m"
    RESET = "\\033[0m"

    files = os.listdir(current_dir)

    if not files:
        print("Empty folder.")
        return

    for f in files:
        path = os.path.join(current_dir, f)

        if os.path.isdir(path):
            print(f"{BLUE}{f}{RESET}")
        else:
            print(f)
''',

        "mkdir.py": '''# Usage: mkdir [foldername]
def run(args, current_dir):
    import os
    if len(args) < 1:
        print("Usage: mkdir [foldername]")
        return
    path = os.path.join(current_dir, args[0])
    if os.path.exists(path):
        print(f"Error: '{args[0]}' already exists.")
        return
    os.makedirs(path)
    print(f"Folder '{args[0]}' created.")
''',

        "make.py": '''# Usage: make [filename] "[content]"
def run(args, current_dir):
    import os

    def is_protected(path):
        try:
            with open(path, "r") as f:
                return f.read().strip().endswith("#SystemGen:1b-TRUE")
        except:
            return False

    if len(args) < 2:
        print('Usage: make [filename] "[content]"')
        return

    filename = args[0]
    content = " ".join(args[1:])
    path = os.path.join(current_dir, filename)

    if os.path.exists(path):
        if is_protected(path):
            print("Access denied: protected system file.")
            return
        print(f"Error: '{filename}' already exists.")
        return

    with open(path, "w") as f:
        f.write(content)

    print(f"{filename} created.")
''',

        "del.py": '''# Usage: del [filename]
def run(args, current_dir):
    import os

    def is_protected(path):
        try:
            with open(path, "r") as f:
                return f.read().strip().endswith("#SystemGen:1b-TRUE")
        except:
            return False

    if len(args) < 1:
        print("Usage: del [filename]")
        return

    path = os.path.join(current_dir, args[0])

    if not os.path.exists(path):
        print("File not found.")
        return

    if os.path.isdir(path):
        print("Use mkdel for folders.")
        return

    if is_protected(path):
        print("Access denied: protected system file.")
        return

    os.remove(path)
    print(f"{args[0]} deleted.")
''',

        "mkdel.py": '''# Usage: mkdel [foldername]
def run(args, current_dir):
    import os, shutil

    def contains_protected(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, "r") as f:
                        if f.read().strip().endswith("#SystemGen:1b-TRUE"):
                            return True
                except:
                    pass
        return False

    if len(args) < 1:
        print("Usage: mkdel [foldername]")
        return

    path = os.path.join(current_dir, args[0])

    if not os.path.exists(path):
        print("Folder not found.")
        return

    if not os.path.isdir(path):
        print("Not a folder.")
        return

    if contains_protected(path):
        print("Access denied: folder contains protected files.")
        return

    shutil.rmtree(path)
    print(f"{args[0]} deleted.")
''',

        "run.py": '''# Usage: run [file.py]
def run(args, current_dir):
    import os, subprocess, sys

    if len(args) < 1:
        print("Usage: run [file.py]")
        return

    path = os.path.join(current_dir, args[0])

    if not os.path.exists(path):
        print("File not found.")
        return

    subprocess.run([sys.executable, path])
'''
    }

    # 🔥 ALWAYS overwrite to enforce protection
    for name, code in commands.items():
        path = os.path.join(SYSTEM_CMD_DIR, name)
        final_code = code.strip() + "\n\n#SystemGen:1b-TRUE"
        with open(path, "w") as f:
            f.write(final_code)

create_system_files()

# =========================
# MODULE LOADER
# =========================
def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# =========================
# HELP COMMAND
# =========================
def show_help():
    print("\nCommands:\n")
    for file in os.listdir(SYSTEM_CMD_DIR):
        if file.endswith(".py"):
            path = os.path.join(SYSTEM_CMD_DIR, file)
            with open(path, "r") as f:
                line = f.readline().strip()
            name = file.replace(".py", "")
            if line.startswith("#"):
                print(f"{name} → {line[1:]}")
            else:
                print(name)

# =========================
# COMMAND RUNNER
# =========================
def run_command(command, args):
    global current_dir

    if command == "cd":
        if not args:
            print("Usage: cd [folder]")
            return
        if args[0] == "..":
            current_dir = os.path.dirname(current_dir)
        else:
            new = os.path.join(current_dir, args[0])
            if os.path.isdir(new):
                current_dir = new
            else:
                print("Folder not found")
        return

    if command == "help":
        show_help()
        return

    file_path = os.path.join(SYSTEM_CMD_DIR, command + ".py")

    if not os.path.exists(file_path):
        print("Command not found")
        return

    try:
        module = load_module(file_path, command)
        module.run(args, current_dir)
    except Exception as e:
        print("Error:", e)

# =========================
# TERMINAL
# =========================
def terminal():
    print("Welcome to TFTOS! Try help if started")

    while True:
        rel = os.path.relpath(current_dir, ROOT_DIR)
        prompt = "Root" if rel == "." else f"Root/{rel}"

        cmd = input(f"{prompt} >>> ").strip()

        if cmd == "exit":
            break
        if not cmd:
            continue

        parts = cmd.split()
        run_command(parts[0], parts[1:])

terminal()