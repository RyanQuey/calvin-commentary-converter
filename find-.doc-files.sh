#!/bin/bash




if [ -z "$1" ]
    then 
        echo "Purpose: For identifying remaining .doc files so it can be converted. Unfortunately haven't found a better way to convert than opening each one manually in online viewer. Pandoc doesn't do .doc files so this is the what we want to do to convert to markdown."
        echo "Usage: $0 {path_to_scan}"
        echo "e.g.,: $0 /mnt/c/Users/queyr/OneDrive/Notes"
        echo "(make sure to use quotes if folder has spaces)"
        exit 1;
fi

path_to_scan=${1}

# makes it so `find` command handles the spaces in folder and file names
IFS=$'\n'


# Source: https://gist.github.com/bzerangue/2504041


# for .doc files
find $path_to_scan -name "*.doc" | while read i; do printf "\n${i}";  done

