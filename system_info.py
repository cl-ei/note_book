#!/usr/bin/env python3

import os
import sys


def main():
    key_map = [
        ("未使用的:    ", "free"),
        ("正在使用:    ", "Pages active"),
        ("不活跃的:    ", "inactive"),
        ("内核占用:    ", "wired")
    ]
    used = 0.0
    unused = 0.0
    out_string = ""
    for index in range(len(key_map)):
        description, key = key_map[index]
        raw_s = os.popen("vm_stat | grep '%s'" % key).read().strip(" \n\t\r.").split(" ")[-1]
        s = float(int(raw_s)*4/1024.0/1024.0)
        out_string += "%s %.2f GB\n" % (description, s)

        if index in (0, 2):
            unused += s
        else:
            used += s

    sys.stdout.write("\n共计：可用%.2f GB，已用%.2f GB。\n\n%s\n" % (unused, used, out_string))


if __name__ == "__main__":
    main()
