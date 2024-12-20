import urllib.parse 
import requests 

main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "ScjKx3iErPfxrgjijjqnWf2bV1X8keCG"
while True:
    orig = input("Source City: ")
    if orig == "quit" or orig == "q":
        break
    dest = input("Dest City: ")
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

        # Ensure miles is calculated before using
        miles = json_data["route"]["distance"]

        # Print kilometers
        print("Kilometers:      " + str("{:.2f}".format(miles * 1.60934)))
        for each in json_data["route"]["legs"][0]["maneuvers"]: 
           print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)")) 
           

        try:
            # User input for fuel efficiency
            km_per_l = float(input("Enter your vehicle's fuel efficiency (km/L) (default is 10 km/L): ") or 10)
            fuel_used_ltr = (miles * 1.60934) / km_per_l  # Convert miles to km and divide by km/L
            print("Estimated Fuel Used (Ltr): " + str("{:.3f}".format(fuel_used_ltr)))
            print("=============================================") 
        except ValueError:
            print("Invalid input for fuel efficiency. Please provide a numeric value.")
    else:
        print(f"\nAPI Status: {json_status} = Route call failed. Please check your input and try again.")
        print("=============================================") 
        
