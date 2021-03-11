from cx_Freeze import setup, Executable
import pris

includefiles = ["LICENSE", "README.md", "res/"]
includes = ["pris.gui"]
excludes = []
packages = []

company_name = "Alerus"
product_name - "pris"

setup(
    name = "pris",
    version = pris.VERSION,
    description = "pris",
    author = "Alexander Rusakevich",
    options = {"build_exe": {
            "includes":includes,
            "excludes":excludes,
            "packages":packages,
            "include_files":includefiles,
            "include_msvcr": True,
            "add_to_path": True
        },
        "bdist_msi": {
            "upgrade_code":"{041664CE-304D-444C-A9E4-C88ABE3BE4EC}",
            "add_to_path":True,
            "initial_target_dir": r"[ProgramFilesFolder]\%s\%s" % (company_name, product_name)
        }
    },
    executables = [Executable("pris.pyw", icon="icon.ico", base = "Win32GUI")]
)
