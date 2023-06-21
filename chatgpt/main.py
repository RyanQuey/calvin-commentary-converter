import openai
import os
from dotenv import load_dotenv
from pathlib import Path
import sys

load_dotenv()
# the folder that this current file is in
base_path = Path(__file__).parent

PLEASE_CONTINUE = "Please continue"

class SimplifyJob:
    def __init__(self, testing, original_text_filename, original_folder, bible_book):
        self.testing = testing
        #testing = True
        print(f"testing: {self.testing}")

        ####################
        # Files to send through
        ####################
        # see Ryan's Obsidian notes for what these version numbers refer to.
        self.formatted_base_text_version = "2.4"
        ####
        if self.testing:
            self.filename_base = os.path.splitext(original_text_filename)[0]

        else:
            # NOTE GPT-4 model's max length is 8192 tokens. For example, Coloissians as a whole is 42253 tokens (file was 181 kb). So about a little less than 1/5 of that is ideal target (maybe 36 kb).  

            # can use if want to do manually
            self.filename_base = os.path.splitext(original_text_filename)[0]
            # self.filename_base = "Calvin.Colossians.en.2.4 - ch.01.1-14"

        self.file_path = (base_path / f"./{original_folder}/chunks-for-ingestion/{self.filename_base}.md").resolve()
        #self.file_path = (base_path / f"./{original_folder}/{self.filename_base}.txt").resolve()

        ####################
        # Result files
        ####################
        ####
        self.conversion_script_version = "0.1.0.0"
        # For testing
        # (depending on how big of a chunk)

        if self.testing:
            self.results_subdir = "test"
        else:
            self.results_subdir = "prod"

        self.results_file_path = (base_path / f"./results/{self.results_subdir}/{self.filename_base}_SIMPLIFIED_v.{self.conversion_script_version}.txt")


        # shouldn't need, using API key set by env var. (see .env file)
        #openai.api_key = "sk-..."


        # TODO try different propmts
        # Nathan's original
        #prompt_base = "Update the language used in this ancient commentary to modern English:"
        # TODO not yet tried
        #prompt_base = "Update the language used in this ancient Bible commentary to modern English:"
        # TODO not yet tried
        #prompt_base = "Update the language used in this ancient commentary in markdown to modern English:"

        # 0.0.3.1
        #prompt_base = "Update the language used in John Calvin's Bible commentary to modern English:"
        # 0.0.3.2
        #prompt_base = "Update the language used in John Calvin's Bible commentary to simple, modern English:"
        # 0.0.3.3
        #prompt_base = "Update the language used in John Calvin's Bible commentary to clear, modern English:"
        # 0.0.3.4 -- 0.0.4.2
        #prompt_base = "Update the text delimited by triple quotes used in John Calvin's Colossians Bible commentary to clear, modern English:"

        # 0.0.5.1-4
        #self.prompt_base = "Please help to update the following markdown text delimited by triple quotes, which was taken from John Calvin's Colossians Bible commentary:"
        # 0.0.5.5 
        # self.prompt_base = "Please update the following markdown text delimited by triple quotes, which was taken from a 19th century Bible commentary:"
        # 0.0.5.6- (currently using)
        # so...let's put the prompt in the system. THen let user just put in calvin's stuff. Hopefully this will avoid having hte system think it needs to summarize my statement about triple quotes
        self.prompt_base = ""


        # TODO experiment with different blocks, to make sure results are repeatable. 
        # - Note that longer blocks take longer to get response, and eat up more quota. 

        self.final_result_arr = []
        self.has_more_to_say = False
        self.messages_base = []

        self.prompt_system = True

        # https://platform.openai.com/docs/guides/gpt-best-practices/tactic-ask-the-model-to-adopt-a-persona
        if self.prompt_system:
            print("adding system prompt")

            # 0.0.5.1 - Just leaving for now
            # self.system_text = "When I ask for help to update a markdown text, update to clear, modern English:"
            # 0.0.5.2 High school reading level
            # self.system_text = "When I ask for help to update a markdown text, update to clear, modern English at a high school reading level:"
            # 0.0.5.3 ESL reading level
            # self.system_text = "When I ask for help to update a markdown text, update to clear, modern English for ESL reading level:"
            # 0.0.5.3.2 ESL reading level - remove passive
            # self.system_text = "When I ask for help to update a markdown text, update to clear, modern English for ESL reading level (when possible use active voice instead of passive voice):"
            # 0.0.5.4 Junior High school reading level
            # self.system_text = "When I ask for help to update a markdown text, update to clear, modern English at a junior high school reading level:"
            # 0.0.5.5 ESL reading level - reword 
            # self.system_text = f"When I ask for help to update a markdown text, update the language which was taken from a 19th century Bible commentary to clear, modern English for ESL reading level:"

            # 0.1.0.0 ESL reading level - specify book of Bible
            self.system_text = f"When I ask for help to update a markdown text, update the language which was taken from a 19th century Bible commentary on the book of {bible_book} to clear, modern English for ESL reading level:"
            self.messages_base.append({
                "role": "system", 
                "content": self.system_text 
            })

        # we'll put results in here.
        # this as string
        self.commentary_text_block = None
        # this as array of chunks, one per verse section
        self.chunks = []

    def get_original_text(self):
        """
        Fetch the original English text of Calvin's commentaries that we need to simplify.
        """

        with open(self.file_path, "r") as f:

            # get only the top n lines
            if self.testing:
                # n_lines = 3
                # 5 lines gets the first part of 2:8, which is enough for quick iteration/testing
                n_lines = 7

                # 19 lines gets 2:8-9
                # n_lines = 19

                text = [next(f) for _ in range(0, n_lines)]

            else:
                text = f.readlines()

            # divide into chunks
            this_chunk = []

            for line in text:
                if line[:12] == "# Colossians":
                    # can just write that to file directly and move on
                    print(f"writing title to file: {line}")
                    with open(self.results_file_path, 'a') as the_file:
                        the_file.write(line)

                elif line[:9] == "### Verse":
                    # make that into new chunk

                    # check if this chunk has anything worth saving
                    this_chunk_has_something = False
                    for chunk_line in this_chunk:
                        if chunk_line != "\n" and chunk_line != "":
                            this_chunk_has_something = True

                    if this_chunk_has_something:
                        # set it in the chunks for the file! If not, we can ignore and keep going (i.e., the first verse in the section won't need this...)
                        self.chunks.append(this_chunk)
                    # start over with just this line

                    this_chunk = [line]
                    print(f"Making new chunk for: {line}")

                else:
                    # put this line of text in the chunk, and continue.
                    this_chunk.append(line)

            # then make sure to push in that last chunk
            this_chunk_has_something = False
            for chunk_line in this_chunk:
                if chunk_line != "\n" and chunk_line != "":
                    this_chunk_has_something = True

            if this_chunk_has_something:
                # set it in the chunks for the file! If not, we can ignore and keep going (i.e., the first verse in the section won't need this...)
                self.chunks.append(this_chunk)

            # at this point, everything should be chunked out.

            # Let's put all the text into a variable as well though.
            self.commentary_text_block = "".join(text)
            #print("original text block:\n\n", text)


    def initialize_results_file(self):
        """
        creates (overwriting to blank if necessary) file to write results to
        """

        print(f"\n\n=== Writing to file: {self.results_file_path} ===\n\n")
        with open(self.results_file_path, 'w') as the_file:
            the_file.write("")

    def start_conversation(self, chunk):
        """
        Start the conversation with the chat bot.
        """

        # set prompt for this round
        # Use delimiters to clearly indicate distinct parts of the input
        # https://platform.openai.com/docs/guides/gpt-best-practices/six-strategies-for-getting-better-results
        text_for_chunk = "".join(chunk)
        #prompt = f"{self.prompt_base}\n\"\"\"\n{text_for_chunk}\"\"\""
        prompt = text_for_chunk

        messages = self.messages_base + [{
            "role": "user", 
            "content": prompt
        }]

        print("Using messages:\n\n", messages)

        print("now sending to GPT API...")
        # send request to OpenAI GPT-4 API for 
        chat_completion = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=messages
            )

        print(chat_completion.choices)

        # for now, just taking first choice only
        assistant_message = chat_completion.choices[0].message
        response = assistant_message.content

        # if the chat bot finished because of length issue, then that means it has "more to say".
        # NOTE for now, should never run into this since we didn't set a token limit for responses. 
        self.has_more_to_say = chat_completion.choices[0].finish_reason == "length"


        # print the chat completion
        #print("Response for round:", response)
        cleaned_response = self.clean_results(response)
        print("Cleaned Response for round:", cleaned_response)

        self.final_result_arr.append(cleaned_response) 

        # append to file
        self.append_to_file(text_for_chunk, cleaned_response)

    def clean_results(self, results_chunk):
        """
        Takes results we get back from API and cleans it.

        @param results_chunk arr - array of lines from text we got back.
        """

        cleaned_response = results_chunk
        if cleaned_response[:4] == '""" ':
            # if the api returned our triple string...
            # then strip those off!
            cleaned_response = cleaned_response[4:]

        if cleaned_response[-3:] == '"""':
            # if the api returned our triple string at end...
            # then strip those off!
            cleaned_response = cleaned_response[:-3]

        return cleaned_response

    def append_to_file(self, original_text_for_chunk, result_text):
        """
        Take final results for a single chunk and save to end of file.
        """
        # turn from array into string with new lines. This seems to be preferred way in Python to write to file. 

        print("\n\n=== FINAL RESULT for chunk ===\n\n")
        print(result_text)
        with open(self.results_file_path, 'a') as the_file:
            the_file.write("## Original Text:\n")
            the_file.write(original_text_for_chunk)

            the_file.write("\n\n## Simplified Text:\n")
            the_file.write(result_text)
            # at least one is very necessary, or next original text shows up wrong. Two is just a little easier to read. 
            the_file.write("\n\n")

