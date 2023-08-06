import requests
import clappform
import clappform.dataclasses as cldc
import pandas as pd

class Itsperfect:
    id=None

    def __init__(self, url, token, version = "v2"):
        self.url = url
        self.token = token
        self.version = version

    def setFullUrl(self, category):
        url = f"https://{self.url}/api/{self.version}/{category}/&token={self.token}"
        return url
    
    def getAllPicks(self):
        fullUrl = self.setFullUrl("picks")
        r = requests.get(fullUrl)
        return r.json()
    
    def getOnePick(self, id : int ): 
        fullUrl = f"https://{self.url}/api/v2/picks/{id}/&token={self.token}"
        r = requests.get(fullUrl)
        return r.json()

    def storePicks(self, clp):
        defaultApp = clp.get(cldc.App(id="import_database", extended=True))
        flightCollection = clp.get(cldc.Collection(
            app=defaultApp,
            slug="picks"
        ))

        try:
            df = pd.DataFrame(self.getOnePick(1321)['picks'])
            clp.empty_dataframe(flightCollection)
            clp.write_dataframe(df, flightCollection, size=100)
            print("yes")
        except clappform.exceptions.HTTPError as exc:
            print(exc.response.text)

    def readPicks(self, clp):
        pipeline = {
            "app": "import_database",
            "collection": "picks",

            "pipeline": [{
                "type": "raw",
                "stages": [{"$limit": 200}]
            }, {
                "type": "fix_sort"
            }],
            "limit": 500
        }

        try:
            aggregateResults = pd.DataFrame([])
            for batch in clp.aggregate_dataframe(pipeline):
                aggregateResults = pd.concat(
                    [aggregateResults, batch], ignore_index=True, sort=False)
        except clappform.exceptions.HTTPError as exc:
            print(exc.response.text)
            print(exc.request.body)

        return aggregateResults


        
