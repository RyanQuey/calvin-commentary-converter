#!/bin/bash

if [ -z "$1" ]
    then 
        echo "Purpose: copy all markdown files in folder recursively into Obsidian dir"
        echo "Usage: $0 {path_to_copy} {obsidian_dir | /mnt/c/Users/queyr/OneDrive/obsidian/Bible notes}"
        echo "e.g.,: $0 '/mnt/c/Users/queyr/OneDrive/Notes/Bible Notes'"
        echo "(make sure to use quotes if folder has spaces)"
        exit 1;
fi

# escapes spaces and sets to var
path_to_copy=$1
obsidian_dir=${2:-"/mnt/c/Users/queyr/OneDrive/obsidian/Bible notes"}

# makes it so `find` command handles the spaces in folder and file names
IFS=$'\n'

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )


echo ""
echo "== Copying files from $path_to_copy to $obsidian_dir"
echo ""

# https://superuser.com/questions/299938/how-can-i-recursively-copy-files-by-file-extension-preserving-directory-structu/299999
# (-updm for overwrite destination content.)
find $path_to_copy -name '*.md' | cpio -updm $obsidian_dir

# remove the parent folders so you don't have all folders since root in here
mv ${obsidian_dir}${path_to_copy} $obsidian_dir

#rm -rf ${obsidian_dir}${path_to_copy}/mnt

echo "done."
