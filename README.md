# Calvin Commentaries Converter
For converting Calvin Commentaries copied from CCEL word documents to markdown (so it's machine readable), then to prepare and ingest into ChatGPT-4

# Instructions
## Install python requirements
```
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

Note that pandoc will use default python, so whatever version of python is ran by `python` command (2 or 3) will be what pandoc uses. But we want to use latest version of pandoc, and so use python3 (our script will specify that for us). 

Therefore, don't install using `pip3 install`, but use `pip install`

## Install pandoc
Needs pandoc 2.1 or later that allows lua filters, so get latest release using .deb file from pandoc releases on Github (NOTE as of Dec 2022, can do `sudo apt-get install pandoc` if in new enough Ubuntu version. 18.04 Bionic, which ships with WSL2, is too old, giving 1.19.2, but focal or jammy (20.04 or 22.04) are fine. 

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


# Usage 
See [README](./chatgpt/README.md)