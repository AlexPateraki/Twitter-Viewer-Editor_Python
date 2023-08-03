# make sure to import the following packages
import json
import os
from datetime import datetime
from pytz import timezone

SUCCESS = 1
FAIL = 0
NULL = None
BAD_INPUT_MESSAGE = "...Bad input, please try again..."
JSON_PATH = "tweetdhead300000.json"
NEW_JSON_PATH = "tweetdhead300000_new.json"

CURRENT_TWEET = 1  # points out the current tweet
OFFSET_LIST = []  # list saving the length of each line of the file including the new line character


# CURRENT TWEET REFERS TO THE LINE
# IF YOU WANT TO ACCESS A LIST, REDUCE IT BY 1 :)


def main():
    """ continuously prints the command board, waiting for user input
     the file object becomes global, so it can be accessed throughout the program's operations without the need to
     open and close the file all the time (that way we don't have to save the altered .json every time)
     the object will be closed when "q" or "x" are selected
    """
    create_list()
    while True:
        user_choice_list = user_choice_to_int_list(print_menu())
        if user_choice_list[0] == NULL:
            continue
        else:
            case_picker(user_choice_list)


# prints the board of options returning a string with the user's choice
def print_menu() -> str:
    print("\
            \n+-------------+----------------------------------------------------------+\
            \n|   Command   |                      Description                         |\
            \n+-------------+----------------------------------------------------------+\
            \n|      c      | Create tweet by giving its “text”                        |\
            \n|  r  | Read the tweet with ID                           |\
            \n|  u  | Update the tweet with ID  by giving its new text |\
            \n|      d      | Delete current tweet                                     |\
            \n|      $      | Read the last tweet in the file                          |\
            \n|      -      | Read one tweet up from the current tweet                 |\
            \n|      +      | Read one tweet down from your current tweet              |\
            \n|      =      | Print current tweet ID                                   |\
            \n|      q      | Quit without save                                        |\
            \n|      w      | (Over)write file to disk                                 |\
            \n|      x      | Exit and save                                            |\
            \n+-------------+----------------------------------------------------------+\
            \n\n")
    user_choice = str(input("Please enter the desired command: "))
    return user_choice


def user_choice_to_int_list(user_choice: str) -> list:
    """function to enable an easier and cleaner interpretation of user input by returning a list formatted as
    [COMMAND_NUMBER, NUMBER] where COMMAND_NUMBER is the number corresponding to the user's choice and NUMBER is the
    optional tweet ID (in the cases of "r" or "u") keep that formatting in mind when checking out case_picker()
    :param user_choice: string user's input
    :return: list saving each command respectively as a number and if needed the position of the line to update/read
    """
    return_list = [NULL, NULL]

    input_dict = {"c": 1, "r": 2, "u": 3, "d": 4, "$": 5, "-": 6, "+": 7, "=": 8, "q": 9, "w": 10, "x": 11}
    must_have_id = ["r", "u"]
    user_choice = user_choice.split(" ")
    if user_choice[0] in input_dict:
        return_list[0] = input_dict[user_choice[0]]
        if user_choice[0] in must_have_id:
            if len(user_choice) == 2:
                try:
                    return_list[1] = int(user_choice[1])
                except Exception as e:
                    print("{bad_input}\nFailed to convert given id to integer\nError message: {error_id}".format(
                        bad_input=BAD_INPUT_MESSAGE, error_id=e))
                    return_list[0] = None
            else:
                return_list[0] = None
                print("{bad_input}\nSelected input must be accompanied by a tweet ID".format(
                    bad_input=BAD_INPUT_MESSAGE))
        else:
            print(
                "{bad_input}\nDesired operation doesn't require a second argument".format(bad_input=BAD_INPUT_MESSAGE))
            return_list[0] = None
    else:
        print(BAD_INPUT_MESSAGE)
    return return_list


