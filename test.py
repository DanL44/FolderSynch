import os
import sys
import shutil
import time
import hashlib
import subprocess
import random
import string

# Test setup
source_folder = "test_source"
replica_folder = "test_replica"
log_file = "test_sync.log"
sync_interval = 5  # 5 seconds

def create_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_large_file(path, size_mb):
    with open(path, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def setup_test_environment():
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(replica_folder, exist_ok=True)

def clean_test_environment():
    shutil.rmtree(source_folder, ignore_errors=True)
    shutil.rmtree(replica_folder, ignore_errors=True)
    if os.path.exists(log_file):
        os.remove(log_file)

def verify_synchronization():
    print("Verifying synchronization...")
    for root, dirs, files in os.walk(source_folder):
        for dir in dirs:
            source_dir = os.path.join(root, dir)
            replica_dir = os.path.join(replica_folder, os.path.relpath(source_dir, source_folder))
            assert os.path.exists(replica_dir), f"Directory not synced: {replica_dir}"
        
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_folder, os.path.relpath(source_file, source_folder))
            
            assert os.path.exists(replica_file), f"File not synced: {replica_file}"
            assert calculate_md5(source_file) == calculate_md5(replica_file), f"File content mismatch: {replica_file}"
    
    for root, dirs, files in os.walk(replica_folder):
        replica_path = os.path.relpath(root, replica_folder)
        source_path = os.path.join(source_folder, replica_path)
        assert os.path.exists(source_path), f"Extra directory in replica: {root}"
        
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_folder, os.path.relpath(replica_file, replica_folder))
            assert os.path.exists(source_file), f"Extra file in replica: {replica_file}"
    
    print("Synchronization verified successfully!")

def run_sync_program():
    try:
        return subprocess.Popen([sys.executable, "synch_veeam.py", source_folder, replica_folder, str(sync_interval), log_file])
    except FileNotFoundError:
        print(f"Error: Could not find the Python interpreter or the folder_sync.py file.")
        print(f"Current Python interpreter: {sys.executable}")
        print(f"Working directory: {os.getcwd()}")
        print("Please ensure that folder_sync.py is in the same directory as this test script.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred while starting the synchronization program: {e}")
        sys.exit(1)

def wait_for_sync():
    time.sleep(sync_interval + 1)

def test_basic_operations():
    print("Testing basic operations...")
    os.makedirs(os.path.join(source_folder, "subfolder1"))
    create_file(os.path.join(source_folder, "file1.txt"), "This is file 1")
    create_file(os.path.join(source_folder, "subfolder1", "file2.txt"), "This is file 2")
    wait_for_sync()
    verify_synchronization()

def test_update_and_delete():
    print("Testing update and delete operations...")
    create_file(os.path.join(source_folder, "file1.txt"), "This is updated file 1")
    os.remove(os.path.join(source_folder, "subfolder1", "file2.txt"))
    wait_for_sync()
    verify_synchronization()

def test_special_characters():
    print("Testing special characters in filenames...")
    special_filename = "special!@#$%^&*()_+{}.txt"
    create_file(os.path.join(source_folder, special_filename), "File with special characters")
    wait_for_sync()
    verify_synchronization()

def test_empty_folders():
    print("Testing empty folders...")
    os.makedirs(os.path.join(source_folder, "empty_folder"), exist_ok=True)
    wait_for_sync()
    verify_synchronization()

def test_large_file():
    print("Testing large file synchronization...")
    create_large_file(os.path.join(source_folder, "large_file.bin"), 10)  # 10 MB file
    wait_for_sync()
    verify_synchronization()

def run_all_tests():
    clean_test_environment()
    setup_test_environment()
    
    sync_process = run_sync_program()
    
    try:
        test_basic_operations()
        test_update_and_delete()
        test_special_characters()
        test_empty_folders()
        test_large_file()
        
        print("All tests completed successfully!")
    except AssertionError as e:
        print(f"Test failed: {str(e)}")
    except Exception as e:
        print(f"An error occurred during testing: {str(e)}")
    finally:
        sync_process.terminate()
        clean_test_environment()

if __name__ == "__main__":
    run_all_tests()