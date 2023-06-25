from statistics import mean
import psycopg2
from src.swen344_db_utils import*
from src.rideshare import*

def get_all_drivers():
    drivers_data = exec_get_all("""SELECT * FROM Drivers""")
    return drivers_data

def get_all_riders():
    riders_data = exec_get_all("""SELECT * FROM Riders""")
    return riders_data

def rides_driver(*args):
    sql = """SELECT * FROM rides WHERE driver_name = %s """
    driver_data = exec_get_all(sql, args)
    return driver_data

def rides_rider(*args):
    sql = """SELECT * FROM rides WHERE rider_name[1] = %s """
    rider_data = exec_get_all(sql, args)
    return rider_data

def driver_rating(*args):
    sql = """SELECT average_rating FROM drivers WHERE name = %s"""
    rating = exec_get_one(sql, args)
    return rating

def rider_rating(*args):
    sql = """SELECT average_rating FROM riders WHERE name = %s"""
    rating = exec_get_one(sql, args)
    return rating

def rate_driver(args):
    sql = "UPDATE  drivers set average_rating = %s WHERE name = %s"
    exec_commit(sql, args)

def rate_rider(args):
    sql = "UPDATE  riders set average_rating = %s WHERE name = %s"
    exec_commit(sql, args)

def rate_ride(args):
    sql = """UPDATE rides SET rider_rating = ARRAY_APPEND(rider_rating, %s)
            WHERE id = %s"""
    exec_commit(sql, args)

def update_ride_rating(args):
    sql = """UPDATE rides SET average_rating = AVG(r) FROM UNNEST(rider_rating) AS r
            WHERE id = %s"""
def create_new_account(args):
    sql = """INSERT INTO accounts( user_name, account_type, join_date) VALUES (%s,  %s, %s)"""
    new_account = exec_commit(sql, args)

def add_new_driver(args):
    sql = """INSERT INTO drivers (id, name, average_rating, license_number, car_make, car_model, zipcode, longitude, latitude, special_instructions, location_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """
    exec_commit(sql, args)

def add_new_rider(args):
    sql = """INSERT INTO riders (id, name, credit_card_num, available, zipcode, longitude, latitude, average_rating, special_instructions, location_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    exec_commit(sql, args)

def remove_account( *args):
    sql = """UPDATE  accounts SET active=false WHERE user_name = %s"""
    exec_commit(sql, args)

def pick_up_rider(args):
    sql = """INSERT INTO rides(rider_names, rider_id, fare, start_location_id, start_time, pick_up) VALUES(%s,%s,%s,%s,%s,%s) WHERE id = %s"""
    exec_commit(sql, args)

def drop_off_rider(args):
    sql = """UPDATE rides SET end_location_id = %s, end_time = %s, drop_off = %s WHERE id = %s"""
    exec_commit(sql, args)

def get_pickup_status(args):
    sql = """SELECT pick_up FROM rides WHERE  rider_name[1] = %s AND  driver_name = %s"""
    status = exec_get_one(sql, args)
    return status

def charge_rider(args):
    sql = """INSERT INTO rider(receipt) VALUES(%s)"""
    exec_commit(sql, args)

def update_account(args):
    sql = """UPDATE  accounts SET user_name = %s WHERE user_name = %s"""
    exec_commit(sql, args)

def add_new_ride(args):
    sql = """INSERT INTO rides(id, driver_name, rider_name,  driver_id, rider_id, longitude, latitude, start_time) VALUES(%s,%s,%s,%s,%s,%s,%s, %s)"""
    new_ride = exec_commit(sql, args)
    return new_ride

def generate_receipt(args):
    sql = """SELECT rides.id, riders.name, SUM(rides.fare) AS total_spending FROM riders
            INNER JOIN rides 
            ON riders.name = %s AND  %s = ANY(rides.rider_name)
            WHERE drop_off = True  And (rides.start_time BETWEEN %s AND %s )
            GROUP BY rides.id , riders.name
            ORDER BY rides.id ASC """
    receipt = exec_get_all(sql, args)
    return receipt

def split_fare(args):
    sql = """UPDATE rides 
            SET fare = fare / ARRAY_LENGTH(rider_id, 1) 
            WHERE id = %s"""
    exec_commit(sql, args)

def get_fare(*args):
    sql = """SELECT fare FROM rides WHERE %s = ANY(rider_name)"""
    fare = exec_get_all(sql, args)
    return fare

def accept_ride(*args):
    sql = """UPDATE rides SET accepted = True WHERE rider_name[1] = %s"""
    exec_commit(sql,args)

def add_to_carpool(args):
    sql = """UPDATE rides SET rider_name = ARRAY_APPEND(rider_name, %s), 
            rider_id = ARRAY_APPEND(rider_id,%s) 
            WHERE driver_name = %s AND id = %s"""
    exec_commit(sql, args)

def add_fare(args):
    sql = """UPDATE rides SET fare = %s 
            WHERE driver_name = %s AND %s = ANY(rides.rider_name)"""
    exec_commit(sql, args)

def set_availability( args):
    sql = """UPDATE riders SET available = %s WHERE id = %s """
    availability = exec_commit(sql, args)
    return availability

def view_all_available_riders( args):
    sql = """SELECT * FROM riders WHERE available = true"""
    availability = exec_get_all(sql, args)
    return availability

def view_rider_availability( args):
    sql = """SELECT * FROM riders WHERE available = true AND name = %s"""
    availability = exec_get_all(sql, args)
    return availability

def view_driver_availability( args):
    sql = """SELECT * FROM drivers WHERE available = true"""
    availability = exec_get_all(sql, args)
    return availability

def view_drivers_by_zipcode(*args):
    sql = """SELECT * FROM drivers where zipcode = %s"""
    all_drivers = exec_get_all(sql, args)
    return all_drivers

def view_ride(args):
    sql = """SELECT * FROM rides WHERE %s = ANY(rides.rider_name) AND driver_name = %s"""
    ride = exec_get_all(sql,args)
    return ride

def update_location( *args):
    sql = """UPDATE location """
    location = exec_commit(sql, args)
    return location

def view_profile(*args):
    sql = """SELECT * FROM accounts WHERE user_name = %s"""    
    profile = exec_get_all(sql, args)
    return profile


def view_all_accounts():
    sql = """SELECT * FROM accounts"""
    accounts = exec_get_all(sql)
    return accounts

def update_driver_availability(args):
    sql = """UPDATE drivers SET available = %s WHERE name = %s"""
    exec_commit(sql, args)

def get_full_ride_info(*args):
    sql = """SELECT driver_name, latitude, longitude, rider_name, average_rating
            FROM rides
            WHERE start_time >= %s::DATE - INTERVAL '24 HOURS' """
    result = exec_get_all(sql, args)
    return result

def get_fare_times():
    sql = """SELECT EXTRACT(HOUR FROM rides.start_time), AVG(fare) 
            FROM rides
            GROUP BY start_time"""
    times = exec_get_all(sql)
    return times