def case_picker(user_choice_list: list):
    """  Calls the appropriate function based on user input
    :param user_choice_list: the list generated by user_choice_to_int_list(), containing the user's choice as an int and
    the optional ID
    """
    match user_choice_list[0]:
        case 1:
            error_checker(create_tweet())
        case 2:
            error_checker(read_tweet(user_choice_list[1]))
        case 3:
            error_checker(update_tweet(user_choice_list[1]))
        case 4:
            error_checker(delete_tweet())
        case 5:
            error_checker(read_last_tweet())
        case 6:
            error_checker(read_one_up())
        case 7:
            error_checker(read_one_down())
        case 8:
            error_checker(print_current_tweet_id())
        case 9:
            error_checker(quit_without_save())
        case 10:
            error_checker(write_to_file())
        case 11:
            error_checker(save_and_exit())
        case _:
            print("What...?")


def get_datetime() -> str:
    """
    :return: datetime in this format -> Thu Sep 13 01:30:22 +0000 2012
    """
    # pulls a datetime object through the datetime package in the UTC timezone
    now_utc = datetime.now(timezone("UTC"))
    # formats the object into a string to match the twitter API
    formatted = now_utc.strftime("%a %b %d %H:%M:%S %z %Y")
    return formatted


def error_checker(return_value: int):
    """Checks each function's return value to determine exit status.
    It has been disabled as to not interfere with user experience
    """
    """print(".....")
    time.sleep(1)
    if return_value == SUCCESS:
        print("Success!")
    elif return_value == FAIL:
        print("Failure! Contact the program maintainer...")"""
    pass


def create_list():
    """Populates the tweets[] list with as many entries as the file has lines, where tweets[index] = index
    """
    global tweets
    with open(JSON_PATH, 'r') as f:
        number_of_lines = sum(1 for line in f)
        tweets = [i for i in range(number_of_lines)]


def get_line_from_file(f, line_offset: int) -> str:
    """Returns the selected line from the file, given its offset. Moves file cursor to line_offset,
    reads the line into a variable, resets the pointer and returns the variable
    :param f: file  object to the file we want to pull the line from (object of )
    :param line_offset: the offset of the line from the file's start
    :return: string of read line
    """
    f.seek(line_offset)
    pulled_line = f.readline()
    f.seek(0)
    return pulled_line


def get_offset_list(filename) -> list:
    """Returns a list with the offset of every line in a file. Opens the file in rb (r will always be a byte short),
    reads the length of every line and adds it to the offset variable, appending offset at every turn,
    the array looking like [0, x, x+y, x+y+z, ..., total_chars-len(final-line)]
    :param filename: the name of the file whose line offsets will be mapped
    """
    with open(filename, 'rb') as f:
        global OFFSET_LIST
        offset = 0
        for line in f:
            OFFSET_LIST.append(offset)
            offset += len(line)
        f.seek(0)
        return OFFSET_LIST


# START OF CORE FUNCTIONS


def create_tweet() -> int:
    """function for command "c". At first, reading new tweet text from user, creates a tuple of new text and
    the date time-using get_datetime()- then appends new tweet to tweets[] and updates current_tweet accordingly
    """
    tweet_text = str(input("Please enter tweet text: "))
    new_tweet = (tweet_text, get_datetime())
    tweets.append(new_tweet)
    global CURRENT_TWEET
    CURRENT_TWEET = len(tweets)
    return SUCCESS


def read_tweet(id: int) -> int:
    """ function for command "r". Reads tweet at specific ID.
    NOTE typing in "r 1" will read tweets[0]. MAKE SURE CONVENTION IS ADHERED TO NOTE
    :param id: tweet id that user demands to read
    """
    # current_tweet is updated
    global CURRENT_TWEET
    CURRENT_TWEET = id
    # translates the desired line (start at 1) to the correct list entry (starting at 0)
    tweet_index = CURRENT_TWEET - 1
    # if tweet_index is an int then file is opened to find the line and then text and also date
    # else if it is a tuple then registers immediately text and date
    if isinstance(tweets[tweet_index], int):
        with open(JSON_PATH, 'r') as f:
            tweet_to_read = json.loads((get_line_from_file(f, OFFSET_LIST[tweets[tweet_index]])))
            tweet_text = tweet_to_read["text"]
            tweet_date = tweet_to_read["created_at"]
    else:
        tweet_text = tweets[tweet_index][0]
        tweet_date = tweets[tweet_index][1]

    print(
        "\nText: {text}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nCreated at: {created_at}"
        .format(text=tweet_text, created_at=tweet_date))
    return SUCCESS


