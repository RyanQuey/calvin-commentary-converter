#!/bin/bash

if [ -z "$1" ]
    then 
        echo "Purpose: move docx files in current folder (not recursive) into a backup dir, and then archive that dir and delete the original."
        echo "Usage: $0 {path_to_scan}"
        echo "e.g.,: $0 '/mnt/c/Users/queyr/OneDrive/Notes/Bible Notes'"
        echo "(make sure to use quotes if folder has spaces)"
        exit 1;
fi

# escapes spaces and sets to var
path_to_scan=$1

# makes it so `find` command handles the spaces in folder and file names
IFS=$'\n'

# Source: https://gist.github.com/bzerangue/2504041
# other resources: 
#   - https://forum.obsidian.md/t/simple-powershell-for-now-script-to-convert-microsoft-word-files-into-markdown-with-pandoc/7121/5

# possible changes: 
# - use different markdown format, e.g., github markdown

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# for .docx files
# wrap path in single quotes to easily handle spaces in folder names, which is common for my ONedrive folders
# TODO add recursive option
# TODO add checker to check for .md file first to make sure we don't archive stuff that isn't ready yet!!! Very important, make sure that is in place before recursive option is implemented. 
mkdir -p $path_to_scan/backup && \
    mv *.docx $path_to_scan/backup && \
    zip -r backup.zip $path_to_scan/backup && \
    rm -rf $path_to_scan/backup && \
    echo "Successfully cleaned up those old docx files!"

