import os 

# ---------- DIRECTORIES NAVIGATION ----------

def dir_info():
    """dir_info() --> [current directory string], [directories list], [files list]
       Calls the os module methods and returns the main datas concerning the current directory: its name, the directories
       in there and the files contained """

    cwd = os.getcwd()
    walk = os.walk(cwd)

    this_dir = next(walk)
    return cwd, this_dir[1], this_dir[2]

def is_cd_input(user_input):
    """ is_cd_input([user input string]) --> [dir name string] OR False
    if the user input is a change directory command returns just the directory name, otherwise returns false"""

    split_input = user_input.split()

    if split_input[0] == "cd" and len(split_input) > 1:
        return " ".join(split_input[1:])
    elif split_input[0] == "cd" and len(split_input) == 1:
        return " "
    else:
        return False

def issue_cd_command(dir_name, dirs_list, home_dir):
    """ issue_cd_command([dir name string]) --> None
    change the current directory, if the command cd was empty returns to home directory, if the command was .. returns to parent directory"""

    if dir_name in dirs_list:
        os.chdir(dir_name)

    elif dir_name == " ":
        os.chdir(home_dir)

    elif dir_name == "..":
        cwd = os.getcwd()
        os.chdir( os.path.split(cwd)[0] ) 
        
def list_to_string(items):
    """ list_to_string([list]) --> [string]
    returns a single string listing all the items in the list"""

    if not items:
        return "\033[31mNO ITEMS HERE\033[0m"

    brackets_off = str(items)[2:-2]
    splitted = brackets_off.split("', '")
    joined = " ,".join(splitted)

    return joined

#---------- SRT HANDLING ----------

def filter_srt(files):
    """ filter_srt([files list]) --> [filtered list]
    the returned list of filenames will contain only filenames with .srt extension """

    out = []
    for filename in files:
        splitted = os.path.splitext(filename)
        srt_identifier = ".srt"
        if splitted[1] == srt_identifier: 
            out.append(filename)

    return out 

def extract_srt(filename):
    """ extract_srt([filename string]) --> [lines list]
        Returns a list containing all the lines in a srt file"""

    srt_file = open(filename, "r")
    lines = srt_file.readlines()
    srt_file.close()
    print(lines[:50])

    return lines

def extract_time(line):
    """extract_time([srt line]) --> [timestamps dict] OR False 
    First controls if the line is a timestamp line, if it is returns a dictionary with all the timestamps organized by hours, minutes and seconds;
    otherwise returns False"""

    dcolon_indexes = (2,5,19,22)
    try:
        for i in dcolon_indexes:
            if line[i] != ":":
                return False
    except IndexError:
        return False

    out = { "h" : [int(line[0:2]), int(line[17:19])],
            "m" : [int(line[3:5]), int(line[20:22])],
            "s" : [float(line[6:8] + "." + line[9:12]), float(line[23:25] + "." + line[26:29])] }
    return out

def add_time(user_input, timestamps): 
    """add_time([input float], [timestamps dict]) --> [new timestamp dict]
    Adds the seconds (user input) to the old timestamp dict and returns it with the changes applied"""

    while user_input > 0:

        for index in range(2):
            seconds = timestamps['s'][index] + user_input

            if seconds >= 60:
                minutes = timestamps['m'][index] + 1
                if minutes >= 60:
                    timestamps['h'][index] += 1
                    minutes -= 60
                timestamps['m'][index] = minutes
                seconds -= 60

            elif seconds < 0:
                minutes = timestamps['m'][index] - 1
                if minutes < 0:
                    timestamps['h'][index] -= 1
            else:
                timestamps['s'][index] = seconds

        user_input -= 60

    return timestamps
                

def apply_new_time(lines_list, user_input):
    """ apply_new_time([lines list], [user input string]) --> [updated lines list]
    returns the new timestamp string for the srt file with the user modification applied """
    
    for line in lines_list:
        pass


    


# ----------INPUT AUTOCOMPLETE ----------

def autocomplete(partial_str, collection):
    """autocomplete([user input string], [items list]) --> [full item string]
       Returns the complete name starting from the first letters, if there are multiple matches calls
       the select_options function """
    options = []

    for item in collection:
        if item.startswith(partial_str) or item.lower().startswith(partial_str):
            options.append(item)

    if len(options) == 0:
        print("\033[31;1mError\033[0m characters entered don't match with any item")
        return
    elif len(options) == 1:
        return options[0]
    elif len(options) > 1:
        return select_options(options)

def select_options(options):
    """select_options([options list]) --> [selected option string]
       Through the user input one of multiple string options is selected and returned"""

    print("""

characters entered match  with the following, choose one:
-----------------------------""")

    for item in options:
        num = str(options.index(item))
        print(num + ") " + item)

    prompt = input("""------------------
enter the option's number: """)

    try:
        index = int(prompt) 
    except ValueError:
        print("\033[31;1mError\033[0m invalid input, enter a number")
        return
    try:
        return options[index]
    except IndexError:
        print("\033[31;1mError\033[0m you must enter one of the given numbers")
        return

# ---------- TERMINAL USER INPUT ---------

def main():

    JUST_STARTED = True

    """ if you've just started the program here will be defined the home directory (the directory where is located the program) """
    if JUST_STARTED:
        home_dir = os.getcwd()
        JUST_STARTED = False

    """ Now starts the main loop """
    while True:

        """ defining general infos about current directory"""
        cwd, dirs_list, files_list = dir_info()
        srt_list = filter_srt(files_list)
        
        """turning the lists in strings"""
        dirs_list_string = list_to_string(dirs_list)
        srt_list_string = list_to_string(srt_list)

        """ Now will be printed the general infos about the directory and defined the main prompt """
        print("""

\033[33;1mCurrent directory:\033[0m %s
\033[33;1mDirectories list:\033[0m %s
\033[33;1msrt files:\033[0m %s
---------------------------------------
if you're lost enter '?'
to quit enter 'q'""" % (cwd, dirs_list_string, srt_list_string))
        main_prompt = input("")

        is_cd = is_cd_input(main_prompt)

        """ The user input will be confronted with all the possible commands """
        # Quit
        if main_prompt == "q":
            break

        # Change directory
        elif is_cd:
            if is_cd == " " or is_cd == "..":
                dir_str = is_cd
            else:
                dir_str = autocomplete(is_cd, dirs_list)
            issue_cd_command(dir_str, dirs_list, home_dir)

if __name__ == "__main__":
    main()

