"""file_libs.py"""

import random
import os
from libsan.host.cmdline import run


def create_ramdisk(dir_path="/ramdisk/", num=10, file_name_prefix="block-"):
    """
    @param dir_path:
    @param num:
    @param file_name_prefix:
    @return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        print("Dir %s exists." % dir_path)

    tmpfs_size = num + 3
    _cmd = "mount -t tmpfs -o size=" + str(tmpfs_size) + "g" " tmpfs /ramdisk"
    retcode = run(_cmd)

    if retcode == 0:
        for i in range(1, num+1):
            file_name = "%s%d" % (file_name_prefix, i)
            _cmd = f"dd if=/dev/zero of={dir_path}{file_name} bs=1M count=1152"
            retcode = run(_cmd)
    return retcode


def generate_file(path, file_name, size=1024):
    """
    Generate a txt file, the default size is 1kB=1024B
    1KB=1024B;1MB=1024KB=1024*1024B
    1B=8 bits
    """
    file_full_path = path + "/" + file_name + ".txt"
    curr_size = 0
    with open(file_full_path, "w", encoding="utf-8") as f:
        while curr_size < size:
            f.write(str(round(random.randint(1, 10000))))
            f.write("\n")
            curr_size = os.stat(file_full_path).st_size

    total_size = os.stat(file_full_path).st_size
    print(total_size)

    return file_full_path


def configure_file(conf_file, *args):
    """
    @param conf_file: the file you want to write
    @param args: one or more strings
    @return: None
    """
    with open(conf_file, 'r+') as rf:
        for p in args:
            rf.seek(0)
            lines = rf.read()
            if p not in lines:
                with open(conf_file, 'a+') as wf:
                    wf.write(p)
                    wf.write('\n')
            else:
                print("INFO: It's all set already.")

