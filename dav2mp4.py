#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

version = '0.1'


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


parser = argparse.ArgumentParser(description="Convert .dav files to .mp4.")
parser.add_argument('path', help='Path to dav file(s)')
parser.add_argument('-m', '--ffmpeg-location', required=False, help='Path to ffmpeg binary')
parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + version)
args = parser.parse_args()

ffmpeg_args = ["-vcodec", "libx264", "-crf", "24", "-filter:v", "setpts=1*PTS"]
path = args.path

if args.ffmpeg_location:
    ffmpeg = which(args.ffmpeg_location)
else:
    ffmpeg = which("ffmpeg")
if not ffmpeg:
    print "Error: could not find ffmpeg. Use ffmpeg-location to specify path to binary."
    sys.exit(1)

if os.path.isdir(path):
    for filename in os.listdir(path):
        if (filename.endswith(".dav")):
            infile = os.path.join(path, filename)
            outfile = infile + '.mp4'
            subprocess.call([ffmpeg, '-i', infile] + ffmpeg_args + [outfile])
        else:
            continue
elif os.path.isfile(path):
    if path.endswith(".dav"):
        outfile = path + '.mp4'
        subprocess.call([ffmpeg, '-i', path] + ffmpeg_args + [outfile])
    else:
        print "Error: .dav file(s) not found at path."
        print parser.print_help()
        sys.exit(1)
elif not os.path.exists(path):
    print "Error: path not found."
    sys.exit(1)
else:
    print "Error: path not recognized."
    sys.exit(1)
