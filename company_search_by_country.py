from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["linkedin_data"]
collection = db["linkedin_d3"]

def find_by_country(country, limit=1):
    results = collection.find(
        {"Location": {"$regex": country, "$options": "i"}}
    ).limit(limit)
    return list(results)


if __name__ == "__main__":
    country = input("Enter a country: ")
    companies = find_by_country(country, limit=1)

    for doc in companies:
        print("=" * 60)
        print(doc)