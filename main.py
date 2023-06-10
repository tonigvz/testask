import os, time, json, shutil, hashlib, glob
from deepdiff import DeepDiff


class syncronization:
    def __init__(self):
        self.source_path = "C:/Users/antonia/Desktop/Test Task/source"
        self.replica_path = "C:/Users/antonia/Desktop/Test Task/replica"
        self.interval = 300
        self.log = None
        self.source_files = {}
        self.files = os.listdir(self.source_path)
        self.files_r = glob.glob("C:/Users/antonia/Desktop/Test Task/replica/*")

    def prepare(self):
        self.source_files["size"] = len(self.files)
        if os.path.exists(self.source_path):
            for file in self.files:
                with open(os.path.join(self.source_path, file), "rb") as f:
                    self.source_files[f.name.split("\\")[1]] = hashlib.md5(
                        f.read()
                    ).hexdigest()

    def syncronyze(self):
        self.log = json.load(open("log.txt"))
        diff = DeepDiff(self.log, self.source_files)
        print(self.source_files)
        print("\n")
        print(self.log)
        print(diff)
        time_now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        if not diff:
            print(f"{time_now} - no changes have been made")
        else:
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
        json.dump(self.source_files, open("log.txt", "w"))


if __name__ == "__main__":
    test = syncronization()
    test.prepare()
    test.syncronyze()
