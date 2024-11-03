import datetime as dt
import requests
from bs4 import BeautifulSoup
from backend.utils.logging_utils import *


def market_holidays(url):
    # Send a GET request to the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section containing holiday calendar data
        holiday_section = soup.find('section', id='holidays')

        # Extract holiday data
        if holiday_section:
            holidays = []
            rows = holiday_section.find_all('tr')
            for row in rows[1:]:  # Skip the header row
                columns = row.find_all('td')
                if columns:
                    holiday_date = columns[1].text.strip()
                    holiday_description = columns[2].text.strip()
                    holiday_date = dt.datetime.strptime(holiday_date, '%d %b %Y').date()

                    holidays.append({'date': holiday_date, 'description': holiday_description})
                else:
                    break

            return holidays
        else:
            log_info("Holiday calendar data not found on the webpage.")
    else:
        log_error("Failed to fetch webpage. Status code:", response.status_code)
