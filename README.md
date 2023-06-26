# Interner

This is a Python program that scrapes job postings from LinkedIn based on a list of queries and locations and returns a csv file containing the results.

An application bot is in the works to automate the whole process!

## Installation

1. Clone this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt` in your terminal.
3. create an `.env` and populate it as so:

   ```
   LINKEDIN_EMAIL = "your_linkedin@email.com"
   LINKEDIN_PASSWORD = "your_password"
   ```

Make sure to create the `.env` file and put your credentials inside following the same convention as above. The program will remind you to add then in case any of them is missing.

## Usage

1. Open `main.py` in your favorite Python editor.
2. Modify the `queries`, `locations`, `number_of_postings`, and `internship` variables to suit your needs.
   * `queries` should be an array of strings, where each string represents a search query
   * `locations` shoud be an array of strings where each string represents a location you would like to look for all of the queries in (`Total amout of searches = number of queries x number of locations`). The locations should be defined in the `src/constants/locations.py`. More on that further down.
   * `number_of_postings` should be an integer value that represents how many offers to scrap for each query/location pair. If you want to scrap all the queries found for every pair, set it to `None`
   * `internship` is a boolean value that represents whether to scrap for internships (`true`) or job offerings (`false`)
3. Run the program by executing `python main.py` in your terminal.
4. Wait for the program to finish scraping job postings. This may take a few minutes depending on the number of postings and your internet connection.
5. The program will output a CSV file containing the scraped data. The default output path is `data/output.csv`.

### First time usage

On your first time using the program, Linkedin may give you an authentification challenge to make sure you're human. **You're only required to solve it once**, as the scrapper is built to make a dump of the browser's cookies and use them in every subsequent execution, bypassing the need to complete security challenges in the future.

Do note that in case any of your credentials are false, there is no safeguard against that and the program will continue with its execution. Pay attention the first time the browser's window is oppened and check if the login operation was successful.

### Adding a location

1. go to [Linkedin](www.linkedin.com) and search for some random **job** query (make sure it's a job query and not person, company...) **IN** **the location** that you want to add
2. press search and check the generated URL of the query, it should look something like this:
   `https://www.linkedin.com/jobs/search/currentJobId=3640386495&geoId=103644278&keywords=adfad&location=United%20States&refresh=true`
3. copy what comes after `&Location=` (in this example: `United%20States`)
4. go to `src/constants/locations`
5. add your new locations to the `LinkedinLocations` enum by giving it a key and setting its value to whatever you copied from Linkedin
6. go back to the `main.py` file and put the key of your location (as a string) into the locations array and execute the program (see Usage above)

Your `locations.py` file should look like this:

```python
# This class contains the locations to be used in a Linkedin query
class LinkedinLocations(Enum):
    #existing locations
    YOUR_LOCATION = "your%20location"
```

And your main.py file should look like this:

```python
# List of locations to search for
# Allowed locations:
#   - US 
#   - UK 
#   - FR
#   - MOROCCO
#   - RABAT
#   - CASABLANCA
# To add further locations, please refer to src\constants\locations.py
locations = ["YOUR_LOCATION", "US", "UK"]
```

## TO-DO

* [X] Create the scrapping bot
* [ ] **Create the application bot**
* [ ] Consider using multi-threading to further accelerate the search and appilcation processes (**WARNING**: could lead to account suspension if too many queries/applications are being done)

## Contributing

If you find a bug or have a feature request, please open an issue on GitHub. Pull requests are also welcome.

## License

This program is licensed under the MIT License. See the `LICENSE` file for more information.
