import os
import sys
import subprocess
import shutil
from pathlib import Path


def ensure_pyinstaller():
    try:
        import PyInstaller
    except ImportError:
        print("正在安装PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])


def clean_build_dirs():
    for dirname in ["dist", "build"]:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)


def get_build_command():
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=CJGameStudio",
        "--add-data=src;src",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--clean",
        "main.py"
    ]

    if os.path.exists("assets/icon.ico"):
        cmd.insert(4, "--icon=assets/icon.ico")

    if os.path.exists("assets"):
        cmd.insert(5, "--add-data=assets;assets")

    return cmd


def copy_config_files():
    """复制配置文件到dist目录"""
    if os.path.exists("config"):
        dist_config_dir = "dist/config"
        if os.path.exists(dist_config_dir):
            shutil.rmtree(dist_config_dir)
        shutil.copytree("config", dist_config_dir)
        print("配置文件已复制到dist/config目录")
    else:
        print("警告: config目录不存在")

def copy_assets_files():
    """复制配置文件到dist目录"""
    if os.path.exists("assets"):
        dist_assets_dir = "dist/assets"
        if os.path.exists(dist_assets_dir):
            shutil.rmtree(dist_assets_dir)
        shutil.copytree("assets", dist_assets_dir)
        print("配置文件已复制到dist/assets目录")
    else:
        print("警告: assets目录不存在")

def build_executable():
    print("开始构建可执行文件...\n")

    ensure_pyinstaller()
    clean_build_dirs()

    cmd = get_build_command()
    print(f"构建命令: {' '.join(cmd)}\n")

    try:
        subprocess.check_call(cmd)
        print(f"\n构建完成: {os.path.abspath('dist/CJGameStudio.exe')}")

        copy_config_files()
        copy_assets_files()
        return True
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False


def install_dependencies():
    print("安装项目依赖...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False


def main():
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print("=" * 60)
    print("CJGameStudio 构建工具")
    print(f"工作目录: {script_dir}")
    print("=" * 60 + "\n")

    if sys.version_info < (3, 7):
        print("错误: 需要 Python 3.7 或更高版本")
        return

    if not install_dependencies():
        return

    if build_executable():
        print("\n" + "=" * 60)
        print("构建成功!")
        print("可执行文件: dist/CJGameStudio.exe")
        print("=" * 60)
    else:
        print("\n构建失败，请检查错误信息")


if __name__ == "__main__":
    main()
