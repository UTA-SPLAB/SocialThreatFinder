# import module

def country_city(lat,longi):

	from geopy.geocoders import Nominatim
	  
	# initialize Nominatim API
	geolocator = Nominatim(user_agent="geoapiExercises")
	  
	  
	# Latitude & Longitude input
	Latitude = str(lat)
	Longitude = str(longi)
	  
	location = geolocator.reverse(Latitude+","+Longitude)
	  
	address = location.raw['address']
	  
	# traverse the data
	city = address.get('city', '')
	country = address.get('country', '')
	state = address.get('state', '')

	if city=="":
		return_string=str(state)+", "+str(country)
	else:
		return_string=str(city)+", "+str(country)
	return return_string
