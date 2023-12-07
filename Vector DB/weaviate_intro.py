import weaviate, json
import numpy as np
from weaviate import EmbeddedOptions
import inflect



def create_data_json(vec_len=None,no_of_dic=None):
    '''This funnctio will be used to create list of dic objects '''
    number_2_str_engine=inflect.engine()
    
    list_of_dic_obj=[]

    for i in range(1,no_of_dic+1):
        obj={
            "title":"Object " + number_2_str_engine.number_to_words(i),
            "foo":np.random.randint(500),
            "vector":np.random.rand(vec_len)
            }
        list_of_dic_obj.append(obj)

    return list_of_dic_obj

# Define some common var that r regulary used in the script 
class_name="Test"
batch_size=10
vec_len=10
no_of_dic=5

# Create random list of object that will inserted into Test class client
list_of_json=create_data_json(vec_len=vec_len,no_of_dic=no_of_dic)
print(f"\n list of jsons = {list_of_json} \n")
    

# Init the client
client = weaviate.Client(
    embedded_options=EmbeddedOptions(),timeout_config = (5, 6000)
)


# Check if the schema is already exits or not 
if client.schema.exists(class_name):
    print(f"Class : {class_name} was found start deleting it")
    client.schema.delete_class(class_name)


# Create class 
schema = {
    "class": class_name,
    "vectorizer": "none", # Default vector serch algorithm will HNSW
    "vectorIndexConfig": {
        "distance": "cosine" # Use cosine distance
    },
}
client.schema.create_class(schema)


# insert the vector empedding into  Test class  
client.batch.configure(batch_size=batch_size)  # make the insert in batches

with client.batch as batch:
  for item in list_of_json:
      properties = {
         "title": item["title"],
         "foo": item["foo"],
      }

      # the call that performs data insert
      client.batch.add_data_object(
         class_name=class_name,
         data_object=properties,
         vector=item["vector"] #  vector embeddings go here
      )


print("Number of objects inserted",
    client.query
    .aggregate(class_name)
    .with_meta_count()
    .do()
    )

# Example of searching for the nearest two vector that r nearest or similar to the query vector input
response = (
    client.query
    .get(class_name, ["title"])
    .with_near_vector({
        "vector": np.random.rand(vec_len)
    })
    .with_limit(2) # limit the output to only 2
    .with_additional(["distance", "vector, id"]) # return the distance and the vector
    .do()
)
result = response["data"]["Get"][class_name]
print("result",json.dumps(result, indent=2))



# Example of searching for the nearest two vector that r nearest or similar to the query vector input
# and also make the condtion of , foo arg is greate than number (filters)
response = (
    client.query
    .get(class_name, ["title"])
    .with_near_vector({
        "vector": np.random.rand(vec_len)
    })
    .with_limit(2) # limit the output to only 2
    .with_additional(["distance", "vector, id"]) # return the distance and the vector
    .with_where({
          "path": ["foo"],
          "operator": "GreaterThan",
          "valueNumber": 44
    })
    .do()
)
result = response["data"]["Get"][class_name]
print("result with filter",json.dumps(result, indent=2))



