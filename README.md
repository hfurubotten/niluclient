# niluclient
Python client for getting air pollution data from NILU sensor stations in Norway.
The package comes with clients that can fetch and cache data from nilus api. 

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]


## Acknowledgements
According to the [api documentation][api-nilu-no] from nilu.no and luftkvalitet.info, 
when using data fetched through this client an acknowledgement to both 
nilu.no and luftkvalitet.info needs to be included. 

## Usage

Finding all station in an area:
```python
import niluclient as nilu

stations = nilu.lookup_stations_in_area('Bergen')
```

Finding all stations and sensor reading within 20 km from a location:
```python
import niluclient as nilu

client = nilu.create_location_client(60.123456, 5.123456)

# name of all stations found.
station_names = client.station_names

# dict of all stations with readings.
stations = client.station_data

# all stations NO2 readings
for station in stations:
    no2_value = station.sensors['NO2'].value

```

Finding readings from a specified station, and update cached value:
````python
import niluclient as nilu

client = nilu.create_station_client('Kannik')
no2_value = client.data.sensors['NO2'].value
no2_unit = client.data.sensors['NO2'].value

# after an hour. Data from the api will only update on the hour. 
client.update()

new_no2_value = client.data.sensors['NO2'].value

````

## Client api coverage

**Air quality index:**
Fetch measured value and index.
- [x] GET /aq/utd (Implemented for station filtering) - `niluclient.NiluStationClient`
- [x] GET /aq/utd/{latitude}/{longitude}/{radius} - `niluclient.NiluLocationClient`
- [ ] GET /aq/historical/{fromtime}/{totime}/{station}
- [ ] GET /aq/historical/{fromtime}/{totime}/{latitude}/{longitude}/{radius}

**Observations:** 
Fetch measured value.
- [ ] GET /obs/utd
- [ ] GET /obs/utd/{latitude}/{longitude}/{radius}
- [ ] GET /obs/historical/{fromtime}/{totime}/{station}
- [ ] GET /obs/historical/{fromtime}/{totime}/{latitude}/{longitude}/{radius}

**Day average**
Calculates day average for a given time period.
- [ ] GET /stats/day/{fromtime}/{totime}/{station}
- [ ] GET /stats/day/{fromtime}/{totime}/{latitude}/{longitude}/{radius}

**Lookup api:**
Lists metadata used for filtering.
- [ ] GET /lookup/areas (Partially with the `niluclient.AREAS` constants)
- [x] GET /lookup/stations - `niluclient.lookup_stations_in_area('')`
- [ ] GET /lookup/components
- [ ] GET /lookup/aqis
 
Source: endpoints and description fetched from [nilu api documentation][api-nilu-no]

[api-nilu-no]: https://api.nilu.no/docs/
[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/heine