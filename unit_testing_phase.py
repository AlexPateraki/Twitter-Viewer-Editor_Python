from datetime import datetime
import io
import sys
from pytz import timezone  # install
import unittest
import refactor
from unittest.mock import Mock, patch

original_JSON = []
#That's how many tweets(lines) dummy.json has
NUM_OF_LINES = 5


def get_datetime() -> str:
    # pulls a datetime object through the datetime package in the UTC timezone
    now_utc = datetime.now(timezone("UTC"));
    # formats the object into a string to match the twitter API
    formatted = now_utc.strftime("%a %b %d %H:%M:%S %z %Y");
    return formatted;

class TestRefactor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print('setupClass was called once at the beginning of the unit tests')

    @classmethod
    def tearDownClass(cls):
        print('teardownClass was called once at the end of the unit tests')



    #   setUp() & tearDown() reset file and memory before/after every unittest

    def setUp(self):
        refactor.JSON_PATH = "dummy.json"
        refactor.NEW_JSON_PATH = "dummy_new.json"
        refactor.create_list()
        refactor.get_offset_list(refactor.JSON_PATH)
        with open(refactor.JSON_PATH, "r") as f:
            global original_JSON
            original_JSON = f.read().splitlines()
    
    def tearDown(self):
        with open(refactor.JSON_PATH, "w") as f:
            f.write("\n".join(original_JSON))
        refactor.current_tweet = 1


    @patch('refactor.input', return_value='r 5')
    def test_print_menu(self, input):
        print("\n\n\n" + "PRINT MENU TEST" + "\n\n\n")
        self.assertEqual(refactor.print_menu(), "r 5");

    def test_has_space(self):
        print("\n\n\n" + "HAS SPACE TEST" + "\n\n\n")
        self.assertTrue(refactor.has_space("string with space"));
        self.assertFalse(refactor.has_space("string_without_space"));


    def test_get_datetime(self):
        print("\n\n\n" + "GET DATE TIME TEST" + "\n\n\n")
        self.assertEqual(refactor.get_datetime(), get_datetime());


    def test_create_list(self):
        print("\n\n\n" + "CREATE LIST TEST" + "\n\n\n")
        self.assertEqual(refactor.create_list()[0], 0)
        self.assertEqual(len(refactor.create_list()), 5)


    def test_user_choice_to_int_list(self):
        print("\n\n\n" + "CHOISE TO INT LIST TEST" + "\n\n\n")
        self.assertEqual(refactor.user_choice_to_int_list("c"), [1, None]);
        self.assertEqual(refactor.user_choice_to_int_list("r 5"), [2, 5]);
        self.assertEqual(refactor.user_choice_to_int_list("c "), [None, None]);
        self.assertEqual(refactor.user_choice_to_int_list("ObviouslyBadInput"), [None, None]);

    def test_case_picker(self):
        print("\n\n\n" + "CASE PICKER TEST" + "\n\n\n")
        self.assertEqual(refactor.case_picker([8, None]), 8)
        self.assertEqual(refactor.case_picker([2, 1]), 2)
        self.assertEqual(refactor.case_picker([123456, None]), -1)


    #Calls create_tweet() twice with "created_tweet" as an argument
    #and checks two tweets were added to the tweets[] list
    @patch('refactor.input', return_value='created tweet')
    def test_create_tweet(self, input):
        print("\n\n\n" + "CREATE TWEET TEST" + "\n\n\n")

        refactor.create_tweet()
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+1)
        self.assertEqual(refactor.tweets[NUM_OF_LINES][0], "created tweet")

        refactor.create_tweet()
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+2)
        self.assertEqual(refactor.tweets[NUM_OF_LINES][0], "created tweet")
        

    #Calls read_tweet() and capture the console output
    #Then checks the first line of the caprured string
    @patch('refactor.input', return_value='updated tweet')
    def test_read_tweet(self, input):
        print("\n\n\n" + "READ TWEET TEST" + "\n\n\n")

        #Check function with no changes applied
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_tweet(3)
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm tweet #3")

        #Check function after a deletion
        refactor.delete_tweet()
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        refactor.read_tweet(3)
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm the 4th one")

        #Check function after an update
        refactor.update_tweet(3)
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_tweet(3)
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES-1)
        

    #Calls update_tweet() twice with "updated_tweet" as an argument
    #and checks if changes were applied correctly
    @patch('refactor.input', return_value='updated tweet')
    def test_update_tweet(self, input):
        print("\n\n\n" + "UPDATE TWEET TEST" + "\n\n\n")

        refactor.update_tweet(3)
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)
        self.assertEqual(refactor.tweets[2][0], "updated tweet")
        refactor.update_tweet(1)
        
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)
        self.assertEqual(refactor.tweets[0][0], "updated tweet")

    #Calls delete_tweet() in different cases and checks
    #if changes were applied correctly
    def test_delete_tweet(self):
        print("\n\n\n" + "DELETE TWEET TEST" + "\n\n\n")

        #Check that everything is in order before first deletion
        self.assertEqual(refactor.tweets[0], 0)
        self.assertEqual(refactor.tweets, [0, 1, 2, 3, 4])

        #Calls delete_tweet() without any other function calls before
        #So it should delete the first tweet(first element of tweets[])
        #because refactor.current_tweet=1 by default
        refactor.delete_tweet()
        self.assertEqual(refactor.tweets[0], 1)
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES-1)
        self.assertEqual(refactor.tweets, [1, 2, 3, 4])
        self.assertEqual(refactor.current_tweet, 1)

        #Current tweet is changed to number of the last tweet
        #Last tweet is in line NUM_OF_LINES - 1 because of the previous deletion
        #Check if last tweet is deleted properly
        refactor.current_tweet = NUM_OF_LINES - 1
        refactor.delete_tweet()
        self.assertEqual(refactor.tweets[0], 1)
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES-2)
        self.assertEqual(refactor.tweets, [1, 2, 3])
        self.assertEqual(refactor.current_tweet, NUM_OF_LINES-1)

        #Check if delete_tweet() deletes the last tweet if
        #current_tweet > len(tweets)
        #(current_tweet remains unchanged after a deletion)
        refactor.delete_tweet()
        self.assertEqual(refactor.tweets[0], 1)
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES-3)
        self.assertEqual(refactor.tweets, [1, 2])
        
        #Check if delete_tweet() deletes the tweet that was
        #just readen, if called after read_tweet()
        refactor.read_tweet(1)
        refactor.delete_tweet()
        self.assertEqual(refactor.tweets[0], 2)
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES-4)
        self.assertEqual(refactor.tweets, [2])


    #Calls read_last_tweet() in different cases and checks
    #if the last tweet was indeed readen by capturing console output
    @patch('refactor.input', return_value='created tweet')
    def test_read_last_tweet(self, input):
        print("\n\n\n" + "  READ LAST TWEET TEST" + "\n\n\n")

        #Check the function before changes
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_last_tweet()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm the 5th and final tweet")

        #Check function after tweets where created
        #Created tweets' text is "created tweet"
        refactor.create_tweet()
        refactor.create_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_last_tweet()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+2)

        #Check function after last tweet's text was update to "created tweet"
        refactor.update_tweet(7)
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_last_tweet()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+2)

        #Check function after deletions
        refactor.delete_tweet()
        refactor.delete_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_last_tweet()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm the 5th and final tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)

    #Calls read_one_up() in different cases and checks
    #if the correct tweet was indeed readen by capturing console output
    @patch('refactor.input', return_value='updated or created tweet')
    def test_read_one_up(self, input):
        print("\n\n\n" + "READ ONE UP TEST" + "\n\n\n")

        #Calling read_one_up() without any previous function calls
        #should read the 2nd tweet beacause current_tweet=1 by default
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_up()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm the 2nd tweet")

        #Update of a tweet for later stages
        refactor.update_tweet(4)

        #Check function after current_tweet was changed
        refactor.current_tweet = 2
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_up()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm tweet #3")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)

        #Check function when it is called twice in a row
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_up()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated or created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)

        #Check function after tweets creation
        #also checks function's Error message
        refactor.create_tweet()
        refactor.create_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_up()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        self.assertEqual(s, "Current tweet is the last one in the file. Can't read one up!" + "\n")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+2)

        #Check function after tweet deletion
        refactor.current_tweet = 5
        refactor.delete_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_up()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated or created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+1)

    #Calls read_one_down() in different cases and checks
    #if the correct tweet was indeed readen by capturing console output
    @patch('refactor.input', return_value='updated or created tweet')
    def test_read_one_down(self, input):
        print("\n\n\n" + "READ ONE DOWN TEST" + "\n\n\n")

        #Check fuction with no changes
        #Should get function FAIL message because current_tweet=1 
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_down()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        self.assertEqual(s, "current_tweet is 1 (the 1st one). Can't read tweet #0!\nQuitting...\n")

        #Check function after a tweet update(current_tweet change)
        refactor.update_tweet(2)
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_down()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: I'm the first tweet about Obama")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES)
        
        #Check function after tweets creation
        refactor.create_tweet()
        refactor.create_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_down()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated or created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+2)

        #Check functions after tweet deletion
        refactor.current_tweet = 3
        refactor.delete_tweet()
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_one_down()
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated or created tweet")
        self.assertEqual(len(refactor.tweets), NUM_OF_LINES+1)

    #Checks if quit_without_save() doesn't change the file after a bunch of changes
    @patch('refactor.input', return_value='updated or created tweet')
    def test_quit_without_save(self, input):
        print("\n\n\n" + "QUIT WITHOUT SAVE TEST" + "\n\n\n")

        #bunch of changes
        refactor.create_tweet()
        refactor.create_tweet()
        refactor.update_tweet(5)
        refactor.current_tweet = 2
        refactor.delete_tweet()
        refactor.delete_tweet()
        refactor.delete_tweet()

        with self.assertRaises(SystemExit):
            refactor.quit_without_save()
        with open(refactor.JSON_PATH, 'r') as f:
            new_lines = sum(1 for line in f)
        self.assertEqual(new_lines, NUM_OF_LINES)
    
    #Checks if write_to_file() updates the file after a bunch of changes
    @patch('refactor.input', return_value='updated or created tweet')
    def test_write_to_file(self, input):
        print("\n\n\n" + "WRITE TO FILE TEST" + "\n\n\n")

        #bunch of changes
        refactor.create_tweet()
        refactor.create_tweet()
        refactor.update_tweet(1)
        refactor.current_tweet = 5
        refactor.delete_tweet()
        refactor.delete_tweet()
        refactor.delete_tweet()

        #Check tha file is unchanged before calling write_to_file()
        with open(refactor.JSON_PATH, 'r') as f:
            new_lines = sum(1 for line in f)
        self.assertEqual(new_lines, NUM_OF_LINES)

        #Check if file is correctly updated
        refactor.write_to_file()
        with open(refactor.JSON_PATH, 'r') as f:
            new_lines = sum(1 for line in f)
            new_tweets = [i for i in range(new_lines)]
        self.assertEqual(new_lines, NUM_OF_LINES-1)
        self.assertEqual(new_tweets, [0, 1, 2, 3])

        #Check if read_tweet() reads updated tweet after write_to_file() call
        capturedOutput = io.StringIO()                  
        sys.stdout = capturedOutput
        refactor.read_tweet(1)
        sys.stdout = sys.__stdout__ 
        s = capturedOutput.getvalue()
        s = s.splitlines()[1]
        self.assertEqual(s, "Text: updated or created tweet")
        

# to be able to run the code under the unittest module we have to add the following
if __name__ == '__main__':
    unittest.main()