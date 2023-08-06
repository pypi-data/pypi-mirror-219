import os
import hashlib
import shutil

from .__version__ import __version__


def get_file(file):
    folder = os.path.dirname(__file__)
    file = os.path.join(folder, file)
    return os.path.abspath(file).replace('\\', '/')

def install_gia_dependence(root_path):
    for folder in ["YoloxModels"]:
        verify_and_copy_files(os.path.join(root_path, 'assets', folder), os.path.join(os.path.dirname(__file__), folder))

def verify_and_copy_files(x_path: str, y_path: str) -> None:
    if not os.path.exists(x_path):
        print(f'copy files to gia: {y_path} -> {x_path}')
        shutil.copytree(y_path, x_path)
    x_hash = hashlib.sha1()
    for root, dirs, files in os.walk(x_path):
        for file in files:
            with open(os.path.join(root, file), "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk: break
                    x_hash.update(chunk)
    y_hash = hashlib.sha1()
    for root, dirs, files in os.walk(y_path):
        for file in files:
            with open(os.path.join(root, file), "rb") as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk: break
                    y_hash.update(chunk)
    if x_hash.digest() != y_hash.digest():
        print(f'copy files to gia: {x_path} -> {y_path}')
        shutil.rmtree(x_path)
        shutil.copytree(y_path, x_path)
