import os

rootdir = os.path.abspath('.')

def get_file_names():
    names = []
    for filenames in os.walk(rootdir):
        names.append(filenames)
    return names[0][2]

if __name__ == '__main__':
    print(get_file_names())