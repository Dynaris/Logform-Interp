import os
import requests
import argparse
import sys
from LLM import config
from LLM.sys_prompt import system_prompt
from LLM.call_function import tool_mapping, tools, call_function

# Retrieve the LLM model and respective port chosen by the user, and assign it to the respective variables
OLLAMA_URL = config.OLLAMA_URL
OLLAMA_MODEL = config.OLLAMA_MODEL

#debug print(OLLAMA_URL, OLLAMA_MODEL) 

if OLLAMA_URL == None or OLLAMA_MODEL == None:
    raise RuntimeError("No Ollama URL or Ollama model detected. Cannot proceed.")

def generate(prompt, verbose=False):

    messages = [
                    {"role": "system",
                    "content": system_prompt},
                    {"role": "user",
                    "content": prompt},
                    ]

    #safeguard for tool iterations, to avoid infinite investigations
    max_tool_iterations = 20

    for _ in range(max_tool_iterations):
        response = requests.post(OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False,
                "tools": tools
            }
        )

        #Debug
        #print("RAW RESPONSE:", response.text)
        #print("PARSED:", data)

        data = response.json()

        #Debug 2
        #print("DATA:", data)

        #extract tool calls and their descriptive name + args (tool calls are function calls)
        if "tool_calls" in data["message"] and data["message"]["tool_calls"]:
            
            #append tool request message
            messages.append(data["message"])

            for tool_call in data["message"]["tool_calls"]:
                tool_response = call_function(tool_call, verbose)
                
                #add tool result to history
                messages.append(tool_response)

                #Debug 3
                #print(tool_response)
                #print(data["message"])

        else:
            #add assistant reply to history if tool calls don't exist
            messages.append(data["message"])
            break
    else:
        print(f"Maximum number of iterations reached. The model did not produce a final response.")
        sys.exit(1)

    return data["message"]["content"]

# This needs further work, due to GUI usage.
def core():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="*")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")

    args = parser.parse_args()
    user_input = " ".join(args.prompt)

    if not user_input.strip():
        parser.error("Prompt cannot be empty.")

    response = generate(user_input, args.verbose)

    if args.verbose:
        print(f'Final response:{response["message"]["content"]}')
        print(f'Prompt tokens:{response.get("prompt_eval_count")}')
        print(f'Response tokens:{response.get("eval_count")}')
    else:
        print(response["message"]["content"])