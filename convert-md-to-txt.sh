#!/bin/bash

if [ -z "$1" ]
    then 
        echo "Purpose: convert all files in folder recursively from .docx to markdown"
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

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# make sure to use python3 so can use right version of pandoc
alias python="$(which python3)"
which python3

# for markdown files
# wrap path in single quotes to easily handle spaces in folder names, which is common for my ONedrive folders
find $path_to_scan -name "*.md" | while read i; 
do 
    printf "\nconverting:        $i";  

    # gets dir of current file that we're looking at
    file_dirname=$(dirname ${i})

    # options used: 
    # --wrap none, so does not wrap text at 72 characters
    # reference-location section, so that footnotes are kept with the section rather than the doc. Important since will be splitting files apart
    # -t gfm is for github markdown, I think it's a better standard than `markdown` option (Pandoc's markdown)
    #       - `markdown` has better image tags, just uses standard ![]() syntax, but adds a {width, height} thing afterwards that shows up as plaintext.
    #       - Users on this page (as of May 2021) on the forum seems to use `markdown` format https://forum.obsidian.md/t/simple-powershell-for-now-script-to-convert-microsoft-word-files-into-markdown-with-pandoc/7121/9
    # --extract-media takes images and so on and puts in a media dir that can be referenced (https://stackoverflow.com/questions/39956497/pandoc-convert-docx-to-markdown-with-embedded-images). Will create a "media" dir if one does not exist yet, and reference.
    # markdown-smart is better. https://stackoverflow.com/questions/53678363/stopping-pandoc-from-escaping-single-quotes-when-converting-from-html-to-markdow doesn't escape as much
    pandoc \
        -f markdown-smart \
        -t plain \
        "$i" -o "${i%.*}.txt" \
        --wrap none \
        --reference-location section \
        --extract-media "$file_dirname" \
        --lua-filter $SCRIPT_DIR/compact-lists-filter.lua \
        --filter $SCRIPT_DIR/python_filters
done


