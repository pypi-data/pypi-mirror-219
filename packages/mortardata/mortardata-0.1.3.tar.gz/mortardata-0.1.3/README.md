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

c = Client()

all_points = """
PREFIX brick: <https://brickschema.org/schema/Brick#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
SELECT ?point ?type ?uuid WHERE {
    ?point rdf:type/rdfs:subClassOf* brick:Point ;
           rdf:type ?type ;
           ref:hasExternalReference [ ref:hasTimeseriesId ?uuid ] .
}"""
df = c.sparql(all_points.strip())
df.to_csv("all_points.csv")
print(df.head())

query1 = """
PREFIX brick: <https://brickschema.org/schema/Brick#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ref: <https://brickschema.org/schema/Brick/ref#>
SELECT ?sen_point ?sen ?equip ?equip_type WHERE {
    ?equip rdf:type ?equip_type .
    ?sen_point rdf:type brick:Supply_Air_Temperature_Sensor ;
               brick:isPointOf ?equip ;
               ref:hasExternalReference [ ref:hasTimeseriesId ?sen ] .
} LIMIT 10"""
df = c.sparql(query1)
df.to_csv("query1_sparql.csv")
print(df.head())

df = c.data_sparql(query1, start="2016-01-01", end="2016-02-01", limit=1e6, sites=['bldg2','bldg5'])
print(df.head())

res = c.data_sparql_to_csv(query1, "query1.csv", sites=['bldg2','bldg5'])
print(res)
```
