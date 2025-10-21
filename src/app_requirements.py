import shutil
from subprocess import CalledProcessError
import requests
import subprocess
from src import common
from tkinter import messagebox
import os

#TLDR:
#The purpose of this file, is to check if the user meets the needed requirements for the tool (installation, execution) prior to parsing any files.

def check_ollama_installed(retry=False):
    ollama_download = "https://ollama.com/download"

    #Check if Ollama is installed and running. If not, give them a Boolean choice if they would like to install it.
    #Depending on the choice, they can be redirected to Ollama's website, or be denied to right to continue to log parsing features.
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
    #This ensures the User has a fallback port, or can use a custom one if already chosen.
    ollama_port = os.getenv("OLLAMA_PORT", "11434")
    ollama_host = os.getenv("OLLAMA_HOST", f"localhost:{ollama_port}")

    #Check if a custom port is being used and inform the user about it.
    if ollama_port != "11434":
        common.log_message(f"Custom Ollama port detected: {ollama_port}. Proceeding with this configuration.")
        print(f"Warning: Ollama running on custom port {ollama_port}.\n") #Debug

    #Check if Ollama localhost connection is running and provide ConnectionError or Timeout results.
    try:
        response = requests.get(f"http://{ollama_host}", timeout=2)
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
        common.log_message(f"It was not possible to establish connection to localhost. Please ensure port: {ollama_port} is accessible.")
        return False

def check_mistral_installed(retry= False):
    #Check if Mistral model has been downloaded within Ollama's models list.
    mistral_listed_check = subprocess.run(["ollama","list"], capture_output= True, text = True)

    if "mistral" in mistral_listed_check.stdout:
        print("AI Model installation found.\n") #Debug
        common.log_message("Mistral model installation found.")
        return True
    else:
        request_mistral_installation = messagebox.askyesno("Mistral model is missing. Would you like to install it?\n")
        if request_mistral_installation:
            try:
                common.log_message("Downloading Mistral model...This may take a while, depending on your connection. Please do not close this page.")
                print("Mistral model is now being downloaded.\n") #Debug
                subprocess.run(["ollama", "pull", "mistral"], check= True) #Downloads Mistral model.
                mistral_listed_check = subprocess.run(["ollama","list"], capture_output= True, text = True) #Update stored output.
                if "mistral" in mistral_listed_check.stdout:
                    print("Model has been installed successfully after initial failure.\n")
                    common.log_message("Model has been installed successfully.")
                    return True
                elif "mistral" not in mistral_listed_check.stdout:
                    if not retry:
                        print("First installation attempt failed, retrying...\n")
                        common.log_message("First installation or attempt to locate Mistral failed. Retrying...")
                        return check_mistral_installed(retry=True)
                    else:
                        common.log_message(
                        "Mistral model remains undetected. Please proceed with installation to continue.\n"
                        "To install Mistral, use your Command Prompt/Powershell or equivalent for other Operating Systems.\n"
                        "Then run the following command: 'ollama pull mistral'\n"
                        "You can check the status of the installation by running the following command: 'ollama list'")
                        print("User did not accept, or did not correctly install Mistral model. Steps were shared for installation, and application stopped running.\n") #Debug
                        return False
            except subprocess.CalledProcessError:
                common.log_message(f"A process error has occurred: {CalledProcessError}")
                print(f"A process error has occurred: {CalledProcessError}")
                return False
    return False

#This function was placed for structural purposes, as a checkpoint for function values: check_mistral_installed, check_ollama_running, and check_ollama_installed.
def local_llm_ready():
    if check_ollama_installed() and check_ollama_running() and check_mistral_installed():
        print("User meets all requirements. Initiating application.\n") #Debug
        common.log_message("All LLM requirements are met.")
        return True
    else:
        print("User does not meet all requirements.\n") #Debug
        return False