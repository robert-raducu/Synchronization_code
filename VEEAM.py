import os       # this is needed for using directory paths and manipulating them
import shutil   # offers a number of high-level operations on files and collections of files
import time     # for synchronization part
import logging  # logging operations to a file,
                # logging = tracking the events and the status of an application as it runs
import argparse # for parsing command-line arguments

# Parse command-line arguments
argParser = argparse.ArgumentParser()

argParser.add_argument("source", help="Path to source directory")
argParser.add_argument("replica", help="Path to replica directory")
argParser.add_argument("sync_time", type=int, help="Interval of synchronization (in seconds)")
argParser.add_argument("-l", "--log", help="Path to log file")

args = argParser.parse_args()

# Start logging
# logging.basicConfig(filename=args.log, level=logging.INFO, format="%(asctime)s%(levelname)s: %(message)s")
# (the target file for log messages; logging level (d,i,w,e,c); customize the format of the message
# Create a logger object
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a formatter for the log messages
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

# Create a file handler for saving log messages to a file
file_handler = logging.FileHandler("synchronize.log")
file_handler.setLevel(logging.INFO)

# Create a stream handler for displaying log messages in the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Add the formatter to the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger object
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Check if source and replica are valid paths

while True:
    if os.path.isdir(args.source):
        break
    else:
        logging.critical("The source path doesn't exist")
        exit()

while True:
    if os.path.isdir(args.replica):
        break
    else:
        logging.critical("The replica path doesn't exist")
        exit()

def get_number(Xsource):
    S = 0; folders=0; files = 0
    for _, dirnames, filenames in os.walk(Xsource):  # _, because we don't actually need the first parameter (the path)
        # count folders
        folders += len(dirnames)
        # count files
        files += len(filenames)
    S = files + folders
    return S

def synchronization(Xsource,Xreplica):
    # Check if replica is an empty directory or not
    global start
    if not os.listdir(Xreplica):    # list of files in the folder
        check = 1                   # empty
    else:
        check = 0                   # not empty

    if check == 1:
        start = 0
    elif check == 0:
        start = get_number(Xreplica)

        for filename in os.listdir(Xreplica):
            file_path = os.path.join(Xreplica, filename)
            if os.path.isfile(file_path):     # check if it is a file
                os.remove(file_path)
            elif os.path.isdir(file_path):    # check if it is a directory
                shutil.rmtree(file_path)      # delete it with all the files inside of it

    logging.info("The replica is empty")

    for filename in os.listdir(Xsource):
        file_source = os.path.join(Xsource, filename)
        file_replica = os.path.join(Xreplica, filename)
        if os.path.isfile(file_source):  # check if it is a file
            shutil.copy2(file_source,file_replica)
        elif os.path.isdir(file_source):  # check if it is a directory
            shutil.copytree(file_source, file_replica)

    end = get_number(Xsource)

    if start < end:
        logging.info("Added files or folders in source directory")
    elif start > end:
        logging.info("Deleted files or folders in source directory")
    else:
        logging.info("No changes in source directory")

    logging.info("Synchronization complete")


while True:                     # always true, so it is gonna be executed continuosly
    synchronization(args.source, args.replica)
    time.sleep(args.sync_time)  # pausing for a specific interval of time (in seconds)

