import hashlib
import re
import sys
try:
    import pefile
except ImportError:
    pefile = None
try:
    import yara
except ImportError:
    yara = None
    
sample = "Procmon.exe"

# hashing

def compute_hashes(path):
    """Compute MD5, SHA1, and SHA256 for IOC extraction."""
    algos = ["md5", "sha1", "sha256"]
    output = {}
    for a in algos:
        h = hashlib.new(a)
        try:
            with open(path, "rb") as f:
                h.update(f.read())
            output[a] = h.hexdigest()
        except FileNotFoundError:
            output[a] = "File not found"
    return output

# strings
def extract_strings(path):
    """Extract readable ASCII strings (IOC candidates)."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        return re.findall(rb"[ -~]{4,}", data)
    except FileNotFoundError:
        return []

# imports

def list_imports(path):
    """Inspect PE imports to infer capabilities."""
    if not pefile:
        print("pefile module not installed.")
        return {}
    try:
        pe = pefile.PE(path)
        imports = {}
        for entry in getattr(pe, 'DIRECTORY_ENTRY_IMPORT', []):
            dll = entry.dll.decode()
            funcs = [imp.name.decode() if imp.name else "None" for imp in entry.imports]
            imports[dll] = funcs
        return imports
    except FileNotFoundError:
        print("Sample file not found.")
        return {}

# yara rule

def yara_match(path):
    """Apply simple YARA signature to detect HTTP usage."""
    if not yara:
        return "yara module not installed."
    rule_source = """
    rule ContainsHTTP {
        strings: $s = "http"
        condition: $s
    }
    """
    try:
        rules = yara.compile(source=rule_source)
        return rules.match(path)
    except FileNotFoundError:
        return "Sample file not found."

# run all sections 
if __name__ == "__main__":
    print("\n=== HASHES (MD5 / SHA1 / SHA256) ===")
    print(compute_hashes(sample))

    print("\n=== STRINGS (first 20) ===")
    strings = extract_strings(sample)
    if strings:
        for s in strings[:20]:
            print(s.decode(errors="ignore"))
    else:
        print("No strings found or file not found.")

    print("\n=== IMPORTED DLLs & FUNCTIONS ===")
    imports = list_imports(sample)
    if imports:
        for dll, funcs in imports.items():
            print(f"\n{dll}")
            for f in funcs[:5]:
                print(" -", f)
    else:
        print("No imports found or pefile not installed.")

    print("\n=== YARA MATCH RESULT ===")
    print(yara_match(sample))
