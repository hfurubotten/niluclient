"""
Client for checking the air quality around Norway.

Data delivered by luftkvalitet.info and nilu.no. 
"""
import logging
import requests

_LOGGER = logging.getLogger(__name__)

POLLUTION_INDEX = [
    "No data",
    'Low',
    'Moderate',
    'High',
    "Extreamly high"
]

AREAS = [
    'Ålesund',
    'Zeppelinfjellet',
    'Tustervatn',
    'Trondheim',
    'Tromsø',
    'Sør-Varanger',
    'Stavanger',
    'Sarpsborg',
    'Sandve',
    'Prestebakke',
    'Oslo',
    'Narvik',
    'Moss',
    'Mo i Rana',
    'Lørenskog',
    'Lillestrøm',
    'Lillesand',
    'Lillehammer',
    'Kårvatn',
    'Kristiansand',
    'Karasjok',
    'Hurdal',
    'Harstad',
    'Hamar',
    'Halden',
    'Grenland',
    'Gjøvik',
    'Fredrikstad',
    'Elverum',
    'Drammen',
    'Bærum',
    'Brumunddal',
    'Bodø',
    'Birkenes',
    'Bergen'
]

LOCATION_URL_FORMAT = 'https://api.nilu.no/aq/utd/{0}/{1}/20?method=within'
STATION_URL_FORMAT = 'https://api.nilu.no/aq/utd?stations={0}'
AREA_URL_FORMAT = 'https://api.nilu.no/aq/utd?areas={0}'


class SensorDto:
    """Data about a sensor/data point."""

    def __init__(self, data: dict):
        """Initialize a data object for a sensor."""
        self._data = data

    @property
    def station_id(self) -> str:
        """Station id the sensor belongs to."""
        return self._data['eoi']

    @property
    def value(self) -> float:
        """Measured value."""
        return float(self._data['value'])
    
    @property
    def unit_of_measurement(self) -> str:
        """Unit the sensor is measuring in."""
        return self._data['unit']

    @property
    def component(self) -> str:
        """Pollution component measured in sensor."""
        return self._data['component']

    @property
    def pollution_index(self) -> int:
        """Pollution index."""
        return int(self._data['index'])

    def update(self, data: dict) -> None:
        """Update sensor data with a data dict from api."""
        self._data = data


class StationDto:
    """Data about a station."""

    def __init__(self, data: dict = None):
        self.sensors = {}
        self._station_id = None
        self._station_name = None
        self._area = None
        if data:
            self.update(data)

    @property
    def station_id(self) -> str:
        """Id from of the station."""
        return self._station_id

    @property
    def name(self) -> str:
        """Station name."""
        return self._station_name

    @property
    def area(self) -> str:
        """Area which the station is place within."""
        return self._area

    def reset(self) -> None:
        """Reset cached data."""
        self.sensors = {}

    def update(self, data: dict) -> None:
        """Update the data within the station with dict data from api."""
        self._station_id = data['eoi']
        self._station_name = data['station']
        self._area = data['area']
        comp = data['component']
        if comp not in self.sensors:
            self.sensors[comp] = SensorDto(data)
        else:
            self.sensors[comp].update(data)


class NiluStationClient:
    """Get latest air quality from a station."""

    def __init__(self, station_name: str):
        self._station_name = station_name
        self._station = StationDto()

    @property
    def data(self) -> StationDto:
        """Data from the station."""
        return self._station

    def update(self) -> None:
        """Update cached data from the station."""
        url = STATION_URL_FORMAT.format(self._station_name)
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            _LOGGER.warning("Invalid response from NILU API")
            return

        data = response.json()
        for sensor in data:
            self._station.update(sensor)

        
class NiluLocationClient:
    """Get the latest air quality reading from Nilu API."""

    def __init__(self, latitude: float, longitude: float):
        self._latitude = latitude
        self._longitude = longitude
        self._sites = {}

    @property
    def station_data(self) -> dict:
        """Data from stations withing range."""
        return self._sites

    @property
    def station_names(self) -> list:
        """List station names within range."""
        return [k for k in self._sites]

    def update(self) -> None:
        """Update cached data in all stations."""
        url = LOCATION_URL_FORMAT.format(self._latitude, self._longitude)
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            _LOGGER.warning("Invalid response from NILU API")
            return

        data = response.json()
        for site in data:
            site_id = site['station']
            if site_id not in self._sites:
                self._sites[site_id] = StationDto(site)
            else:
                self._sites[site_id].update(site)


def create_station_client(station_name: str) -> NiluStationClient:
    """Create a client for sensor readings from one specific station."""
    client = NiluStationClient(station_name)
    client.update()
    return client


def create_location_client(
        latitude: float, longitude: float) -> NiluLocationClient:
    """Create a client for sensor readings from stations within 20 km."""
    client = NiluLocationClient(latitude, longitude)
    client.update()
    return client


def lookup_stations_in_area(area: str) -> list:
    """Lookup all stations in an area."""
    url = AREA_URL_FORMAT.format(area)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        _LOGGER.warning("Invalid response from NILU API")
        return []

    data = response.json()
    return list(set([s['station'] for s in data]))
