# Mortar Data (Serverless)

Install with `pip install mortardata`

Set the following environment variables:

```bash
export MORTARDATA_S3_REGION=""
export MORTARDATA_S3_BUCKET=""
export MORTARDATA_QUERY_ENDPOINT=""
```

Then use as follows:


```python
from mortardata import Client

# connect client
c = Client()

vav_points = """
PREFIX brick: <https://brickschema.org/schema/Brick#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
SELECT ?equip ?point ?id WHERE {
    ?equip rdf:type/rdfs:subClassOf* brick:VAV ;
          brick:hasPoint ?point .
    ?point ref:hasExternalReference/ref:hasTimeseriesId ?id .
}"""
# get metadata for first 20 sites
df = c.sparql(vav_points, sites=c.sites[:20]) 
# most operations return dataframes
df.to_csv("vav_points.csv")

# get timeseries data into a dataframe for 2 sites, maximum of 1 million points for January 2016
df = c.data_sparql(vav_points, start="2016-01-01", end="2016-02-01", limit=1e6, sites=['urn:bldg2#','urn:bldg5#'])
print(df.head())

# similar to the above, but streams data directly into a CSV file. Can be helpful for extra large downloads
num = c.data_sparql_to_csv(vav_points, "vav_data.csv", limit=1e6, sites=['urn:bldg2#','urn:bldg5#'])
print(f"Downloaded {num} datapoints")
```
