from selenium.webdriver.common.by import By
from .blueprints import LinkedinBotBlueprint
from ..constants.locations import LinkedinLocations
from ..utility.utils import extract_data, scroll_bottom_element, save_postings_to_csv
from time import sleep


# This class is for the scrapper bot
# This bot is responsible for scraping the internship postings from the linkedin website
class LinkedinScrapperBot(LinkedinBotBlueprint):

    # override the init method to add the query, location and number of postings to scrap, and whether to look for internships or jobs
    # as well as the output path to a csv file and the wait time
    # If the number of postings is not specified, then the bot will scrap all the postings it can find
    def __init__(self, query, location, internship=True, number_of_postings=None, output_path="./data/output.csv", wait_time=10):
        super().__init__(wait_time)

        # array to hold the postings found
        self.postings = []

        # check if the query is part of the LinkedinLocations enum
        # if it is not, raise an error and tell the user to check the locations enum
        if location not in LinkedinLocations.__members__:
            print("The query is not part of the LinkedinLocations enum. Please check the corresponding locations enum in constants/locations.py")
            exit(1)

        # set the query, location, number of postings and output path and internship
        self.query = query
        self.location = location
        self.number_of_postings = number_of_postings
        self.output_path = output_path
        self.internship = internship

    # override the run method to add the main logic of the bot
    def run(self):

        # construct the query url
        # TODO: Make it so that it only looks for internships or make that into an option
        query_join = "%20".join(self.query.split(" "))
        query_internship = 1 if self.internship else 0
        query_url = f"https://www.linkedin.com/jobs/search?keywords={query_join}&location={self.location}&sortBy=R&redirect=false&f_E={query_internship}"
        
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
            while len(self.postings) < self.number_of_postings:
            
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

                    # stop if the number of postings is equal to the number of postings we want to scrap
                    if len(self.postings) == self.number_of_postings:
                        break

                    # extract the data from the posting
                    self.postings.append(extract_data(posting))

                # check to see if the number of postings is still less than the number of postings we want to scrap
                # if it is, then we need to click the next button and repeat the process
                # if it is not, then we can break out of the loop
                if len(self.postings) < self.number_of_postings:
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
                    self.postings.append(extract_data(posting))

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
        print(f"Found {len(self.postings)} postings")

        # save the postings to a csv file
        save_postings_to_csv(self.postings, self.output_path)