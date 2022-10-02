import requests

BASE = "http://127.0.0.1:5000/"

data = [{"name": "Kevin", "views" : 10000, "likes": 10, "favorites": 25}, 
        {"name": "Andrea", "views" : 25000, "likes": 5000, "favorites": 200}, 
        {"name": "Alan", "views" : 500000, "likes": 36000, "favorites": 140},
        {"name": "Amy", "views" : 60000000, "likes": 25000000, "favorites": 30000}]

print("Results of delete requests:")
for i in range(len(data)):
    response = requests.delete(BASE + "video/" + str(i))
    print(response)

input()

print("Results of put requests:")
# send requests to url
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()

print("Results of patch requests")
response = requests.patch(BASE + "video/2", {"views" : 99, "likes": 2400})
print(response.json())

input()

print("Results of get requests:")
for i in range(len(data)):
    response = requests.get(BASE + "video/" + str(i))
    print(response.json())