if __name__ == "__main__":
    # whether or not we're looping over all markdown in a folder.
    running_on_all_in_dir = True
    bible_book = "Colossians"

    args = sys.argv
    testing = len(args) > 1 and args[1] == "test"
    print("args", args)

    if testing:
        # list models
        models = openai.Model.list()

        # print the first model's id
        #print("all models", models.data)
        print("first model available in OpenAI's API:", models.data[0].id)
        original_folder = "sample-text"
    else:
        original_folder = "original-text"

    if running_on_all_in_dir:
        directory_path = (base_path / f"./{original_folder}/chunks-for-ingestion").resolve()
        directory = os.fsencode(directory_path)

    # iterate over all files in the ingestion folder
    for file in os.listdir(directory):
        # This should be filename of path to original text
         filename = os.fsdecode(file)
         print(f"\n==========================")
         if filename.endswith(".md"): 
             print(f"running file: {filename}")
             # print(os.path.join(directory, filename))

             job = SimplifyJob(testing, filename, original_folder, bible_book)
             job.initialize_results_file()
             job.get_original_text()
             for chunk in job.chunks:
                 print("\n = sending chunk = ")
                 job.start_conversation(chunk)

             if job.has_more_to_say:
                 job.get_more()

             # TODO remove when finished testing
             #break

         else:
             print(f"(skipping file/dir: {filename})")
             continue
