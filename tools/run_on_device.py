#!/usr/bin/python -u

import subprocess
from subprocess import *
from optparse import OptionParser
import sys
from os import path
import re

TEST_DIR="/data/local/tmp/unittest"

def run_on_device(command, check):
    print "$ %s" % command
    out = Popen(["adb", "shell", command], stdout=PIPE).communicate()[0]
    ret = 0
    for line in out.split("\n"):
        print "    %s" % line.rstrip()
        m = re.search("EXIT CODE: ([0-9]+)", line)
        if m != None:
            ret = int(m.group(1))
    if check == True and ret != 0:
        raise RuntimeError("EXIT CODE: %d" % ret)
    return ret

print "Command: " + " ".join(sys.argv);

parser = OptionParser()
(options, args) = parser.parse_args()

subprocess.call(["adb", "shell", "rm", "-r", TEST_DIR])
subprocess.call(["adb", "shell", "mkdir " + TEST_DIR])
params = []
for f in args:
    if path.exists(f):
        subprocess.check_call(["adb", "push", f, TEST_DIR])
        params.append(path.basename(f))
    else:
        params.append(f)

tmp_fn = args[0] + ".tmp"
with open(tmp_fn, 'wb') as the_file:
    the_file.write("cd " + TEST_DIR + "\n")
    the_file.write("./" + " ".join(params) + " --log_level=all\n")
    the_file.write("echo \"EXIT CODE: $?\"\n")

subprocess.check_call(["adb", "push", tmp_fn, TEST_DIR])
subprocess.check_call(["adb", "shell", "ls", "-a", "-l", TEST_DIR])
subprocess.check_call(["adb", "shell", "chmod", "755", TEST_DIR + "/" + path.basename(args[0])])
retcode = run_on_device("sh " + TEST_DIR + "/" + path.basename(tmp_fn), check=True)

exit(retcode)
