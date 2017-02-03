from ftplib import FTP

def get_dirs_ftp(folder=""):
    #print("bbbb")
    contents = ftp.nlst(folder)
    #print(contents)
    folders = []
    for item in contents:
        print(item + "\n")
        if "." not in item:
            folders.append(item)
    return folders

def get_all_dirs_ftp(folder=""):
    #print("aaaa")
    dirs = []
    new_dirs = []

    new_dirs = get_dirs_ftp(folder)

    while len(new_dirs) > 0:
        for dir in new_dirs:
            dirs.append(dir)

        old_dirs = new_dirs[:]
        new_dirs = []
        for dir in old_dirs:
            for new_dir in get_dirs_ftp(dir):
                new_dirs.append(new_dir)

    dirs.sort()
    return dirs


host ="100.1.1.6"
user = "yucps00"
password = "cps111036a"

print("Connecting to {}".format(host))
ftp = FTP(host)
ftp.login(user, password)
print("Connected to {}".format(host))

print("Getting directory listing from {}".format(host))
all_dirs = get_all_dirs_ftp()
print("***PRINTING ALL DIRECTORIES***")
for dir in all_dirs:
    print(dir)