def update_tweet(id: int) -> int:
    """function for command "u". Updates tweet at given ID by creating a json that is replacing the existing tweet
    Now JSON file only contains "text" and "created_at"
    """
    global CURRENT_TWEET
    CURRENT_TWEET = id
    tweet_text = str(input("Please enter tweet text: "))
    new_tweet = (tweet_text, get_datetime())
    tweets[CURRENT_TWEET - 1] = new_tweet
    return SUCCESS


def delete_tweet() -> int:
    """function for command "d".Deletes a current_tweet. If deleted tweet isn't the last one, replace tweet #X
    with tweet #X+1 until tweet #N-1 has been replaced by tweet #N (where N the total number of tweets).
    Then pop the last tweet
    """
    if CURRENT_TWEET != len(tweets):
        for i in range(CURRENT_TWEET - 1, len(tweets) - 1):
            tweets[i] = tweets[i + 1]
    tweets.pop(len(tweets) - 1)
    return SUCCESS


def read_last_tweet() -> int:
    """ function for command "$". Reads the last tweet present in the file
    """
    read_tweet(len(tweets))
    return SUCCESS


def read_one_up() -> int:
    """function for command "-". For current_tweet = X, reads X+1
    if current_tweet is the last one in the list then we can't read the next tweet (it doesn't exist)
    """
    if CURRENT_TWEET == len(tweets):
        print("Current tweet is the last one in the file. Can't read one up!")
        return FAIL
    read_tweet(CURRENT_TWEET + 1)
    return SUCCESS


def read_one_down() -> int:
    """function for command "+". For current_tweet = X, reads X-1
    """
    # if tweets[] is empty then current_tweet is 1. That means that we can't read a tweet down (line 0)
    if CURRENT_TWEET == 1:
        print("current_tweet is 1 (the 1st one). Can't read tweet #0!\nQuitting...")
        return FAIL
    read_tweet(CURRENT_TWEET - 1)
    return SUCCESS


def print_current_tweet_id() -> int:
    """function for command "=". Prints current_tweet using format() method
    """
    print("Current tweet id: {id}".format(id=CURRENT_TWEET))
    return SUCCESS


def quit_without_save() -> int:
    """function for command "q". Prints a goodbye message, closes the file object and exits the program
    """
    print("Quitting without saving... Thanks for using our Twitter viewer!")
    quit(SUCCESS)


def write_to_file() -> int:
    """function for command "w".
    Saves the changes made by the user into a file.Creates a new file where the changes are written.
    It checks every entry in tweets[] entry to verify if it's integer or tuple. If it's an integer it writes line
    #tweets[index] from the old file into the new one. If the entry is a tuple it consructs a Python dictionary from its
    contents and converts said dictionary into a JSON string before writing it into the file, all with the help of
    json.dump, making sure to append an EOL character in the end. When the end of the tweets[] is reached
    It deletes the old file, with the new one taking its name.
    """
    with open(NEW_JSON_PATH, 'w') as f_write:
        with open(JSON_PATH, 'r') as f_read:
            for tweet in tweets:
                if isinstance(tweet, int):
                    f_write.write(get_line_from_file(f_read, OFFSET_LIST[tweet]))
                elif isinstance(tweet, tuple):
                    dict_tmp = {"text": tweet[0], "created_at": tweet[1]}
                    json.dump(dict_tmp, f_write)
                    f_write.write("\n")
                else:
                    print("Oops, unexpected datatype detected!")
                    return FAIL
    os.remove(JSON_PATH)
    os.rename(NEW_JSON_PATH, JSON_PATH)
    return SUCCESS


def save_and_exit() -> int:
    """function for command "x". Saves current tweets[] by calling write_to_file(), closes the file object and
    quits the program
    """
    write_to_file()
    quit(SUCCESS)


# END OF CORE FUNCTIONS

# makes sure that the file doesn't run automatically if imported
if __name__ == '__main__':
    get_offset_list(JSON_PATH)
    main()