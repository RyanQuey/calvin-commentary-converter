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
    def __init__(self, testing, original_text_filename, original_folder):
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
            self.filename_base = f"sample-commentary-text.2.8-15.from-{self.formatted_base_text_version}.quotes-for-scr"

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
        self.conversion_script_version = "0.0.5.4"
        # For testing
        # (depending on how big of a chunk)

        if self.testing:
            self.results_subdir = "test"
        else:
            self.results_subdir = "prod"

        self.results_file_path = (base_path / f"./results/{self.results_subdir}/{self.filename_base}_SIMPLIFIED_v.{self.conversion_script_version}.txt")


        # shouldn't need, using API key set by env var. (see .env file)
        #openai.api_key = "sk-..."

        # experimenting with different apis. 
        self.api = "chat"
        #api = "completion"


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
        # 0.0.5.5-  (currently using)
        self.prompt_base = "Please update the following markdown text delimited by triple quotes, which was taken from a 19th century Bible commentary:"


        # TODO experiment with different blocks, to make sure results are repeatable. 
        # - Note that longer blocks take longer to get response, and eat up more quota. 

        self.final_result_arr = []
        self.has_more_to_say = False
        self.messages = []

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
            self.system_text = "When I ask for help to update a markdown text, update the language to clear, modern English for ESL reading level:"
            self.messages.append({
                "role": "system", 
                "content": self.system_text 
            })

        self.commentary_text_block = None

    def get_original_text(self):


        with open(self.file_path, "r") as f:

            # get only the top n lines
            if self.testing:
                # n_lines = 3
                # 5 lines gets the first part of 2:8, which is enough for quick iteration/testing
                n_lines = 5

                # 19 lines gets 2:8-9
                # n_lines = 19

                text = [next(f) for _ in range(0, n_lines)]

            else:
                text = f.readlines()

            self.commentary_text_block = "\n".join(text)
            #print("original text block:\n\n", text)

            # Use delimiters to clearly indicate distinct parts of the input
            # https://platform.openai.com/docs/guides/gpt-best-practices/six-strategies-for-getting-better-results
            self.prompt = f"{self.prompt_base}\n\"\"\"\n{self.commentary_text_block}\"\"\""

            self.messages.append({
                "role": "user", 
                "content": self.prompt
            })
            #print("Using prompt:\n\n", self.prompt)

    def start_conversation(self):
        """
        Start the conversation with the chat bot.
        """

        print("Using messages:\n\n", self.messages)

        print("now sending to GPT API...")
        # create a chat completion
        if self.api == "chat":
            chat_completion = openai.ChatCompletion.create(
                model="gpt-4", 
                messages=self.messages
                )

            print(chat_completion.choices)

            # for now, just taking first choice only
            assistant_message = chat_completion.choices[0].message
            response = assistant_message.content

            # if the chat bot finished because of length issue, then that means it has "more to say".
            self.has_more_to_say = chat_completion.choices[0].finish_reason == "length"

            # append result, in case this conversation needs to continue
            # TODO I think if we extend our token limit, we might not ever need to do this in the API? Check, would make things simpler.
            self.messages.append(assistant_message)

        else:
            # note that gpt-4 is a chat model, so doesn't work with Completion api
            # TODO never tested
            completion = openai.Completion.create(
                model="text-davinci-003", 
                prompt=self.prompt
                )
            print(completion.choices)
            response = completion.choices[0].message.content

        # print the chat completion
        print("Response for round:", response)

        self.final_result_arr.append(response) 

    def get_more(self):
        """
        - if need to request more results from server.
        """
        # append 
        self.messages.append({"role": "user", "content": PLEASE_CONTINUE})
        print("now sending another round to GPT API...(please wait)")
        next_chat_completion = openai.ChatCompletion.create(
            model="gpt-4", 
            messages=self.messages
            )

        # TODO make this into a loop, incase we have to do this multiple times. 
        assistant_message = next_chat_completion.choices[0].message
        response = assistant_message.content
        self.has_more_to_say = next_chat_completion.choices[0].finish_reason == "length"

        # append result, in case this conversation needs to continue
        # TODO I think if we extend our token limit, we might not ever need to do this in the API? Check, would make things simpler.
        self.messages.append(assistant_message)
        print("Response for round:", response)

        self.final_result_arr.append(response) 

    def write_to_file(self):
        """
        Take final results and save to disk.
        """
        # turn from array into string with new lines. This seems to be preferred way in Python to write to file. 
        self.final_result_text = "\n".join(self.final_result_arr)

        print("\n\n=== FINAL RESULT===\n\n")
        print(self.final_result_text)
        print(f"\n\n=== Writing to file: {self.results_file_path} ===\n\n")

        with open(self.results_file_path, 'w') as the_file:
            the_file.write("# Original Text:\n")
            the_file.write(self.commentary_text_block)

            the_file.write("\n\n# Simplified Text:\n")
            the_file.write(self.final_result_text)


if __name__ == "__main__":
    # whether or not we're looping over all markdown in a folder.
    running_on_all_in_dir = True

    args = sys.argv
    testing = len(args) > 0 and args[0] == "test"

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

    for file in os.listdir(directory):
        # This should be filename of path to original text
         filename = os.fsdecode(file)
         print(f"\n==========================")
         if filename.endswith(".md"): 
             print(f"running file: {filename}")
             # print(os.path.join(directory, filename))

             job = SimplifyJob(testing, filename, original_folder)
             job.get_original_text()
             job.start_conversation()

             if job.has_more_to_say:
                 job.get_more()

             job.write_to_file()

             # TODO remove when finished testing
             #break

         else:
             print(f"(skipping file/dir: {filename})")
             continue
