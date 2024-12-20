import urllib.parse 
import requests 

main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "ScjKx3iErPfxrgjijjqnWf2bV1X8keCG"
default_km_per_l = 10  # Default fuel efficiency in km/L

while True:
    orig = input("Source City: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Destination City: ")
    if dest == "quit" or dest == "q":
        break
    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})  
    print("URL ", (url))
    json_data = requests.get(url).json() 
    json_status = json_data["info"]["statuscode"] 
    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================") 
        print("Directions from " + (orig) + " to " + (dest)) 
        print("Trip Duration:   " + (json_data["route"]["formattedTime"])) 

        # Retrieve and display miles and kilometers
        miles = json_data["route"]["distance"]
        kilometers = miles * 1.60934
        print("Kilometers:      " + str("{:.2f}".format(kilometers)))

        # Calculate and display fuel used in liters
        fuel_used_ltr = kilometers / default_km_per_l
        print("Estimated Fuel Used (Liters): " + str("{:.3f}".format(fuel_used_ltr)))

        # Display step-by-step directions
        for each in json_data["route"]["legs"][0]["maneuvers"]: 
           print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)")) 
        print("=============================================") 
    elif json_status == 402: 
        print("********************************************") 
        print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.") 
        print("**********************************************\n") 
    elif json_status == 611: 
        print("********************************************") 
        print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.") 
        print("**********************************************\n") 
    else: 
        print("**********************************************************************") 
        print("For Status Code: " + str(json_status) + "; Refer to:") 
        print("https://developer.mapquest.com/documentation/directions-api/status-codes") 
        print("************************************************************************\n")