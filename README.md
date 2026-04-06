# TFTOS

TFTOS is a protected mini-OS. Just run it and enjoy!

## Disturbsions

A **disturbsion** is a custom command you can add to TFTOS.  
You **cannot modify the core system**, but you **can add new commands**.

### How to create a disturbsion:

1. Download TFTOS.
2. Go to `Root/System/Commands` on your PC.
3. Create a Python file with the following syntax:

```python
# Usage: hello
def run(args, current_dir):
    print("Hello from disturbsion!")
#SystemGen:1b-TRUE
```
License:
TFTOS™ Copyright 2026 VeresNoémi
All rights reserved.

Permission is granted to:
- Run this software.
- Create new commands in Root/System/Commands folder.
- Publish as a disturbsion

Prohibited:
- Modifying the core system files.
- Using the modified software to create a competing OS.

Violation may result in legal action.
