import os
import random
import string

def create_file(path, size_kb):
    with open(path, 'wb') as f:
        f.write(os.urandom(size_kb * 1024))

def create_text_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def populate_test_environment(root_dir):
    # Create root directory
    os.makedirs(root_dir, exist_ok=True)

    # Create some files in the root directory
    create_file(os.path.join(root_dir, "file1.bin"), 100)  # 100 KB file
    create_text_file(os.path.join(root_dir, "file2.txt"), "This is a sample text file.")
    create_text_file(os.path.join(root_dir, "file3.log"), "This is a sample log file.\nIt has multiple lines.\n")

    # Create a subfolder with files
    subfolder1 = os.path.join(root_dir, "subfolder1")
    os.makedirs(subfolder1, exist_ok=True)
    create_file(os.path.join(subfolder1, "subfile1.bin"), 200)  # 200 KB file
    create_text_file(os.path.join(subfolder1, "subfile2.txt"), "This is a text file in a subfolder.")

    # Create an empty subfolder
    os.makedirs(os.path.join(root_dir, "empty_folder"), exist_ok=True)

    # Create a subfolder with special characters
    special_folder = os.path.join(root_dir, "special!@#$%^&*()_+ folder")
    os.makedirs(special_folder, exist_ok=True)
    create_text_file(os.path.join(special_folder, "special_file.txt"), "This file is in a folder with special characters.")

    # Create a deep nested folder structure
    nested_folder = os.path.join(root_dir, "nested", "folder", "structure")
    os.makedirs(nested_folder, exist_ok=True)
    create_file(os.path.join(nested_folder, "deep_file.bin"), 50)  # 50 KB file

    # Create a large file
    create_file(os.path.join(root_dir, "large_file.bin"), 5 * 1024)  # 5 MB file

    # Create files with random content
    for i in range(5):
        filename = f"random_file_{i}.txt"
        content = random_string(random.randint(100, 1000))
        create_text_file(os.path.join(root_dir, filename), content)

    print(f"Test environment populated in {root_dir}")

if __name__ == "__main__":
    source_folder = "test_source"
    populate_test_environment(source_folder)