import os, time, json
from deepdiff import DeepDiff

source_path = "C:/Users/antonia/Desktop/Test Task/source"
replica_path = "C:/Users/antonia/Desktop/Test Task/replica"
source_files = {}
files = os.listdir(source_path)

if os.path.exists(source_path):
    with os.scandir(source_path) as entries:
        for entry in entries:
            print(
                entry.name,
                "--",
                round(os.path.getsize(entry) / 1024, 0),
            )
            source_files[entry.name] = round(os.path.getsize(entry) / 1024, 0)

source_files["size"] = len(files)

# writing log
json.dump(source_files, open("log.txt", "w"))
# reading log
log = json.load(open("log.txt"))

# differences between two dicitonaries
diff = DeepDiff(source_files, log)
if not diff:
    print("no changes have been made")
else:
    print("theres been changes")
