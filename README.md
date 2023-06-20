# Calvin Commentaries Converter
For converting Calvin Commentaries copied from CCEL word documents to markdown (so it's machine readable), then to prepare and ingest into ChatGPT-4

# Instructions
## Install python requirements
```
pip3 install -r requirements.txt
```
Note that pandoc will use default python, so whatever version of python is ran by `python` command (2 or 3) will be what pandoc uses. But we want to use latest version of pandoc, and so use python3 (our script will specify that for us). 

Therefore, don't install using `pip3 install`, but use `pip install`

## Install pandoc
Needs pandoc 2.1 or later that allows lua filters, so get latest release using .deb file from pandoc releases on Github (NOTE as of Dec 2022, can do `apt-get install pandoc` if in new enough Ubuntu version. 18.04 Bionic, which ships with WSL2, is too old, giving 1.19.2, but focal or jammy (20.04 or 22.04) are fine. 

- https://github.com/jgm/pandoc/blob/master/INSTALL.md#linux

### Version to use
- (UPDATE Mar 2023, on 22.04 still getting 2.9.2 which should work per the above, but still erroring out. 

```
TypeError: ('invalid api version', [1, 20])
Error running filter /home/ryan/projects/document-convertor/python_filters:
Filter returned error status 1
```

Just try 2.16.2 for now

Tested with: `pandoc 2.16.2`

### Testing installation
You can confirm it's new enough by running: `pandoc --help | grep lua-filter`
- Should show the option


## List style
Docs: https://www.uv.es/wikibase/doc/cas/pandoc_manual_2.7.3.wiki?75

## Bullet style
Maybe will want to use different format, e.g., some with asterisk, some with dash? Though better is probably to format in Obsidian itself, leave the text itself alone.

## Compact mode bullets
https://stackoverflow.com/questions/39576747/use-compact-lists-when-converting-from-docx-to-markdown

Summary: No flag for this, 


# split markdown into separate files

Options: 
- https://github.com/goetzf/Split-Markdown-for-Ulysses
- https://stackoverflow.com/questions/33889814/how-do-i-split-a-markdown-file-into-separate-files-at-the-heading

# Usage Patterns
## Jan 2022
First, converting all files recursively
```
~/projects/document-convertor/recursive-word-to-md.sh .
```

Then, when about to make changes, cleanup the word docs in a given folder
```
~/projects/document-convertor/move-docx-to-backup-zip.sh .
```

If using WSL2, I like to right click when in explorer to use "Open in Windows Terminal" to get into WSL, and then from the terminal, can go to the explorer using:
```
explorer.exe .
```

This makes it easy to check and make sure things look right, etc. 
