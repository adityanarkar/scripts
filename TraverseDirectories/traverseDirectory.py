import os

findString = b"" #Enter string to find in files
# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    # print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        filename = root+"\\"+file
        with open(filename, 'rb') as f:
            if (findString in f.read()):
                print(filename)
            # else:
            #     print(f)
