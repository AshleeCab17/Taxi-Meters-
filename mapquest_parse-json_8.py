import urllib.parse
import requests 

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "ScjKx3iErPfxrgjijjqnWf2bV1X8keCG"

# Placeholder function to simulate fetching fuel price
def get_fuel_price(city):
    # In reality, you would use an actual API for fuel prices
    # Here's an example mock implementation
    mock_fuel_prices = {
        "New York": 3.50,  # in USD per gallon
        "Los Angeles": 4.10,
        "Chicago": 3.80,
        "Houston": 3.20
    }
    return mock_fuel_prices.get(city, 3.50)  # Default to $3.50/gallon if city not found

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
    elif json_status == 402: 
              print("**********************************************") 
              print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.") 
              print("**********************************************\n") 
    elif json_status == 611: 
              print("**********************************************") 
              print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.") 
              print("**********************************************\n") 
    else: 
              print("************************************************************************") 
              print("For Status Code: " + str(json_status) + "; Refer to:") 
              print("https://developer.mapquest.com/documentation/directions-api/status-codes") 
              print("************************************************************************\n")

    try:
        # User input for fuel efficiency
        km_per_l = float(input("Enter your vehicle's fuel efficiency (km/L) (default is 10 km/L): ") or 10)
        fuel_used_ltr = (miles * 1.60934) / km_per_l  # Convert miles to km and divide by km/L
        print("Estimated Fuel Used (Ltr): " + str("{:.3f}".format(fuel_used_ltr)))
        
        # Research fuel prices for the origin city
        fuel_price = get_fuel_price(orig)
        print(f"Average Fuel Price in {orig}: ${fuel_price}/gallon")

        # Convert fuel used from liters to gallons (1 liter = 0.264172 gallons)
        fuel_used_gal = fuel_used_ltr * 0.264172
        fuel_cost = fuel_used_gal * fuel_price  # Total cost of fuel for the trip
        print(f"Estimated Fuel Cost: ${fuel_cost:.2f}")
        
        print("=============================================") 
    except ValueError:
        print("Invalid input for fuel efficiency. Please provide a numeric value.")
    else:
        print(f"\nAPI Status: {json_status} = Route call failed. Please check your input and try again.")
        print("=============================================")
