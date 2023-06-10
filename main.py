import os, time, json, shutil, hashlib, glob
from deepdiff import DeepDiff


class syncronization:
    def __init__(self):
        self.source_path = source_path
        self.replica_path = replica_path
        self.interval = interval
        self.log_path = log_path
        self.log = None

    def syncronyze(self):
        while True:
            # dictionary to save name and hash of file
            self.source_files = {}
            # all files from source folder
            self.files = os.listdir(self.source_path)
            # all files from replica folder
            self.files_r = glob.glob(f"{self.replica_path}/*")
            # current time
            time_now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            # saving the number of files to tell the user if there has been an addition or removal of files
            self.source_files["size"] = len(self.files)
            # adding the name and the hash to the dictionary
            if os.path.exists(self.source_path):
                for file in self.files:
                    with open(os.path.join(self.source_path, file), "rb") as f:
                        self.source_files[f.name.split("\\")[1]] = hashlib.md5(
                            f.read()
                        ).hexdigest()
            # if log file is empty then we add the dictionary to it if not we read it
            try:
                self.log = json.load(open(self.log_path))
            except:
                json.dump(self.source_files, open("log.txt", "w"))
                self.log = json.load(open(self.log_path))
            # see if there are any differences between the log file and the dictionary
            diff = DeepDiff(self.log, self.source_files)
            if not diff:
                print(f"{time_now} - no changes have been made")
            else:
                # delete the old files from the replica folder and copy everything from source
                print(f"{time_now} - theres been changes")
                if self.source_files["size"] != self.log["size"]:
                    if self.log["size"] < self.source_files["size"]:
                        print(f"{time_now} - one or more files have been added")
                    else:
                        print(f"{time_now} - one or more files have been deleted")
                print(f"{time_now} - removing files from replica")
                for f in self.files_r:
                    os.remove(f)
                print(f"{time_now} - copying files to replica")
                for f in self.files:
                    shutil.copy2(f"{self.source_path}/{f}", f"{self.replica_path}/{f}")
                print(f"{time_now} - replica has been synchronized")
            # update the log
            json.dump(self.source_files, open("log.txt", "w"))
            time.sleep(interval)


if __name__ == "__main__":
    source_path = input("enter source path:")
    replica_path = input("enter replica path:")
    log_path = input("enter log file path:")
    interval = int(input("enter synchronization interval:"))
    test = syncronization()
    test.syncronyze()
