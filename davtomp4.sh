#!/bin/bash

input="$1"
successful=""
failed=""
ret_code=0

function add_success() {
    successful="${successful}\n${1}"
}

function add_failure() {
    # failed="$failed \n"
    failed="${failed}\n${1}"
}

function convert() {
    infile="$1"
    outfile="${1}.mp4"
    if [[ -e "$outfile" ]]; then
        add_failure "File exists: $outfile"
    else
        ffmpeg -i "$infile" -vcodec libx264 -crf 24 -filter:v "setpts=1*PTS" "$outfile"
        add_success "$outfile"
    fi
}

if [[ -z "$1" ]]; then
    echo "Usage: davtomp4.sh /path/to/dav"
    echo ""
    echo "path/to/dav can be a directory or .dav file"
    echo ""
    echo "return error codes:"
    echo "  1: unknow error"
    echo "  2: one or more output files exist"
    echo "  3: ffmpeg not found"
fi

if [ -f "$(which ffmpeg)" ]; then
    if [[ -f "$input" ]]; then
        # input is a file
        convert "$input"
    elif [[ -d "$input" ]]; then
        # input is a directory
        for i in "$input"/*.dav; do
            convert "$i"
        done
    fi

    # output message
    if [[ ! -z "$successful" ]]; then
        echo ""
        echo "Successfully converted:"
        echo -e $successful
    fi
    echo ""
    if [[ ! -z "$failed" ]]; then
        echo "Failed:"
        >&2 echo -e $failed
        echo ""
        ret_code=2
    fi
else
    >&2 echo "Error: ffmpeg not found. Try installing ffmpeg with brew"
    ret_code=3
fi

exit $ret_code
