#MEMORY PROFILING

from tqdm import tqdm #install
import json
import sys
import time
import statistics     
import cProfile
from memory_profiler import profile


from line_profiler import LineProfiler##
from datetime import date, datetime
from pytz import timezone #install

START =0;
END=1;
SUCCESS = 1;
FAIL = 0;
NULL = None;
BAD_INPUT_MESSAGE = "...Bad input, please try again...";
JSON_PATH = "tweetdhead300000.json";


current_tweet = 1;
# CURRENT TWEET REFERS TO THE LINE
# IF YOU WANT TO ACCESS A LIST, REDUCE IT BY 1 :)
@profile
def main():

    #continuously prints the command board, waiting for user input
    try:
       #the file object becomes a global so it can be accessed throughout the program's operations without the need to open and close the file all the time (that way we don't have to save the altered .json every time)
       #the object will be closed when "q" or "x" are selected
       global f;
       global tweets;
       tweets = []; 
       f = open(JSON_PATH, 'r+');
    except OSError:
        print("Could not open/read file: ", JSON_PATH);
        sys.exit(FAIL);

    while(True):
        user_choice_list = user_choice_to_int_list(print_menu());
        if user_choice_list[0] == NULL:
            continue;
        else:
            case_picker(user_choice_list)


#prints the board of options returning a string with the user's choice ad infinitum
@profile
def print_menu() -> str:
    print("\
            \n+-------------+----------------------------------------------------------+\
            \n|   Command   |                      Description                         |\
            \n+-------------+----------------------------------------------------------+\
            \n|      c      | Create tweet by giving its “text”                        |\
            \n|  r <number> | Read the tweet with ID <number>                          |\
            \n|  u <number> | Update the tweet with ID <number> by giving its new text |\
            \n|      d      | Delete current tweet                                     |\
            \n|      $      | Read the last tweet in the file                          |\
            \n|      -      | Read one tweet up from the current tweet                 |\
            \n|      +      | Read one tweet down from your current tweet              |\
            \n|      =      | Print current tweet ID                                   |\
            \n|      q      | Quit without save                                        |\
            \n|      w      | (Over)write file to disk                                 |\
            \n|      x      | Exit and save                                            |\
            \n+-------------+----------------------------------------------------------+\
            \n\n");
    user_choice = str(input("Please enter the desired command: "));
    return user_choice;

# function to enable an easier and cleaner interpretation of user input by returning a list formatted as [COMMAND_NUMBER, NUMBER] where COMMAND_NUMBER is the number
# corresponding to the user's choice and NUMBER is the optional tweet ID (in the cases of "r" or "u")
# keep that formatting in mind when checking out case_picker()
@profile
def user_choice_to_int_list(user_choice: str) -> list:
    return_list = [NULL, NULL];
    #if there's a space in the user input then the user input probably selected either "r" or "u"
    if has_space(user_choice):
        user_choice = user_choice.split(" ");
        if user_choice[0] == "r":
            return_list[0] = 2;
            return_list[1] = int(user_choice[1]);
        elif user_choice[0] == "u":
            return_list[0] = 3;
            return_list[1] = int(user_choice[1]);
        else:
            #return [NULL, NULL] list. This signals an error and the program will fall back to the while(true) loop, asking again for user input
            print(BAD_INPUT_MESSAGE);
            return return_list;
    else:
        if user_choice == "c":
            return_list[0] = 1;
        elif user_choice == "d":
            return_list[0] = 4;
        elif user_choice == "$":
            return_list[0] = 5;
        elif user_choice == "-":
            return_list[0] = 6;
        elif user_choice == "+":
            return_list[0] = 7;
        elif user_choice == "=":
            return_list[0] = 8;
        elif user_choice == "q":
            return_list[0] = 9;
        elif user_choice == "w":
            return_list[0] = 10;
        elif user_choice == "x":
            return_list[0] = 11;
        else:
            print(BAD_INPUT_MESSAGE);
    return return_list;

# checks if a string contains a space
@profile
def has_space(string: str) -> bool:
    if " " in string:
        return True;
    else:
        return False;



# user_choice_to_int_list produces a list of integers with user's choice. Said choice is quickly checked through a match:case and the correct function is called
# with said function's return value being checked for errors
@profile
def case_picker(user_choice_list: list):
    match user_choice_list[0]:
                case 1:
                    error_checker(create_tweet());
                case 2:
                    error_checker(read_tweet(user_choice_list[1]));
                case 3:
                    error_checker(update_tweet(user_choice_list[1]));
                case 4:
                    error_checker(delete_tweet());
                case 5:
                    error_checker(read_last_tweet());
                case 6:
                    error_checker(read_one_up());
                case 7:
                    error_checker(read_one_down());
                case 8:
                    error_checker(print_current_tweet_id());
                case 9:
                    error_checker(quit_without_save());
                case 10:
                    error_checker(write_to_file());
                case 11:
                    error_checker(save_and_exit());
                case _:
                    print("What...?");

# returns datetime in this format -> Thu Sep 13 01:30:22 +0000 2012
@profile
def get_datetime() -> str:
    # pulls a datetime object through the datetime package in the UTC timezone
    now_utc = datetime.now(timezone("UTC"));
    # formats the object into a string to match the twitter API
    formatted = now_utc.strftime("%a %b %d %H:%M:%S %z %Y");
    return formatted;

# Checks each function's return value to determine exit status
# It has been disabled as to not interfere with user experience
def error_checker(return_value: int):
    '''print(".....");
    time.sleep(1);
    if return_value == SUCCESS:
        print("Success!");
    elif return_value == FAIL:
        print("Failure! Contact the program maintainer...");'''
    pass;

