# FolderSynch

This program synchronizes two folders: a source folder and a replica folder. It maintains a full, identical copy of the source folder at the replica folder location.

## Files

- `synch_veeam.py`: The main synchronization program
- `populate.py`: A script to create a test environment with various files and folders
- `test.py`: A thorough test suite for the synchronization program

## How It Works

The synchronization program (`synch_veeam.py`) does the following:

1. Compares the contents of the source and replica folders
2. Copies new and updated files from source to replica
3. Removes files and folders from replica that don't exist in source
4. Logs all operations to a file and to the console
5. Repeats the process at specified intervals

## How to Run

python3 synch_veeam.py <source_folder> <replica_folder> <sync_interval> <log_file>

Example:

python3 synch_veeam.py /path/to/source /path/to/replica 60 sync_log.txt

This will synchronize the folders every 60 seconds and log operations to `sync_log.txt`.

## Using the tests

1. To create a test environment:
python3 populate.py

This will create a `test_source` directory with various files and folders which then can be used to test synch_veeam.

2. To run the test suite

python3 test.py

This will run a series of tests on the synchronization program, including:
- Basic file and folder operations
- Updates and deletions
- Special character handling
- Empty folder synchronization
- Large file synchronization

The test script will output progress and results for each test phase.
