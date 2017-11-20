#!/usr/bin/env python3

import os
import sys


def main():
    key_map = {
        "剩余： ": "free",
        "已用： ": "Pages active"
    }
    for k in key_map:
        out = os.popen("vm_stat | grep '%s'" % key_map[k]).read()
        s = out.strip(" \n\t\r.").split(" ")[-1]
        print("%s %.2f GB" % (k, float(int(s)*4/1024.0/1024.0)))


if __name__ == "__main__":
    main()
