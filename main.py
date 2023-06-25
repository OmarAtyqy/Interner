from src.bots.linkedin_bots import LinkedinScrapperBot
from time import sleep


# TODO: work on the documentation
# TODO: create the application bot
# TODO: add a function to save the data to a csv file in safe mutli-threaded way in src/utility/utils.py
# TODO: Add a way to run the bots in parallel


# ===================================== CONFIGURATION =====================================
# List of queries to search for
queries = ["data science", "ai", "artificial intelligence", "machine learning", "deep learning", "computer vision", "data analyst", "data engineer", "data scientist"]

# List of locations to search for
# Allowed locations:
#   - US 
#   - UK 
#   - FR
#   - MOROCCO
#   - RABAT
#   - CASABLANCA
locations = ["MOROCCO", "RABAT", "CASABLANCA", "FR", "UK", "US"]

# Number of postings to scrap per query and location
# If None, then all the postings will be scrapped
number_of_postings = 50

# Whether to look for internships or jobs
# If True, then it will look for internships
# If False, then it will look for jobs
internship = True

# Output path to the csv file
# By default, it is set to ./data/output.csv
output_path = "./data/output.csv"

# Wait time in seconds
# This is the time to wait in between operations to let the page load and avoid detection
# By default, it is set to 10 seconds
wait_time = 5

# wait time in between switching bots from different queries and locations
# This is the time to wait in between bots to avoid detection
wait_time_between_bots = 60


# ===================================== EXECUTION =====================================
if __name__ == "__main__":


    # list to hold all the bots
    bots = []
    
    # create the scarpping bot
    bot = LinkedinScrapperBot(
        queries=queries,
        locations=locations,
        internship=internship,
        number_of_postings=number_of_postings,
        output_path=output_path,
        wait_time=wait_time,
        wait_time_between_bots=wait_time_between_bots
    )

    # start the bot
    bot.start()