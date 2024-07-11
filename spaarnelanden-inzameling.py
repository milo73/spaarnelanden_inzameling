import logging
from datetime import datetime, timedelta
import json
import re
import time
from gazpacho import Soup
import requests
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
CONTAINER_NUMBER = os.getenv('CONTAINER_NUMBER', '')
SOURCE_URL = 'https://inzameling.spaarnelanden.nl/'
SEARCH_TAG = 'script'
SEARCH_PATTERN = 'var oContainerModel =(.*])'
TIME_BETWEEN_UPDATES = timedelta(minutes=int(os.getenv('UPDATE_INTERVAL', '10')))
SENSOR_NAME = f'Spaarnelanden Inzameling (Container {CONTAINER_NUMBER})'

TRASH_TYPES = {
    'Papier': ['Papier', 'Paper'],
    'Pbd': ['Plastic, Blik en Drinkpakken', 'Plastic, Cans and Drink cartons'],
    'Rest': ['Restafval', 'Residual waste'],
    'Textiel': ['Textiel', 'Textile'],
    'Glas': ['Glas', 'Glass'],
    None: ['None', 'None']
}

FILLING_DEGREE_STATUSES = {
    1: 'Niet ingepland vandaag',
    2: 'Onbekend (2)',
    3: 'Ingepland'
}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class ContainerData:
    filling_degree_status: str
    filling_degree: float
    latitude: float
    longitude: float
    registration_number: str
    is_out_of_use: bool
    is_skipped: bool
    is_emptied_today: bool
    date_last_emptied: datetime
    container_product_id: int
    product_name: str
    container_kind_name: str
    datetime_last_check: datetime

class ContainerDataFetcher:
    def __init__(self):
        self.last_fetch_time = None
        self.cache = None
        self.cache_duration = timedelta(minutes=5)

    def get_containerdata(self) -> Optional[ContainerData]:
        current_time = datetime.now()
        if self.last_fetch_time is None or (current_time - self.last_fetch_time) > self.cache_duration:
            try:
                logger.info('Fetching new data')
                response = requests.get(SOURCE_URL, timeout=10)
                response.raise_for_status()
                soup = Soup(response.text)
                containers_json_decoded = json.loads(re.search(SEARCH_PATTERN, soup.find(SEARCH_TAG)[10].text).group(1))

                for container in containers_json_decoded:
                    if container['sRegistrationNumber'] == CONTAINER_NUMBER:
                        self.cache = ContainerData(
                            filling_degree_status=FILLING_DEGREE_STATUSES.get(container['iFillingDegreeStatus'], 'Unknown'),
                            filling_degree=container['dFillingDegree'],
                            latitude=container['dLatitude'],
                            longitude=container['dLongitude'],
                            registration_number=container['sRegistrationNumber'],
                            is_out_of_use=container['bIsOutOfUse'],
                            is_skipped=container['bIsSkipped'],
                            is_emptied_today=container['bIsEmptiedToday'],
                            date_last_emptied=datetime.strptime(container['sDateLastEmptied'], '%d-%m-%Y'),
                            container_product_id=container['iContainerProductId'],
                            product_name=container['sProductName'],
                            container_kind_name=container['sContainerKindName'],
                            datetime_last_check=current_time
                        )
                        self.last_fetch_time = current_time
                        return self.cache

                logger.warning(f'Container {CONTAINER_NUMBER} not found')
                return None

            except requests.RequestException as e:
                logger.error(f'Error fetching data: {str(e)}')
                return None
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                logger.error(f'Error processing data: {str(e)}')
                return None
        else:
            logger.info('Using cached data')
            return self.cache

class ContainerSensor:
    def __init__(self):
        self.data_fetcher = ContainerDataFetcher()
        self.containerdata = None

    def update(self):
        logger.info('Updating containerdata started')
        self.containerdata = self.data_fetcher.get_containerdata()
        logger.info('Updating containerdata finished')

    def print_status(self):
        if self.containerdata:
            print(f"\n{SENSOR_NAME} Status:")
            print(f"Filling Degree: {self.containerdata.filling_degree}%")
            print(f"Status: {self.containerdata.filling_degree_status}")
            print(f"Product: {TRASH_TYPES.get(self.containerdata.product_name, ['Unknown'])[0]}")
            print(f"Last Emptied: {self.containerdata.date_last_emptied}")
            print(f"Is Out of Use: {'Yes' if self.containerdata.is_out_of_use else 'No'}")
            print(f"Is Emptied Today: {'Yes' if self.containerdata.is_emptied_today else 'No'}")
            print(f"Last Check: {self.containerdata.datetime_last_check}")
        else:
            print("No data available")

def main():
    sensor = ContainerSensor()
    try:
        while True:
            sensor.update()
            sensor.print_status()
            time.sleep(TIME_BETWEEN_UPDATES.total_seconds())
    except KeyboardInterrupt:
        print("\nExiting the program. Goodbye!")

if __name__ == "__main__":
    main()