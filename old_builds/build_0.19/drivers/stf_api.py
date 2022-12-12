from flask import Flask, jsonify 
from flask_restful import Resource, Api , reqparse
import pandas as pd 

# ThreatFinder API implemention

# v0.01a (09/05/22) Simple GET request to fetch reports by ID
# Usage: https://<ip-address>/reports/<report-id>

import json

app=Flask(__name__)
api=Api(app)

data_arg=reqparse.RequestParser()

class read(Resource):
    def __init__(self):
        # read csv file
        self.data = pd.read_csv('db.csv',sep=',')
        self.data.columns = self.data.columns.str.strip()
    
    def get(self,ID): # GET module
        
        data_fount=self.data.loc[self.data['ID'] == ID].to_json(orient="records",lines=True)
        print(data_fount)
        data_found = json.loads(data_fount.replace("\'", '"')) # Remove tab formatting bug

        return jsonify({'message': data_found})
  
api.add_resource(read, '/reports/<int:ID>')

if __name__ == '__main__':
    app.run(debug=True) 