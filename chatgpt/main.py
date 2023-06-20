import openai
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
base_path = Path(__file__).parent

#file_path = (base_path / "../sample-text/sample-commentary-text.2.8-15.unchanged.md").resolve()

#file_path = (base_path / "./sample-text/sample-commentary-text.2.8-15.unchanged.txt").resolve()
file_path = (base_path / "./sample-text/sample-commentary-text.2.8-15.quotes-for-scr.txt").resolve()

results_file_path = (base_path / "./results/Calvin.Colossians.2.8.GPT-result.txt")


#f = open("demofile.txt", "r")


# shouldn't need, using API key
#openai.api_key = "sk-..."

# list models
models = openai.Model.list()

# print the first model's id
#print("all models", models.data)
#print("first model", models.data[0].id)

# experimenting with different apis. 
api = "chat"
#api = "completion"

please_continue = "Please continue"

# TODO try different propmts
# Nathan's original
#prompt_base = "Update the language used in this ancient commentary to modern English:"
# 0.0.3.1
#prompt_base = "Update the language used in John Calvin's Bible commentary to modern English:"
# 0.0.3.2
#prompt_base = "Update the language used in John Calvin's Bible commentary to simple, modern English:"
# 0.0.3.3
#prompt_base = "Update the language used in John Calvin's Bible commentary to clear, modern English:"
# 0.0.3.4
prompt_base = "Update the language used in John Calvin's Colossians Bible commentary to clear, modern English:"
# TODO not yet tried
#prompt_base = "Update the language used in this ancient Bible commentary to modern English:"
# TODO not yet tried
#prompt_base = "Update the language used in this ancient commentary in markdown to modern English:"



# TODO try different dividers
divider = "\n"
#divider = "\n\n"
#divider = " "

# TODO experiment with different blocks, to make sure results are repeatable. 

n_lines = 7
# try all
#n_lines = 2500

final_result_arr = []
has_more_to_say = False
messages = []

def start_conversation():
    with open(file_path, "r") as f:

        # get only the top n lines
        head = [next(f) for _ in range(0, n_lines)]

        commentary_text_block = "\n".join(head)
        #print("original text block:\n\n", head)

        prompt = f"{prompt_base}{divider}{commentary_text_block}"
        print("Using prompt:\n\n", prompt)

        messages.append({"role": "user", 
                         "content": prompt
                       })

        print("now sending to GPT API...")
        # create a chat completion
        if api == "chat":
            chat_completion = openai.ChatCompletion.create(
                model="gpt-4", 
                messages=messages
                )

            print(chat_completion.choices)

            # for now, just taking first choice only
            assistant_message = chat_completion.choices[0].message
            response = assistant_message.content
            has_more_to_say = chat_completion.choices[0].finish_reason == "length"

            # append result, in case this conversation needs to continue
            # TODO I think if we extend our token limit, we might not ever need to do this in the API? Check, would make things simpler.
            messages.append(assistant_message)

        else:
            # note that gpt-4 is a chat model, so doesn't work with Completion api
            # TODO never tested
            completion = openai.Completion.create(
                model="text-davinci-003", 
                prompt=prompt
                )
            print(completion.choices)
            response = completion.choices[0].message.content

        # print the chat completion
        print("Response for round:", response)
        final_result_arr.append(response) 

start_conversation()

if has_more_to_say:
    # append 
    messages.append({"role": "user", "content": please_continue})
    print("now sending another round to GPT API...(please wait)")
    next_chat_completion = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=messages
        )

    # TODO make this into a loop, incase we have to do this multiple times. 
    assistant_message = next_chat_completion.choices[0].message
    response = assistant_message.content
    has_more_to_say = next_chat_completion.choices[0].finish_reason == "length"

    # append result, in case this conversation needs to continue
    # TODO I think if we extend our token limit, we might not ever need to do this in the API? Check, would make things simpler.
    messages.append(assistant_message)
    print("Response for round:", response)
    final_result_arr.append(response) 

final_result_text = "\n".join(final_result_arr)
print("\n\n=== FINAL RESULT===\n\n")

print(final_result_text)

print(f"\n\n=== Writing to file: {results_file_path} ===\n\n")
with open(results_file_path, 'a') as the_file:
        the_file.write(final_result_text)
