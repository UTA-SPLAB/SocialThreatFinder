
def create_frontend(news_list):
  list_item_message=""
  for i in news_list:
    list_item_message=list_item_message+"\n<option><h3>"+str(i)+"</h3></option>"
    



  f = open('templates/dash.html','w')

  message="""

       <!DOCTYPE html>    
      <html>    
      <title>  
      Example of List Box  
      </title>  
      <body>    
   
   
  <div style = "position:relative; left:80px; top:5px;">
     <h3> Twitter News Feed </h3>
  </div>

   <div align="right">

      <select id="targetField" multiple="multiple" name="D1" style="width:370px; line-height:30px; float:left; height:130px;">
                """+list_item_message+"""
  </select>

   <iframe src="map.html" align="center"height="1000" width="1500" title="Iframe Example"></iframe> 
  </div>

  </body>    
      </html>  


  """

  f.write(message)
  f.close()