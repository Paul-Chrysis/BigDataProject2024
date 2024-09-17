from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")  

db = client["bdp-database"]
processed_data = db["processed_data"]
raw_data = db["raw_data"]

def query_least_vehicles_edge(collection, start_date, end_date):
    min_count_result = collection.aggregate([
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": "$link", "vehicleCount": {"$sum": "$vcount"}}},
        {"$group": {"_id": None, "minCount": {"$min": "$vehicleCount"}}},
    ])
    
    min_count_list = list(min_count_result)
    print(min_count_list)
    if not min_count_list:
        print("DEBUG: No results found for the timeframe.")
        return []

    min_count_value = min_count_list[0]["minCount"]

    result = collection.aggregate([
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": "$link", "vehicleCount": {"$sum": "$vcount"}}},
        {"$match": {"vehicleCount": min_count_value}}
    ])
    
    result_list = list(result)
    return result_list

def query_highest_avg_speed_edge(collection, start_date, end_date):
    max_speed_result = collection.aggregate([
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": "$link", "avgSpeed": {"$avg": "$vspeed"}}},
        {"$group": {"_id": None, "maxSpeed": {"$max": "$avgSpeed"}}},
    ])
    
    max_speed = list(max_speed_result)
    
    if not max_speed:
        print("DEBUG: No results found for the timeframe.")
        return []

    max_speed_value = max_speed[0]["maxSpeed"]

    result = collection.aggregate([
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
        {"$group": {"_id": "$link", "avgSpeed": {"$avg": "$vspeed"}}},
        {"$match": {"avgSpeed": max_speed_value}}
    ])
    
    result_list = list(result)
    return result_list


def query_longest_route(collection, start_date, end_date):
    pipeline = [
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
       
        {"$group": {
            "_id": "$name", 
            "distinctLinks": {"$addToSet": "$link"},
            "lastPosition": {"$last": "$position"}
        }},
        
        {"$project": {
            "vehicleId": "$_id",
            "totalDistance": {
                "$subtract": [
                    {"$multiply": [{"$size": "$distinctLinks"}, 500]},
                    {"$subtract": [500, "$lastPosition"]} 
                ]
            }
        }},
        
        {"$sort": {"totalDistance": -1}},
    ]
    
    total_distance_result = collection.aggregate(pipeline)
    total_distance_list = list(total_distance_result)
    
    if not total_distance_list:
        print("DEBUG: No results found for the timeframe.")
        return []
    longest_route_value = total_distance_list[0]["totalDistance"]
    
    second_pipeline = [
        {"$match": {"time": {"$gte": start_date, "$lte": end_date}}},
       
        {"$group": {
            "_id": "$name", 
            "distinctLinks": {"$addToSet": "$link"},
            "lastPosition": {"$last": "$position"}
        }},
        
        {"$project": {
            "vehicleId": "$_id",
            "totalDistance": {
                "$subtract": [
                    {"$multiply": [{"$size": "$distinctLinks"}, 500]},
                    {"$subtract": [500, "$lastPosition"]} 
                ]
            }
        }},
        
        {"$match": {"totalDistance": longest_route_value}}
    ]

    result = collection.aggregate(second_pipeline)
    result_list = list(result)
    return result_list

def get_timeframe():
    start_date_str = input("Enter start date (YYYY-MM-DD HH:MM:SS): ")
    end_date_str = input("Enter end date (YYYY-MM-DD HH:MM:SS): ")
    
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid date format. Please use 'YYYY-MM-DD HH:MM:SS'.")
        return None, None
    
    return start_date, end_date

def select_query():
    print("\nSelect a query to execute:")
    print("1. Edge with the fewest vehicles in the specified time period.")
    print("2. Edge with the highest average speed in the specified time period.")
    print("3. Vehicle/Group with the longest route in the specified time period.")
    print("4. Change the timeframe.")
    print("5. Stop the program.")
    
    query_choice = input("Enter the number of your choice (1-5): ")
    
    if query_choice not in {'1', '2', '3', '4', '5'}:
        print("Invalid choice. Please enter a number between 1 and 5.")
        return None
    
    return query_choice

def main():
    print("Welcome to the MongoDB Query Program!")
    start_date, end_date = get_timeframe()

    if not start_date or not end_date:
        print("Invalid timeframe. Exiting.")
        return

    while True:
        query_choice = select_query()
        
        if not query_choice:
            continue
        
        if query_choice == '1':
            result = query_least_vehicles_edge(processed_data, start_date, end_date)
            print("\nEdge with the fewest vehicles in the specified time period:")
            print(result)
        elif query_choice == '2':
            result = query_highest_avg_speed_edge(processed_data, start_date, end_date)
            print("\nEdge with the highest average speed in the specified time period:")
            print(result)
        elif query_choice == '3':
            result = query_longest_route(raw_data, start_date, end_date)
            print("\nVehicle/Group with the longest route in the specified time period:")
            print(result)
        elif query_choice == '4':
            start_date, end_date = get_timeframe()
            if not start_date or not end_date:
                print("Invalid timeframe.")
                break
            else:
                print("Timeframe updated successfully.")
        elif query_choice == '5':
            print("Stopping the program. Goodbye!")
            break

if __name__ == "__main__":
    main()