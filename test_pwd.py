import os
import subprocess

basedir = "/data/openpilot" # assuming this is a symlink
print("BASEDIR:", basedir)
print("Resolved:", os.path.realpath(basedir))
