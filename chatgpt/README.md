# Chat GPT - for converting Calvin Commentaries
For converting from old English markdown to modern

## Description
- Takes already-prepared Markdown files from Calvin's Commentaries, and sends chunk by chunk (mostly, verse by verse) 

# Instructions
- For all instructions, see Ryan's personal notes [in Obsidian, here](obsidian://open?vault=Notes&file=work.ministry%2Fkh.my%20teams%2Fplovpit%2Fplovpit.commentaries%2Fplovpit.calvin%2FCalvin's%20Commentaries%20-%20Khmer%20-%20Steps%20-%20Simplifying%20the%20English).
- Some general notes though have been added below for convenience 
    - TODO put all notes in here, for sharing with others etc.

## Step 1 - Prepare markdown for ingestion
- At end of this process, files should have all verses as a header, e.g.:

```
### Verse 10.
This is commentary about verse 10...
(etc)
```



## Step 2 - Split markdown for ingestion
### 2.1 Put it into chapters, one chapter per file 

#### Q: Why Markdown?
- It preserves some formatting/headers which ChatGPT actually seems to recognize and take advantage of. 
- Machine readable AND Human readable
- Chat GPT API also returns as Markdown, so then it's easy to convert to MS Word later using Pandoc


# Folder Organization
- `./original-text`
    - Actual Calvin commentary Text to ingest 
    - `./original-text/chunks-for-ingestion`
        - Commentary broken up into chunks, which will be ingested by our script (`main.py`)
    - `./original-text/finished`
        - Just a place to hide texts when they've ran through already and I don't want to run them again, but don't want to delete. 
        - Don't commit anything in there. 
    - `./original-text/backup`
        - Place to put original files/chunks after running them through GPT API, so don't run them again on accident (eating up API credits), but don't want to delete yet. 
    - `./original-text/full`
        - Place to put the full Calvin commentary files (markdown/txt only)
- `./sample-text`
    - Small chunks of Calvin commentary Text to ingest, for testing purposes (when using `test` option)
    - Structured similarly to `./original-text`

# Tips for ingestion
## Break up into chunks
GPT-4 API will heavily abridge once a section is more than a few paragraphs. This not just simplifies, but summarizing, cutting out lots of info.
    - How long is too long? 
        - (think 1-2 paragraphs, or maybe a page max. E.g., Col 1:24 was too long, so had to break that up further)

Some things in this script to accomodate for that:
    - I made the script to recognize when a section starts with a Header 3 `### Verse__`. This works well with the preparation process I have (as documented elsewhere) for getting Calvin's commentary
    - For Introduction chapter, I divided up manually instead. Dividing it up into smaller chunks and running that way worked much better. 