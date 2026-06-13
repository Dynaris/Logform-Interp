import shutil
from subprocess import CalledProcessError
import requests
import subprocess
import common
from tkinter import messagebox
import os
from LLM import config

#TLDR:
#The purpose of this file, is to check if the user meets the needed requirements for the tool (installation, execution) prior to parsing any files.

#This ensures the User has a fallback port, or can use a custom one if already chosen.
OLLAMA_URL = config.OLLAMA_URL
OLLAMA_MODEL = config.OLLAMA_MODEL

def check_ollama_installed(retry=False):
    ollama_download = "https://ollama.com/download"

    #Check if Ollama is installed and running. If not, give them a Boolean choice if they would like to install it.
    #Depending on the choice, they can be redirected to Ollama's website, or be denied the right to continue.
    if shutil.which("ollama") is not None:
        print("Found Ollama installation.\n") #Debug
        common.log_message("Ollama installation was found.")
        return True
    else:
        want_to_install = messagebox.askyesno("Missing dependency.","Ollama installation was not detected. Would you like to install it?\n")
        if want_to_install:
            print("An Ollama download link was sent to the user.\n") #Debug
            common.log_message(f"Please install Ollama via the following hyperlink\n: {ollama_download}.")
            install_second_check = messagebox.askyesno("Checking dependency status...", "Were you able to complete the download and installation of the tool?\n")
            if install_second_check:
                if not retry:
                    return check_ollama_installed(retry=True)
                else:
                    print("Second installation check: installation remains undetected.\n") #Debug
                    common.log_message("Installation remains undetected.")
                    return False
            else:
                common.log_message("You opted out of installing needed requirements. For this reason, it is not possible to proceed.")
                print("Second installation check: User did not accept requirement installation needed.\n")  # Debug
                return False
        else:
            common.log_message("\nYou opted out of installing needed requirements. For this reason, it is not possible to proceed.")
            print("User did not accept requirement installation needed.\n") #Debug
            return False

def check_ollama_running():

    #Check if a custom port is being used and inform the user about it.
    if "11434" not in OLLAMA_URL:
        common.log_message(f"Custom or invalid Ollama port detected: {OLLAMA_URL}. Proceeding with this configuration.")
        print(f"Warning: Ollama running on custom port {OLLAMA_URL}.\n") #Debug

    #Check if Ollama localhost connection is running and provide ConnectionError or Timeout results.
    try:
        response = requests.post(
            OLLAMA_URL, json={
                "model": OLLAMA_MODEL,
                "messages": [{
                    "role": "user",
                    "message": "This is a test. Is the model reading this?"
                }]
            },
            timeout=90
        )

        #Room for improvement here, by adding a section that allows the user to see the return of the "alive check" for the LLM model.

        if response.status_code == 200:
           common.log_message("Ollama connection is active.")
           print("Ollama service active.\n") #Debug
           return True
        else:
            common.log_message(f"It was not possible to locate your Ollama connection. Error: {response.status_code} was found.")
            print(f"Unexpected status code: {response.status_code}") #Debug
    except requests.exceptions.ConnectionError:
        print("Ollama is not running..\n") #Debug
        common.log_message("Ollama is not running. Please start the application and retry.")
        return False
    except requests.exceptions.ConnectTimeout:
        print("Connection to localhost timed out.\n")
        common.log_message(f"It was not possible to establish connection to localhost. Please ensure port: {OLLAMA_URL} is accessible.")
        return False

def check_llm_installed(retry= False):
    #Check if the LLM model has been downloaded within Ollama's models list.
    check_llm_list = subprocess.run(["ollama","list"], capture_output= True, text = True)

    if OLLAMA_MODEL in check_llm_list.stdout:
        print(f"Ollama Model {OLLAMA_MODEL} installation found.\n") #Debug
        common.log_message(f"{OLLAMA_MODEL} model installation found.")
        return True
    else:
        request_model_installation = messagebox.askyesno("An LLM model is missing. Would you like to install it?\n")
        if request_model_installation:

            #Inform user that the LLM model download will attempt to start.
            common.log_message(f"Attempting to download {OLLAMA_MODEL} LLM model...This may take a while, depending on your connection. Please do not close this page.")
            print(f"{OLLAMA_MODEL} model is now being downloaded.\n") #Debug

            try:
                subprocess.run(["ollama", "pull", OLLAMA_MODEL], check= True) #downloads predefined model
                check_llm_list() #update ollama list to check if model is now available
                if OLLAMA_MODEL in check_llm_list.stdout:
                    print(f"Model {OLLAMA_MODEL} has been installed successfully.\n")
                    common.log_message(f"Model {OLLAMA_MODEL} has been installed successfully.")
                    return True
                elif OLLAMA_MODEL not in check_llm_list.stdout:
                    if not retry:
                        print("First installation attempt failed, retrying...\n")
                        common.log_message("First installation or attempt to locate an LLM failed. Retrying...")
                        return check_llm_installed(retry=True)
                    else:
                        common.log_message(
                        f"{OLLAMA_MODEL} model remains undetected. Please proceed with installation to continue.\n"
                        "To install the LLM model of your choice, use your available CLI and define the intended model manually in the application files.\n")
                        print("User did not accept, or did not correctly install LLM model. Steps were shared for installation, and application stopped running.\n") #Debug
                        return False
            except subprocess.CalledProcessError:
                common.log_message(f"A process error has occurred: {CalledProcessError}")
                print(f"A process error has occurred: {CalledProcessError}")
                return False
    return False

#This function was placed for structural purposes, as a checkpoint for function values: check_ollama_installed, check_ollama_running, and check_ollama_installed.
def local_llm_ready():
    if check_ollama_installed() and check_ollama_running() and check_llm_installed():
        print("User meets all requirements. Initiating application.\n") #Debug
        common.log_message("All LLM requirements are met.")
        return True
    else:
        print("User does not meet all requirements.\n") #Debug
        return False