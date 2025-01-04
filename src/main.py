##########################################################
# Anki AI Toolkit - Main Script
# (c)pschuelpen.tec
#
# www.tec.pschuelpen.com/anki_ai_toolkit/
#
# Program for AI Generation
#
# Optimized for:
# Python3 - Running on any computer - Docker
#
##########################################################
# Import Libraries
##########################################################


# System Libs
import os
import sys

# Libs
import yaml

# Custom Libs
from ap_generateanki import AnkiDeckGenerator
from ap_pdftoqa import PDFToQA


#####################################
#            Functions
#####################################

# Debug Print
def print_d(message, type=0):
    t_m = "Debug"

    if type == 1:
        t_m = "Info"

    if type == 2:
        t_m = "Caution"
    
    if type == 3:
        t_m = "Warning"
    
    if type == 4:
        t_m = "Error"

    # Only if it is an Error it will be displayed 
    if DEBUG_FLAG or type == 4:
        print(f"[{t_m}] {message}")


# Load Credentials from config.yaml
def load_credentials(filepath):
    try:
        with open(filepath, 'r') as file:
            credentials = yaml.safe_load(file)
            openai_key = credentials['openai-api-key']
            return openai_key
    except Exception as e:
        print_d("Failed to load credentials: {}".format(e), type=4)
        print_d("Config could not be loaded - Please create a config file first -> Read the Docs", type=4)
        sys.exit("[System] Program execution ended")


#####################################
#              Init
#####################################

# Debug Flag - Set True if Developing
DEBUG_FLAG = True
version = "1.0.6(Beta)"

# Load API-Key
openai_api_key = load_credentials("./config.yaml")

# Foreground colors
COLORS = {
    "BLACK": '\033[30m',
    "RED": '\033[31m',
    "GREEN": '\033[32m',
    "YELLOW": '\033[33m',
    "BLUE": '\033[34m',
    "MAGENTA": '\033[35m',
    "CYAN": '\033[36m',
    "WHITE": '\033[37m',
    "RESET": '\033[0m',
}

# Styles
STYLES = {
    "BOLD": '\033[1m',
    "UNDERLINE": '\033[4m',
    "BLINK": '\033[5m',
    "REVERSE": '\033[7m',
    "HIDE": '\033[8m',
    "RESET": '\033[0m',
}



#####################################
#              MAIN
#####################################

