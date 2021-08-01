#!/usr/bin/env python

# git diff
# strace -e trace=execve,openat -f -o z-open.strace make

# 243783 openat(AT_FDCWD, "variants/standard/mpconfigvariant.mk", O_RDONLY) = 4
# 243784 execve("/usr/bin/uname", ["uname", "-s"], 0x7ffd426a8298 /* 50 vars */) =

import base64
import hashlib
import os.path
import re
import sys

sha2empty=hashlib.sha256(b'').hexdigest()
def main():
    seen = {}
    with open(sys.argv[1]) as fh:
        for l in fh:
            (nil, nil, beginFilename) = l.partition('"')
            (filename, nil, nil) = beginFilename.partition('"')
            seen[filename] = True
    for filename in sorted(seen.keys()):
        #print('debug',filename)
        sha2hex=sha2(filename)
        if sha2hex==sha2empty:
            continue
        print('SHA256 (%s) = %s'%(filename,sha2hex))
        #SHA256 (go.strace) = 871e380e653a58e1dae6361b40d3fe097e67084a6acfd7420136b721643cafc8
def sha2(filename):
    if filename.startswith('/dev/'):
        return sha2empty
    if not os.path.exists(filename):
        return sha2empty
    blockSz=1024*1024
    m = hashlib.sha256()
    try:
        with open(filename,'rb') as fh:
            while True:
                buf = fh.read(blockSz)
                m.update(buf)
                if len(buf) < blockSz:
                    break
    except Exception as e:
        pass
    #return base64.b64encode(m.digest())
    return m.hexdigest()
        
            

if __name__ == "__main__":
    main()
