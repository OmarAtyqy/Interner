from src.bots.linkedin_bots import LinkedinScrapperBot


# TODO: work on the documentation
# TODO: create the application bot
# TODO: Add a way to run the bots in parallel
# TODO: add a function to save the data to a csv file in safe mutli-threaded way in src/utility/utils.py


# ===================================== CONFIGURATION =====================================
# List of queries to search for
queries = ["data science", "ai", "artificial intelligence", "machine learning", "deep learning", "computer vision",
           "data analyst", "data engineer", "data scientist"]

# List of locations to search for
# Allowed locations:
#   - US 
#   - UK 
#   - FR
#   - MOROCCO
#   - RABAT
#   - CASABLANCA
# To add further locations, please refer to src\constants\locations.py
locations = ["MOROCCO", "RABAT", "CASABLANCA", "FR", "UK", "US"]

# Number of postings to scrap per query and location
# If None, then all the postings will be scrapped
number_of_postings = None

# Whether to look for internships or jobs
# If True, then it will look for internships
# If False, then it will look for jobs
internship = True

# csv file name (MAKE SURE TO ADD THE .csv EXTENSION)
# By default, it is set to output.csv
# The file will be saved in the data folder
file_name = "output.csv"

# Wait time in seconds
# This is the time to wait in between operations to let the page load and avoid detection
# By default, it is set to 10 seconds
wait_time = 1

# wait time in between switching from different queries and locations
# This is the time to wait in between queries avoid detection
wait_time_between_queries = 5


# ===================================== EXECUTION =====================================
if __name__ == "__main__":
    
    # create the scarpping bot
    bot = LinkedinScrapperBot(
        queries=queries,
        locations=locations,
        internship=internship,
        number_of_postings=number_of_postings,
        file_name=file_name,
        wait_time=wait_time,
        wait_time_between_queries=wait_time_between_queries
    )

    # start the bot
    bot.start()