# Loads every tweet present in a JSON file into the tweets[] list
@profile
def load_tweets():

    # load_tweets is called when tweets[] is empty
    # we count the number of lines in the file, then append each line to the tweets list
    # we could get better code performance by ditching the line counting and tqdm but I feel like it's negligeble, especially compared to the 
    # proggress bar functionality. I'll leave it upon the refactoring team to figure this one out 
    # NOTE FIXME MARAKH DES EDW: "count = len(open('/path/to/the/file.ext').readlines())" FIXME FIXME XXX
    tweet_count = 0;
    for line in f:
        tweet_count += 1;
    f.seek(0);
    for line in tqdm(f, total=tweet_count):
        tweets.append(json.loads(line));

#START OF CORE FUNCTIONS

# Creates a tweet
# Command: c
@profile
def create_tweet() -> int:
    create_tweet_time = 0;
    # reads new tweet text from user
    tweet_text = str(input("Please enter tweet text: "));
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();  
    # formats data given by user and creation time pulled from the user's system into a JSON
    new_tweet = {"text":tweet_text, "created_at":get_datetime()};
    # appends new tweet to tweets[]
    tweets.append(new_tweet);
    # updates current_tweet accordingly
    global current_tweet; 
    current_tweet = len(tweets);

    return SUCCESS;

# Reads tweet at given ID
# Command: r <tweet_id>
@profile
def read_tweet(id: int) -> int:

    # NOTE typing in "r 1" will read tweets[0]. MAKE SURE CONVENTION IS ADHEERED TO NOTE
    # current_tweet is updated
    global current_tweet;
    current_tweet = id;
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();
    # translates the desired line (start at 1) to the correct list entry (starting at 0)
    tweet_to_read = tweets[current_tweet-1];
    # we could instantly print json.dumps(tweet_to_read["text"]); to avoid loading it into a variable and improve memory usage somewhat, though it's probably negligible,
    # with the current configuration providing much needed visual clarity
    tweet_text = json.dumps(tweet_to_read["text"]);
    tweet_date = json.dumps(tweet_to_read["created_at"]);
    print("\nText: {text}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nCreated at: {created_at}".format(text = tweet_text, created_at = tweet_date));

    return SUCCESS;

# Updates tweet at given ID
# Command: u <tweet_id>
@profile
def update_tweet(id: int) -> int:
    global current_tweet;
    current_tweet = id;
    tweet_text = str(input("Please enter tweet text: "));
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();
    # creates a new minimalistic JSON that will replace the existing tweet
    # NOTE by minimalistic JSON I mean a JSON file that only contains "text" and "created_at" entries NOTE
    new_tweet = {"text":tweet_text, "created_at":get_datetime()};
    tweets[current_tweet-1] = new_tweet;

    return SUCCESS;

# Deletes a current_tweet
# Command: d
@profile
def delete_tweet() -> int:
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();
    # if deleted tweet isn't the last one, replace tweet #X with tweet #X+1 until tweet #N-1 has been replaced by tweet #N (where N the total number of tweets). 
    # Then pop the last tweet
    if(current_tweet != len(tweets)):
        for i in range(current_tweet-1, len(tweets)-1):
            tweets[i] = tweets[i+1];
    tweets.pop(len(tweets)-1);

    return SUCCESS;


# Reads the last tweet present in the file
# Command: $
@profile
def read_last_tweet() -> int:
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();
    # tweets[-1] could be used for a more pythonic feel but that'd mess with the setting of current_tweet
    read_tweet(len(tweets));
    return SUCCESS;

# For current_tweet = X, reads X+1
# Command: -
@profile
def read_one_up() -> int:
    # if current_tweet is the last one in the list then we can't read the next tweet (it doesn't exist)
    if(current_tweet == len(tweets)):
        print("Current tweet is the last one in the file. Can't read one up!");
        return FAIL;
    # loads tweets if tweets[] is empty
    if(len(tweets) == 0):
        load_tweets();
    read_tweet(current_tweet + 1);
    return SUCCESS;

# For current_tweet = X, reads X-1
# Command: +
@profile
def read_one_down() -> int:
    # if tweets[] is empty then current_tweet is 1. That means that we can't read a tweet down (line 0)
    if(len(tweets) == 0):
        print("Initial current_tweet is 1 (the 1st one). Can't read tweet #0!\nQuitting...");
        return FAIL;
    read_tweet(current_tweet - 1);
    return SUCCESS;

# Prints current_tweet in a clean, pythonic manner
# Command: =
@profile
def print_current_tweet_id() -> int:
    print("Current tweet id: {id}".format(id = current_tweet));
    return SUCCESS;

# Prints a goodbye message, closes the file object and exits the program
# Command: q
@profile
def quit_without_save() -> int:
    print("Quitting without saving... Thanks for using our Twitter viewer!");
    f.close();
    quit(SUCCESS);

# Writes tweets[] to the file we operate on
# Command: w
@profile
def write_to_file() -> int:

    # saves time by not writing anything to the file if load_tweets() hasn't been called
    if(len(tweets) == 0):
        print("No changes to write to disk...");
        return FAIL;
    # goes to the start of the file and deletes everything
    f.seek(0);
    f.truncate();
    # for every tweets[] entry, writes the tweet to the file
    # ensures that a new tweet will be written to a new line by appending an EOL character at the end of each tweet .JSON
    for tweet in tqdm(range(len(tweets)), total=len(tweets)):
        json.dump(tweets[tweet], f);
        f.write("\n");
    return SUCCESS;

# saves current tweets[], closes the file object and quits the program
# Command: x
@profile
def save_and_exit() -> int:
    # calls write_to_file(), closes the file object and quits
    write_to_file();
    f.close()
    quit(SUCCESS);

#END OF CORE FUNCTIONS

# makes sure that the file doesn't run automatically if imported
if __name__ == '__main__':
    main()