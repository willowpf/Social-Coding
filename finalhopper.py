import requests
import urllib.parse
from logger import setup_logger  
from config import GRAPH_HOPPER_API_KEY



logger = setup_logger("GraphhopperApp")
#UNTERMENSCH
#JARCEL FRANZ M. TUBIGON, JOHN PAUL SANORIA, JHON AXELL SENAGAN, IVAN CUYOS


geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = GRAPH_HOPPER_API_KEY


def geocoding(location, key):
    try:
        while location == "":
            location = input("Enter the location again: ")
            logger.warning("Empty location provided, prompting user again")

        url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
        logger.debug(f"Geocoding API URL: {url}")

        replydata = requests.get(url)
        json_status = replydata.status_code
        logger.debug(f"Geocoding API response status: {json_status}")

        if json_status == 200:
            json_data = replydata.json()
            logger.debug("Geocoding API response received")

            if len(json_data["hits"]) != 0:
                lat = json_data["hits"][0]["point"]["lat"]
                lng = json_data["hits"][0]["point"]["lng"]
                name = json_data["hits"][0]["name"]
                value = json_data["hits"][0]["osm_value"]

                country = json_data["hits"][0].get("country", "")
                state = json_data["hits"][0].get("state", "")

                if state and country:
                    new_loc = f"{name}, {state}, {country}"
                elif state:
                    new_loc = f"{name}, {state}"
                else:
                    new_loc = name

                location_type = f"(Location Type: {value})" if value else ""
                logger.info(f"Geocoding successful for {new_loc} {location_type}")

                return json_status, lat, lng, new_loc
            else:
                logger.warning(f"No results found for location: {location}")
                return json_status, None, None, None
        else:
            logger.error(f"Geocoding API error, status code: {json_status}")
            return json_status, None, None, None
            
    except Exception as e:
        logger.error(f"Geocoding failed: {str(e)}", exc_info=True)
        return 500, None, None, None

while True:
    logger.info("Starting new route planning session")
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehicle profiles available on Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car, bike, foot")
    print("+++++++++++++++++++++++++++++++++++++++++++++")

    profile = ["car", "bike", "foot"]
    vehicle = input("Enter a vehicle profile from the list above: ")
    
    if vehicle.lower() in ["quit", "q"]:
        logger.info("User exited program")
        break
    elif vehicle not in profile:
        logger.warning(f"Invalid vehicle profile entered: {vehicle}, defaulting to car")
        print("No valid vehicle profile was entered. Using the car profile.")
        vehicle = "car"

    loc1 = input("Starting Location: ")
    if loc1.lower() in ["quit", "q"]:
        logger.info("User exited program")
        break

    status1, lat1, lng1, new_loc1 = geocoding(loc1, key)

    loc2 = input("Destination: ")
    if loc2.lower() in ["quit", "q"]:
        logger.info("User exited program")
        break

    status2, lat2, lng2, new_loc2 = geocoding(loc2, key)

    if status1 == 200 and status2 == 200:
        op = f"&point={lat1}%2C{lng1}"
        dp = f"&point={lat2}%2C{lng2}"
        paths_url = f"{route_url}{urllib.parse.urlencode({'key': key, 'vehicle': vehicle})}{op}{dp}"
        logger.debug(f"Routing API URL: {paths_url}")
        
        try:
            paths_response = requests.get(paths_url)
            paths_status = paths_response.status_code
            logger.debug(f"Routing API response status: {paths_status}")
            paths_data = paths_response.json()

            print("=================================================")
            print("Routing API Status:", paths_status)
            print("Routing API URL:")
            print(paths_url)
            print("=================================================")
            print(f"Directions from {new_loc1} to {new_loc2}")
            print("=================================================")

            if paths_status == 200 and "paths" in paths_data:
                distance_m = paths_data["paths"][0]["distance"]
                time_ms = paths_data["paths"][0]["time"]
                miles = distance_m / 1000 / 1.61
                km = distance_m / 1000
                sec = int(time_ms / 1000 % 60)
                min = int(time_ms / 1000 / 60 % 60)
                hr = int(time_ms / 1000 / 60 / 60)

                logger.info(f"Route calculated - Distance: {distance_m:.2f}m, Duration: {hr:02d}:{min:02d}:{sec:02d}")

                print(f"Distance Traveled: {distance_m:.2f} m")
                print(f"Trip Duration: {time_ms} millisec")
                print(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")
                print("=================================================")

                for each in range(len(paths_data["paths"][0]["instructions"])):
                    path = paths_data["paths"][0]["instructions"][each]["text"]
                    distance = paths_data["paths"][0]["instructions"][each]["distance"]
                    print(f"{path} ( {distance/1000:.1f} km / {distance/1000/1.61:.1f} miles )")
                    print("=================================================")

            else:
                error_msg = paths_data.get("message", "Unknown error occurred")
                logger.error(f"Routing error: {error_msg}")
                print("Error message:", error_msg)
                print("*************************************************")

        except Exception as e:
            logger.error(f"Routing API request failed: {str(e)}", exc_info=True)
            print(f"An error occurred: {str(e)}")

    again = input("Do you want to look up another location? (yes/no): ")
    if again.lower() != "yes":
        logger.info("User chose to end session")
        break