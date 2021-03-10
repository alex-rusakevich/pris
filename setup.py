from cx_Freeze import setup, Executable
import pris

includefiles = ["LICENSE", "README.md", "res/"]
includes = ["pris.gui"]
excludes = []
packages = []

setup(
    name = "pris",
    version = pris.VERSION,
    description = "pris",
    author = "Alexander Rusakevich",
    options = {'build_exe': {'includes':includes,'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable("pris.pyw", icon="icon.ico", base = "Win32GUI")]
)