if __name__ == "__main__":
    # Init Print
    print(f"\n{45 * "* "}\n")
    print(r"""
                 _    _            _____   _______          _ _    _ _   
     /\         | |  (_)     /\   |_   _| |__   __|        | | |  (_) |  
    /  \   _ __ | | ___     /  \    | |______| | ___   ___ | | | ___| |_ 
   / /\ \ | '_ \| |/ / |   / /\ \   | |______| |/ _ \ / _ \| | |/ / | __|
  / ____ \| | | |   <| |  / ____ \ _| |_     | | (_) | (_) | |   <| | |_ 
 /_/    \_\_| |_|_|\_\_| /_/    \_\_____|    |_|\___/ \___/|_|_|\_\_|\__|
                                                                         
    """)
    print(f"\n\n{45 * "* "}\n\n[System] Anki AI-Toolkit \n[System] by pschuelpen (c)2025 \n[System] Version V{version} \n\n {45 * "* "}\n")

    # Loop Through as long as not terminated
    try:
        # While count & Max Count to break when 
        w_count = 0
        w_count_max = 10

        while True:
            # Check Directory for files - PDF
            dir_path_pdf = "/usr/app/resources/pdf"
            pdf_items = os.listdir(dir_path_pdf)

            # Append all files
            files = [item for item in pdf_items if os.path.isfile(os.path.join(dir_path_pdf, item)) and item.lower().endswith('.pdf')]


            # Only if There are Files
            if len(files) > 0:
                print(f"[System] Please select a pdf file you want to use. Select by entering the number {COLORS['YELLOW']}[i]{COLORS['RESET']}")
                print(f"[System] {COLORS['YELLOW']}{len(files)}{COLORS['RESET']} Files found")
                print(f"\nList:\n{45 * '_ '}\n")
                for i, file in enumerate(files):
                    print(f"{COLORS['YELLOW']}[{i}]{COLORS['RESET']} -> {COLORS['GREEN']}{file}{COLORS['RESET']}")
                
                print(f"{45 * '_ '}\n")
            else:
                # Exit if no Files found
                print(f"[System] No pdf Files found in Directory - '{dir_path_pdf}' :: Check your Files")
                sys.exit("[System] Program execution terminated")

            ###
            # File Selection Input

            cont_flag = True
            cont_it = 1
            cont_it_max = 3

            while cont_flag:
                if cont_it == 1:
                    user_input = input(f"[System] Please enter your selection {COLORS['YELLOW']} i {COLORS['RESET']}: ")
                else:
                    user_input = input(f"[System] Retry again {COLORS['YELLOW']} i {COLORS['RESET']} - Number only! : ")
                
                # Try to INT Conversion
                try:
                    file_selection = int(user_input)
                    # We break out of the Loop if 
                    if file_selection >= 0 and file_selection <= len(files):
                        cont_flag = False
                        break
                    else:
                        print(f"[System] Input out of bound ! - Max number {COLORS['YELLOW']}{len(files) - 1}{COLORS['RESET']}")
                except Exception as e:
                    print_d(e, type=1)
                    print(f"[System] Input is not a number")
                
                # Terminate after max tries
                if cont_it >= cont_it_max:
                    print("[System] Maximum Tries - Only input Numbers")
                    sys.exit("[System] Program execution terminated")
                    break
                
                # Increase Count
                cont_it += 1


            selected_file_name = files[file_selection]
            print(f"[System] Selected File: {selected_file_name}")

            ###
            # Init Classes

            print("[System] Continue Execution - Starting Main Program")

            # PDF to QA - No Web Search init
            pdf_to_qa = PDFToQA(openai_api_key, None, None)

            # Generate Q&A Pairs
            qa_pairs = pdf_to_qa.process_pdf_to_qa(f"{dir_path_pdf}/{selected_file_name}", max_pairs=15, use_web_search=False)

            print(f"[System] Pairs generated - {COLORS['GREEN']}{len(qa_pairs)} Pairs{COLORS['RESET']}")

            # Define Deck Name
            package_name = input("[System] Please name the package: ")

            # Deck Class init
            anki_deck_generator = AnkiDeckGenerator(package_name)



            with open(f"/usr/app/resources/csv/{package_name}.csv", "w") as file:
                for i, (question, answer) in enumerate(qa_pairs, start=1):
                    # Uncomment to reveal all Q&A in Terminal
                    #print(f"[System] Card {i} \nQ: {question} \nA: {answer}\n")
                    
                    # Write redundant Q&A csv File
                    file.write(f"{i};{question};{answer}\n")

                    # Add to Deck
                    anki_deck_generator.add_card(question, answer)

            
            print(f"[System] Generating Anki Package - Name: {package_name}")
            anki_deck_generator.generate_package(f"/usr/app/resources/anki/{package_name}.apkg")

            print("[System] Success - Anki Package generated")

            # Break out if Max Runs exceeded
            w_count += 1
            if w_count >= w_count_max:
                print_d("Max Runs exceeded - Breaking out", type=2)
                break

            ###
            # Select options to continue
            
            # Separator
            print(f"\n{45 * '* '}\n")

            print(f"[System] Select your options to continue")

            print(f"\n{45 * '_ '}\n")
            print(f"{COLORS['GREEN']}[0]{COLORS['RESET']} -> Continue to next Package")
            print(f"{COLORS['GREEN']}[1]{COLORS['RESET']} -> Exit")
            print(f"{45 * '_ '}\n")


            cont_flag = True
            cont_it = 1

            while cont_flag:
                if cont_it == 1:
                    user_input = input(f"[System] Select your options to continue {COLORS['GREEN']} i {COLORS['RESET']}: ")
                else:
                    user_input = input(f"[System] Retry again {COLORS['GREEN']} i {COLORS['RESET']} - Number only! : ")
                
                # Try to INT Conversion
                try:
                    options = int(user_input)
                    # We break out of the Loop if 
                    if options >= 0 and options <= 1:
                        cont_flag = False
                        break
                    else:
                        print(f"[System] Input out of bound ! - Max number {COLORS['YELLOW']}1{COLORS['RESET']}")
                except Exception as e:
                    print_d(e, type=1)
                    print(f"[System] Input is not a number")
                
                # Terminate after max tries
                if cont_it >= cont_it_max:
                    print("[System] Maximum Tries - Only input Numbers")
                    sys.exit("[System] Program execution terminated")
                    break
                
                # Increase Count
                cont_it += 1

            # Separator
            print(f"\n{45 * '* '}\n")

            # If 
            if options == 1:
                print("[System] Program Terminated by choice")
                break
            else:
                print("[System] Program Continued by choice")



    except KeyboardInterrupt:
        # Separator
        print(f"\n{45 * '* '}\n")
        print("\n[System] Terminated by User Input --> ^C")
    except Exception as e:
        # Separator
        print(f"\n{45 * '* '}\n")
        print_d(f"Error occured - {e}", type=4)

    # END
    print("[System] Program ended - Thanks for using Anki AI-Toolkit")