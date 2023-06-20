#!/bin/bash

# Jan 2022 update: not really using anymore, just converting and then moving docx files into backup

if [ -z "$1" ]
    then 
        echo "Purpose: convert all files in folder recursively from .docx to markdown, then copy"
        echo "Usage: $0 {path_to_scan}"
        echo "e.g.,: $0 '/mnt/c/Users/queyr/OneDrive/Notes/Bible Notes'"
        echo "(make sure to use quotes if folder has spaces)"
        exit 1;
fi

# escapes spaces and sets to var
path_to_scan=$1

# makes it so `find` command handles the spaces in folder and file names
IFS=$'\n'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

$SCRIPT_DIR/recursive-word-to-md.sh $path_to_scan && \
$SCRIPT_DIR/copy-dir-into-obsidian.sh $path_to_scan 




