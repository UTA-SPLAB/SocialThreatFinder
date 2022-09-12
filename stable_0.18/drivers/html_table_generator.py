from csv import reader

def htg():
    message1="""<style>
    ..hover_img { 
      position:relative;  

    }
    .hover_img a span { 
      position:absolute;

      display:none; 
      z-index:99;
      left:50%;
      -webkit-transform: translateX(-50%);
      -ms-transform: translateX(-50%);
      transform: translateX(-50%);
    }
    .hover_img a:hover span { 
      display:block;
      border: 5px solid #555;
    }
    .styled-table {

        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }

    .styled-table thead tr {
        background-color: #EF0303;
        color: #ffffff;
        text-align: left;
    }

    .styled-table tbody tr {
        border-bottom: 1px solid #dddddd;
      
    }

    table tr td {

      border-left: 1px solid black;
      border-right: 1px solid black;
      color: black


    }

     td {
      text-align: center;
      padding:5px;
    }

     th {
      text-align: center;
      border-right: 1px solid black;
      border-left: 1px solid black;
     
    }

    table th
    {
    padding:10px;
    }

    .styled-table tbody tr:nth-of-type(even) {
        background-color: #f3f3f3;
    }

    .styled-table tbody tr:last-of-type {
        border-bottom: 2px solid #009879;
    }

    .styled-table tbody tr.active-row {
        font-weight: bold;
        color: #009879;
    }
    </style>
    <div align="center">
   <h1> <font color="black">ThreatFinder ft. Twitter Database </font> </h1></div>
    <div align="center">
    <h3> <font color="blue"> Updated every ~5 mins </h3></div>


    <table class="styled-table" border=1 frame=void rules=columns>
        <thead>
            <tr>
                <th>URL</th>
                <th>Registrar name</th>
                <th> IP Address </th>
                <th>URL status</th>
                <th>Detections</th>
                <th> Location </th>
                <th>Creation date</th>
                <th> Creation time </th>
                <th> Image URL </th>
                

            </tr>
        </thead>
        <tbody>"""

    message2=""
    with open('database/db.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        # Check file as empty
        if header != None:
            # Iterate over each row after the header in the csv
            for row in csv_reader:

                row[2]=row[2][0:44] 

                if(int(row[5])==1): # Changing URL status for display in the database.
                    row[5]='Online'
                elif(int(row[5])==0):
                    row[5]='Inactive'
                elif(int(row[5])==999):
                    row[5]='Unknown'

                row[7] = str(row[7])[:20] # Truncate the geo location co-ordinate


                if(row[11])=="":
                    image_text="Not available"
                else:
                    image_text="<div class='hover_img'><a href='#'>See image<span><img src="+"'"+str(row[11])+"'"+"/></span> </a></div>"
                    image_text="<a href="+str(row[11])+" target='_blank'>See image</a>"


                temp_string="<tr><td>"+str(row[2])+"</td><td>"+str(row[3])+"</td><td>"+str(row[4])+"</td><td>"+str(row[5])+"</td><td>"+str(row[6])+"</td><td>"+str(row[8])+"</td><td>"+str(row[9])+"</td><td>"+str(row[10])+"</td><td>"+image_text+"</td></tr>"

                message2=message2+temp_string


    message3="""
         
        </tbody>
    </table> """



    html_message=message1+message2+message3
    file=open("templates/database.html","w")
    file.write(html_message)
    file.close()

