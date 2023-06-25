from selenium.webdriver.common.by import By
from time import sleep


# function to extract the data from a job posting
# the job posting is a li element with the class name "jobs-search-results__list-item"
def extract_data(job_posting):

    # initialize the data to be extracted, so that if it's not found, it will be None or False
    job_title = None
    job_link = None
    company_name = None
    time_posted = None
    location = None
    actively_recruiting = False
    easy_apply = False
    
    # try to get the job title and link from the a tag with the class name "job-card-list__title"
    try:
        job_title = job_posting.find_element(By.CLASS_NAME, "job-card-list__title").text
        job_link = job_posting.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")
    except:
        pass

    # try and get the company name from the span tag with the class name "job-card-container__primary-description"
    try:
        company_name = job_posting.find_element(By.CLASS_NAME, "job-card-container__primary-description").text
    except:
        pass

    # try to get the time it was posted from the time tag
    try:
        time_posted = job_posting.find_element(By.TAG_NAME, "time").text
    except:
        pass

    # try and get the location from the span tag with the class name "job-card-container__metadata-item"
    try:
        location = job_posting.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
    except:
        pass

    # see if the job posting is actively recruiting
    # if it is, the div tag with the class name "job-card-container__job-insight-text" will be present
    try:
        job_posting.find_element(By.CLASS_NAME, "job-card-container__job-insight-text")
        actively_recruiting = True
    except:
        pass

    # see if the job supports easy apply
    # if it does, the span tag with the class name "job-card-container__apply-method" will be present
    try:
        job_posting.find_element(By.CLASS_NAME, "job-card-container__apply-method")
        easy_apply = True
    except:
        pass

    # return a dictionary with the data
    return {
        "job_title": job_title,
        "job_link": job_link,
        "company_name": company_name,
        "time_posted": time_posted,
        "location": location,
        "actively_recruiting": actively_recruiting,
        "easy_apply": easy_apply
    }


# function to scroll to the bottom of the given element
def scroll_bottom_element(driver, element_class_name):

    # Find the scrollable element by its class
    scrollable_element = driver.find_element(By.CLASS_NAME, element_class_name)

    # Get the height of the scrollable element
    scroll_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_element)

    # Scroll slowly to the bottom of the element
    step = 150
    scroll_top = 0
    while scroll_top <= scroll_height:
        driver.execute_script(f"arguments[0].scrollTop += {step};", scrollable_element)
        sleep(0.1)

        # check if an additional increment will go beyond the scroll height
        # if it does, scroll to the bottom of the element and break
        if scroll_top + step > scroll_height:
            driver.execute_script(f"arguments[0].scrollTop = {scroll_height};", scrollable_element)
            break
        else:
            scroll_top += step
    
    print("Finished scrolling to the bottom of the element")