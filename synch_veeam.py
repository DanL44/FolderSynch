import os
import shutil
import hashlib
import argparse
import time
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Folder Synchronization Program")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Log file path")
    return parser.parse_args()

def setup_logging(log_file):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        handlers=[logging.FileHandler(log_file),
                                  logging.StreamHandler()])

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        replica_path = os.path.join(replica, relative_path)
        
        # Create directories that don't exist in replica
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)
            logging.info(f"Created directory: {replica_path}")
        
        # Copy/update files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_path, file)
            
            if not os.path.exists(replica_file) or \
               calculate_md5(source_file) != calculate_md5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"Copied/Updated file: {replica_file}")
    
    # Remove extra files/folders in replica
    for root, dirs, files in os.walk(replica):
        relative_path = os.path.relpath(root, replica)
        source_path = os.path.join(source, relative_path)
        
        if not os.path.exists(source_path):
            shutil.rmtree(root)
            logging.info(f"Removed directory: {root}")
            continue
        
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_path, file)
            
            if not os.path.exists(source_file):
                os.remove(replica_file)
                logging.info(f"Removed file: {replica_file}")

def main():
    args = parse_arguments()
    setup_logging(args.log_file)
    
    logging.info("Starting folder synchronization")
    
    while True:
        try:
            sync_folders(args.source, args.replica)
            logging.info(f"Synchronization completed. Waiting for {args.interval} seconds.")
            time.sleep(args.interval)
        except KeyboardInterrupt:
            logging.info("Synchronization stopped by user.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            break

if __name__ == "__main__":
    main()