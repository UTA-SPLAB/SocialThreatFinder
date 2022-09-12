# Populate from database
import folium
import time
import pandas as pd
import os
import json
import pandas as pd
from os.path import exists as file_exists

def populate_from_database(): # Function to populate the map from URLs collected before
        
    global coords_dict
    coords_dict = {}

    global url_dict
    url_dict={}

    global news_list
    news_list=[]

    global activity_dict
    activity_dict={}

    check_if_db_file_exists=file_exists('database/db.csv')
    if(check_if_db_file_exists==True):
        df=pd.read_csv("database/db.csv")


        for index, row in df.iterrows():
            tweet_id=(row['Tweet_id'])
            url=(row['URL'])
            target=(row['Target'])
            registrar_name=(row['registrar_name'])
            ip_address=(row['ip_address'])
            url_activity=(row['URL is alive'])
        
            geo=(row['Geo co-ordinates'])
            Location=(row['Location'])
            creation_date=(row['Creation_date'])
            #creation_time=(row['Creation_time'])
            image_url=(row['image_url'])
            target=(row['Target'])

            if target=='metamask' or target=='binance' or target=='trustwallet':

              target_string='Crypto scam!'
            else:
              target_string="Phishing attack!<br>"



            

            if(url_activity)==1:
                    activity_string='<font color="red">URL is active!</font>'
                    activity_dict[tweet_id]=url_activity

            elif(url_activity)==0:
                activity_string='<font color="green">URL is inactive</font>'
                activity_dict[tweet_id]=url_activity
            else:
                activity_string='Error checking URL status'
                activity_dict[tweet_id]=url_activity

            # if(detections==999): # Scanning error returned from API
            # 		detections_string='<div align="center">URL could not be scanned</div>'
            # else:
            # 	detections_string='<div align="center"><font color="blue"><strong> The URL was detected by '+str(detections)+' security tools.</strong></font></div><br>'

            time_string='<br><font color="MediumVioletRed">Discovered on:'+str(creation_date)+","+str(creation_time)+'</font><br>'

            message='<div align="center"><h4><img src="icons/phish.png" width=50 height=50><br><strong>'+target_string+'</strong><br>'+str(url)+str(time_string)+"<br><font><strong>IP Address :</strong> "+str(ip_address)+"</font><br><font><strong>Location :</strong>"+str(Location)+"</font><br><font> <strong>Registrar</strong> : "+str(registrar_name)+"</font><br><br>"+str(activity_string)+"<br></h4></div>"


            # The dictionaries to send to Leaflet

            url_dict[tweet_id]=message
            coord_value = list(eval(geo))
            coords_dict[tweet_id] = coord_value
            activity_dict[tweet_id]=url_activity

            with open('raw_output/coords_dict.txt', 'w') as file: # Writes co-ordinate info
                file.write(json.dumps(coords_dict))

            with open('raw_output/url_dict.txt', 'w') as file: # Writes URL info dict
                file.write(json.dumps(url_dict))


            with open('raw_output/activity_dict.txt', 'w') as file: # Writes URL activity dict
                file.write(json.dumps(activity_dict))
                
    build_map(coords_dict,url_dict,activity_dict)


def build_map(matrix,urllist,active): # URL list contains the message

    boulder_coords = [40.015, -105.2705]

    # Create the map
    my_map = folium.Map(location=boulder_coords, zoom_start=3)

    # Display the map
    for (k,v), (k2,v2), (k3,v3) in zip(matrix.items(), urllist.items(), active.items()):
    
        try:
        
          if v3==1: 
   
            folium.Marker(v, popup=str(v2),icon=folium.Icon(color="red")).add_to(my_map) 
          elif v3==0:

            folium.Marker(v, popup=str(v2),icon=folium.Icon(color="green")).add_to(my_map) 

          elif v3==999:
            folium.Marker(v, popup=str(v2),icon=folium.Icon(color="orange")).add_to(my_map) 

        except Exception as e: 
            print(e)
           
        #folium.Marker(v, popup=str(v4),icon=folium.Icon(color="purple")).add_to(my_map) 


    # Add markers to the map
  


# Define coordinates of where we want to center our map

    my_map.save("templates/map.html")
    #webbrowser.open("map.html")





		