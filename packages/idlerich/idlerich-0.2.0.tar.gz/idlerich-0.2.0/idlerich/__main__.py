# imports?
import sys
import os
import packaging.version
import shutil
import subprocess

def regencache():
    # regen da cache
    global idlepath, fdir, pyver

    try:
        print("Yeeting old cache")
        shutil.rmtree(f"{fdir}/idlelib")

    except FileNotFoundError:
        pass

    print("Regenerating Cache")
    shutil.copytree(idlepath, f"{fdir}/idlelib")
    with open(f"{fdir}/idlelib/ir_version.txt", "w") as f:
        f.write(str(pyver))

    print("Patching Pyshell...")
    with open(f"{fdir}/idlelib/pyshell.py", "r") as f:
        pyshellcode = f.read()

    pyshellcode = pyshellcode.replace("def begin(self", """\
# New patch wrapper from Idlerich for IDLE
    def begin(self, *args, **kwargs):
        retval = self.begin_idle(*args, **kwargs)
        self.write("Python-Rich in namespace.")
        self.interp.runcode(\"\"\"\
import pkgutil
module_name = "rich"
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
rich.pretty.install()
rich.traceback.install(show_locals=False)\"\"\")
        return retval

    # Original begin() from IDLE
    def begin_idle(self""")

    with open(f"{fdir}/idlelib/pyshell.py", "w") as f:
        f.write(pyshellcode)

    print("Patching all files for imports...")

    for file in os.listdir(f"{fdir}/idlelib"):
        if file.endswith(".py") or file.endswith(".pyw"):
            with open(f"{fdir}/idlelib/{file}", "r") as f:
                script = f.read()

            with open(f"{fdir}/idlelib/{file}", "w") as f:
                f.write(f"# Idlerich patch for imports\nimport sys, os\nsys.path.insert(0, os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + \"/..\"))\n\n" + script)

def main():
    global idlepath, fdir, pyver

    print("Idlerich Patcher started!")
    print(f"Idlepath: {idlepath}")
    print(f"Current file dir of pkg: {fdir}")
    print(f"Currrent py ver: {pyver}")

    try:
        with open(f"{fdir}/idlelib/ir_version.txt", "r") as f:
            ir_version = int(f.read())

            print(f"Cache ver: {ir_version}")

            if ir_version < pyver:
                regencache()

    except:
        regencache()

    pywpath = list(os.path.split(os.path.abspath(sys.executable)))
    pywpath[~0] = pywpath[~0].split(".")
    pywpath[~0][0] += "w"
    pywpath[~0] = ".".join(pywpath[~0])
    pywpath = "/".join(pywpath)
    print(f"Pythonw path: {pywpath}")

    print("To run Idlerich, run pythonw on idle.pyw in idlelib in your site-packages folder, at python.")
    print(f"Your pythonw path is {pywpath}, and your idle script path is {fdir}/idlelib/idle.pyw .")

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # idfk y u would pyinstaller idle but ok
    sys.stderr.write("WARNING: Idlerich may not run properly in a PyInstaller environment.\n")
else:
    pass

if not str(sys.version).startswith("3"):
    # python 2 is literally a joke from the gods
    sys.stderr.write("WARNING: Idlerich may not run properly without Python 3.\n")

idlepath = os.path.dirname(sys.executable) + "/Lib/idlelib"
fdir = os.path.dirname(__file__)
pyver = sys.hexversion

if __name__ == "__main__":
    main()
