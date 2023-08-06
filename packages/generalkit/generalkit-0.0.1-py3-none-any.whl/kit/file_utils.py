import os, shutil
from pathlib import Path
from io import DEFAULT_BUFFER_SIZE as size


class Files:
    @classmethod
    def read_file_to_string(cls, file_path, buffering=size, encoding='utf-8', errors=None, newline=None, closefd=True):
        with open(file_path, buffering=buffering, encoding=encoding, errors=errors, newline=newline,
                  closefd=closefd) as f:
            return str(f.read())

    @classmethod
    def read_lines(cls, file_path, buffering=size, encoding='utf-8', errors=None, newline=None, closefd=True):
        with open(file_path, buffering=buffering, encoding=encoding, errors=errors, newline=newline,
                  closefd=closefd) as f:
            return f.readlines()

    @classmethod
    def write_lines(cls, file_path, text_list: list, append=False, buffering=size, encoding='utf-8', errors=None,
                    newline=None, closefd=True):
        mode = 'w'
        if append:
            mode = 'a+'
        with open(file_path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline,
                  closefd=closefd) as f:
            for i in text_list:
                f.write(i)
            f.close()

    @classmethod
    def write_string_to_file(cls, file_path, text, append=False, buffering=size, encoding='utf-8', errors=None,
                             newline=None, closefd=True):
        mode = 'w'
        if append:
            mode = 'a+'
        with open(file_path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline,
                  closefd=closefd) as f:
            f.write(text)
            f.close()

    @classmethod
    def delete_directory(cls, directory_path):
        shutil.rmtree(directory_path)

    @classmethod
    def create_file(cls, file_path):
        return open(file_path, 'w')

    @classmethod
    def create_directory(cls, directory):
        os.mkdir(directory)

    @classmethod
    def create_directory_recursion(cls, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)

    @classmethod
    def delete_file(cls, file_path):
        os.remove(file_path)

    @classmethod
    def rename_file(cls, old_file, new_file):
        os.rename(old_file, new_file)

    @classmethod
    def move_file_to_directory(cls, old_file, new_file):
        shutil.move(old_file, new_file)

    @classmethod
    def copy_file_to_directory(cls, old_file, directory):
        name = str(Path(old_file).name)
        shutil.copyfile(old_file, directory + "/" + name)

    @classmethod
    def list_files(cls, directory, format=None):
        files = []
        for f in os.walk(directory):
            for j in f[2]:
                files.append(os.path.join(f[0], j))
        if format:
            for i in  files:
                if not i.endswith(format):
                    files.remove(i)
        return files

    @classmethod
    def is_file_exists(cls, file_path):
        return os.path.exists(file_path)

    @classmethod
    def get_file_format(cls, file_path):
        return Path(file_path).suffix.replace('.', '')

    @classmethod
    def get_file_name(cls, file_path):
        return Path(file_path).stem

    @classmethod
    def get_file_dir_path(cls, file_path):
        return os.path.dirname(file_path)

    @classmethod
    def get_file_abs_path(cls, file_path):
        return os.path.abspath(file_path)

    @classmethod
    def get_file_parent(cls, file_path):
        return Path(file_path).parent
