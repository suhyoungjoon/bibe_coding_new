import subprocess, tempfile, os, textwrap

FORBIDDEN = ["import os", "import subprocess", "open(", "shutil", "socket", "sys.exit", "input("]

def _blocked(code: str):
    return any(x in code for x in FORBIDDEN)

def run_python(code: str):
    if _blocked(code):
        return {"ok": False, "error": "Forbidden API in code"}
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code); path = f.name
    try:
        out = subprocess.check_output(["python", path], stderr=subprocess.STDOUT, timeout=10)
        return {"ok": True, "stdout": out.decode()}
    except subprocess.CalledProcessError as e:
        return {"ok": False, "stdout": e.output.decode()}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        try: os.unlink(path)
        except Exception: pass

def run_javac(src: str, classname="Main"):
    if _blocked(src):
        return {"ok": False, "error": "Forbidden API in code"}
    with tempfile.TemporaryDirectory() as d:
        java_path = os.path.join(d, f"{classname}.java")
        open(java_path,"w").write(src)
        try:
            subprocess.check_output(["javac", java_path], stderr=subprocess.STDOUT, timeout=20)
            out = subprocess.check_output(["java", "-cp", d, classname], stderr=subprocess.STDOUT, timeout=10)
            return {"ok": True, "stdout": out.decode()}
        except subprocess.CalledProcessError as e:
            return {"ok": False, "stdout": e.output.decode()}
        except Exception as e:
            return {"ok": False, "error": str(e)}
