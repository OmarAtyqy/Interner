from selenium.webdriver.common.by import By
from .blueprints import LinkedinBotBlueprint
from ..constants.locations import LinkedinLocations
from ..utility.utils import extract_data, scroll_bottom_element, save_postings_to_csv
from time import sleep


# This class is for the scrapper bot
# This bot is responsible for scraping the internship postings from the linkedin website
class LinkedinScrapperBot(LinkedinBotBlueprint):

    # Create a bot for the linkedin scrapper
    # queries: list of queries to search for
    # locations: list of locations to search in. Check the LinkedinLocations enum in constants/locations.py for the allowed locations
    # internship: whether to look for internships or jobs
    # number_of_postings: number of postings to scrap per query and location. If None, then all the postings will be scrapped
    # output_path: output path to the csv file. By default, it is set to ./data/output.csv
    # wait_time: wait time in seconds. This is the time to wait in between operations to let the page load and avoid detection. By default, it is set to 10 seconds
    # wait_time_between_bots: wait time in between switching bots from different queries and locations. This is the time to wait in between bots to avoid detection. By default, it is set to 60 seconds
    def __init__(self, queries, locations, internship=True, number_of_postings=None, output_path="./data/output.csv", wait_time=10, wait_time_between_bots=60):
        super().__init__(wait_time)

        # total number of postings found
        self.total_number_of_postings_saved = 0

        # check if the query is part of the LinkedinLocations enum
        # if it is not, raise an error and tell the user to check the locations enum
        for location in locations:
            if location not in LinkedinLocations.__members__:
                print(f"The location {location} is not part of the LinkedinLocations enum. Please check the corresponding locations enum in constants/locations.py")
                exit(1)

        # set the queries, locations, number of postings and output path and internship
        self.queries = queries
        self.locations = locations
        self.number_of_postings = number_of_postings
        self.output_path = output_path
        self.internship = internship
        self.wait_time_between_bots = wait_time_between_bots

    # scrap Linkedin for job/internship postings for a given query and location
    # q: query to search for
    # l: location to search in
    def scrap(self, q, l):

        # list of postings found for this query and location
        postings = []

        # construct the query url
        # TODO: Make it so that it only looks for internships or make that into an option
        query_join = "%20".join(q.split(" "))
        query_internship = 1 if self.internship else 0
        query_url = f"https://www.linkedin.com/jobs/search?keywords={query_join}&location={l}&sortBy=R&redirect=false&f_E={query_internship}"
        
        # go to the query url
        self.driver.get(query_url)

        # Look for job postings
        # We're using a sleep instead of EC.presence_of_all_elements_located
        # because the page loads the job postings dynamically and not at once
        print("Waiting for job postings to load...")
        sleep(self.wait_time)

        # check if there are any postings found by looking for the "no results found" element
        try:
            self.driver.find_element(By.CLASS_NAME, "jobs-search-no-results-banner__image")
            print("No results found")
            exit(0)
        except:
            pass
        print("Job postings found!")
    
        # while we haven't reach the number of postings we want to scrap, keep looking for more
        current_page = 1
        if self.number_of_postings:
            while len(postings) < self.number_of_postings:
            
                # scroll to the bottom of the postings list to load all the postings
                print("Scrolling to the bottom of the element...")
                scroll_bottom_element(self.driver, "jobs-search-results-list")

                # wait for the postings to load
                sleep(self.wait_time)

                # get the job postings
                print("Getting job postings...")
                scrapped_postings = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
                print(f"Found {len(postings)} postings")

                # iterate over the postings and extract the data
                for posting in scrapped_postings:

                    # stop if the number of postings is equal to the number of postings we want to scrap
                    if len(postings) == self.number_of_postings:
                        break

                    # extract the data from the posting
                    postings.append(extract_data(posting))

                # check to see if the number of postings is still less than the number of postings we want to scrap
                # if it is, then we need to click the next button and repeat the process
                # if it is not, then we can break out of the loop
                if len(postings) < self.number_of_postings:
                    try:
                        print("Clicking next button...")
                        next_buttons = map(lambda x: x.find_element(By.TAG_NAME, "button"), self.driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator--number"))
                        for button in next_buttons:
                            if button.text == str(current_page + 1):
                                sleep(self.wait_time)
                                button.click()
                                current_page += 1
                                break
                        else:
                            print("No next page found")
                            break
                    except:
                        print("Page buttons not found")
                        break
        # if the number of postings is not specified, then scrap all the postings
        else:
            while True:
            
                # scroll to the bottom of the postings list to load all the postings
                print("Scrolling to the bottom of the element...")
                scroll_bottom_element(self.driver, "jobs-search-results-list")

                # wait for the postings to load
                sleep(self.wait_time)

                # get the job postings
                print("Getting job postings...")
                postings = self.driver.find_elements(By.CLASS_NAME, "job-card-container")
                print(f"Found {len(postings)} postings")

                # iterate over the postings and extract the data
                for posting in postings:

                    # extract the data from the posting
                    postings.append(extract_data(posting))

                # check to see if the number of postings is still less than the number of postings we want to scrap
                # if it is, then we need to click the next button and repeat the process
                # if it is not, then we can break out of the loop
                try:
                    print("Clicking next button...")
                    next_buttons = map(lambda x: x.find_element(By.TAG_NAME, "button"), self.driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator--number"))
                    for button in next_buttons:
                        if button.text == str(current_page + 1):
                            sleep(self.wait_time)
                            button.click()
                            current_page += 1
                            break
                    else:
                        print("No next page found")
                        break
                except:
                    print("Page buttons not found")
                    break
            
        # print the number of postings found
        print(f"Found {len(postings)} postings")

        # save the postings to a csv file
        self.total_number_of_postings_saved += save_postings_to_csv(postings, self.output_path)

    # ovveride the run method
    # this method implements the logic of the bot
    def run(self):
            
        # iterate over the queries and locations
        # Keep track of the progress
        # wait for the wait_time_between_bots in between bots to avoid detection
        # unless it is the last bot
        total_length = len(self.queries) * len(self.locations)
        for i, q in enumerate(self.queries):
            for j, l in enumerate(self.locations):
                
                print("=====================================")
                print(f"Progress: {i * len(self.locations) + j + 1}/{total_length}")
                print(f"Query: {q} | Location: {l}")

                self.scrap(q, l)
                if i != len(self.queries) - 1 or j != len(self.locations) - 1:
                    print(f"Waiting for {self.wait_time_between_bots} seconds...")
                    sleep(self.wait_time_between_bots)
        
        
        print("=====================================")
        print(f"Total number of postings added: {self.total_number_of_postings_saved}")
