from src.bots.linkedin_bots import LinkedinScrapperBot
from src.constants.locations import LinkedinLocations
from time import sleep

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

# wait time in between bots
# This is the time to wait in between bots to avoid detection
wait_time_between_bots = 60



# ===================================== EXECUTION =====================================
if __name__ == "__main__":


    # list to hold all the bots
    bots = []
    
    # create a bot for each query and location
    for query in queries:
        for location in locations:
            bot = LinkedinScrapperBot(
                query=query,
                location=location,
                internship=internship,
                number_of_postings=number_of_postings,
                output_path=output_path,
                wait_time=wait_time
            )
            bots.append(bot)
    
    # run each bot sequentially
    progress_counter = 0
    for bot in bots:
        print("=====================================")
        print(f"Progress: {progress_counter}/{len(bots)}")
        print(f"Running bot for query: {bot.query} and location: {bot.location}")
        bot.start()
        progress_counter += 1

        # wait in between bots to avoid detection
        sleep(wait_time)