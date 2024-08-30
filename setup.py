from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame"],
    "include_files": [],
}

setup(
    name="Lx Paint",
    version="0.1",
    description="MS Paint-like application Made by @NobleSkye named from @foodfor1000",
    options={"build_exe": build_exe_options},
    executables=[Executable("lxpaint.py")]
)
