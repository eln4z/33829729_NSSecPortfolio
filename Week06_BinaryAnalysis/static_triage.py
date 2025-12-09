import hashlib, pefile, re, yara

# ⚠️ Update path if your file is somewhere else
sample = "Procmon.exe"

# --------------------- HASHING ---------------------

def compute_hashes(path):
    """Compute MD5, SHA1, and SHA256 for IOC extraction."""
    algos = ["md5", "sha1", "sha256"]
    output = {}
    for a in algos:
        h = hashlib.new(a)
        with open(path, "rb") as f:
            h.update(f.read())
        output[a] = h.hexdigest()
    return output

# --------------------- STRINGS ---------------------

def extract_strings(path):
    """Extract readable ASCII strings (IOC candidates)."""
    with open(path, "rb") as f:
        data = f.read()
    return re.findall(rb"[ -~]{4,}", data)

# --------------------- PE HEADER / IMPORTS ---------------------

def list_imports(path):
    """Inspect PE imports to infer capabilities."""
    pe = pefile.PE(path)
    imports = {}
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode()
        funcs = [imp.name.decode() if imp.name else "None" for imp in entry.imports]
        imports[dll] = funcs
    return imports

# --------------------- YARA RULE ---------------------

def yara_match(path):
    """Apply simple YARA signature to detect HTTP usage."""
    rule_source = """
    rule ContainsHTTP {
        strings: $s = "http"
        condition: $s
    }
    """
    rules = yara.compile(source=rule_source)
    return rules.match(path)

# --------------------- RUN ALL SECTIONS ---------------------

if __name__ == "__main__":
    print("\n=== HASHES (MD5 / SHA1 / SHA256) ===")
    print(compute_hashes(sample))

    print("\n=== STRINGS (first 20) ===")
    strings = extract_strings(sample)
    for s in strings[:20]:
        print(s.decode(errors="ignore"))

    print("\n=== IMPORTED DLLs & FUNCTIONS ===")
    imports = list_imports(sample)
    for dll, funcs in imports.items():
        print(f"\n{dll}")
        for f in funcs[:5]:
            print(" -", f)

    print("\n=== YARA MATCH RESULT ===")
    print(yara_match(sample))
