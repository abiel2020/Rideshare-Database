import datetime
from decimal import Decimal
import unittest
from src.rideshare import *
from src.swen344_db_utils import *
from src.rideshare_api import *

class TestRideshare(unittest.TestCase):
    
    #The database is seeded with a test data set without crashing
    def test_data_seeding_drivers(self):
        #build tables
        build_db()
        
        #invoke
        populate_db()

        drivers_data = get_all_drivers()

        expected_drivers = [(1, 'Tom Magliozzi', 3.2, 145738913, 'Toyota', 'Camry', 23456, Decimal('42.523800'), Decimal('72.293400'), 'Do not drive like my brother.', 1, None), (2, 'Ray Magliozzi', 3.4, 123456789, 'Toyota', 'Rav-4', 23456, Decimal('43.773200'), Decimal('71.018400'), 'Do not drive like my brother.', 2, None),(3, 'ALEX', 0.0, 443006789, 'Honda', 'Crv', 83924, Decimal('41.700200'), Decimal('70.928400'), None, 2, None),(4, 'Bobby', 0.0, 148950089, 'Toyota', 'Prius', 14492, Decimal('41.773200'), Decimal('73.018400'), None, 2, None),(5, 'Louis', 0.0, 987456789, 'Toyota', 'Rav-4', 23456, Decimal('43.693200'), Decimal('70.918400'), None, 2, None),(6, 'Elaine', 3.4, 123456789, 'Toyota', 'Rav-4', 23456, Decimal('43.773200'), Decimal('71.018400'), None, 2, None),(7, 'Tony', 3.4, 987423081, 'Toyota', 'Rav-4', 83956, Decimal('43.773200'), Decimal('71.018400'), None, 2, None) ]

        self.assertEquals(drivers_data, expected_drivers)

    def test_data_seeding_riders(self):
        #build tables
        build_db()
        
        #invoke
        populate_db()

        riders_data = get_all_riders()
        expected_riders = [((1, 'Mike Easter', 1111222233334444, True, 12345, Decimal('42.729800'), Decimal('73.678900'), 4.3, None, 1, Decimal('0.00'), None)), ((2, 'Ray Magliozzi', None, True, 67890, Decimal('3.400000'), Decimal('43.130600'), 77.626, 'Do not drive like my brother.', 2, Decimal('0.00'), None))]
        self.assertEquals(riders_data, expected_riders)

    def test_data_seeding_rides(self):
        #build tables
        build_db()
        
        #invoke
        populate_db()
        rides_data = exec_get_all("""SELECT * FROM Rides""")
        expected_rides = [(1, 'Tom Magliozzi', ['Mike Easter'], 1, [1], Decimal('43.084800'), Decimal('77.671500'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None ), (2, 'Ray Magliozzi', ['Mike Easter'], 2, [1], Decimal('42.729800'), Decimal('73.678900'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None),(3, 'Tom Magliozzi', ['Ray Magliozzi'], 1, [2], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None)]
        self.assertEquals(rides_data, expected_rides)


    #When we list the rides that Tom gave, they include the rides to Mike and Ray
    def test_case_2(self):
        build_db()
        populate_db()

        driver = ("Tom Magliozzi")
        driver_data = rides_driver( driver)

        expected = [(1, 'Tom Magliozzi', ['Mike Easter'], 1, [1], Decimal('43.084800'), Decimal('77.671500'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False,Decimal('0.0'), None ), (3, 'Tom Magliozzi', ['Ray Magliozzi'], 1, [2], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None)]
        self.assertEquals(driver_data, expected)



    
    #When we list the rides that Mike took, they include the rides from Tom and Ray
    def test_case_3(self):
        build_db()
        populate_db()

        rider = ("Mike Easter")
        rider_data = rides_rider(rider)

        expected = [(1, 'Tom Magliozzi', ['Mike Easter'], 1, [1], Decimal('43.084800'), Decimal('77.671500'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False,Decimal('0.0'), None ), (2, 'Ray Magliozzi', ['Mike Easter'], 2, [1], Decimal('42.729800'), Decimal('73.678900'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False,Decimal('0.0'), None)]
        self.assertEquals(rider_data, expected)   
    
    #When we list the rides that Mike gave, we get no results
    def test_case_4(self):
        build_db()
        populate_db()

        driver = ("Mike Easter")
        driver_data = rides_driver( driver)

        expected = []

        self.assertEquals(driver_data, expected)

    
    
    #When Tom checks his rating, it returns the correct value
    def test_case_5(self):
        build_db()
        populate_db()

        driver = ("Tom Magliozzi")
        rating = driver_rating(driver)

        expected = (3.2,)

        self.assertEquals(rating, expected)

    def test_loading_data_from_csv(self):
        build_db()
        
        file = open("data/rideshare.csv","r")
        header = file.readline().strip()
        account_type = 1
        for line in file:
            line = line.replace("\n", "")
            values = line.split(",")
            if values[1] == "driver":
                args = (values[0], account_type ,values[2])
                create_new_account(args)
            elif values[1] == "rider":
                account_type = 2
                args = (values[0], account_type,values[2])
                create_new_account(args)
        file.close()

        accounts_data = view_all_accounts()
        expected = [(1, 'Travis Bickell', 1, True, datetime.datetime(1976, 10, 1, 0, 0)), (2, 'Alex Reger', 1, True, datetime.datetime(1979, 9, 1, 0, 0)), (3, 'Louie DePalma', 2, True, datetime.datetime(1979, 9, 3, 0, 0)), (4, 'Tony Banta', 2, True, datetime.datetime(1980, 10, 1, 0, 0)), (5, 'Jim Ignatowski', 2, True, datetime.datetime(1990, 10, 23, 0, 0)), (6, 'Latka Gravas', 2, True, datetime.datetime(1978, 7, 1, 0, 0)), (7, 'Bobby Wheeler', 2, True, datetime.datetime(2001, 11, 1, 0, 0)), (8, 'Bryan Mills', 2, True, datetime.datetime(2008, 7, 1, 0, 0)), (9, 'John McClane', 2, True, datetime.datetime(1988, 6, 1, 0, 0)), (10, 'Artie Lange', 2, True, datetime.datetime(1994, 8, 7, 0, 0)), (11, 'Ben Bailey', 2, True, datetime.datetime(1989, 3, 5, 0, 0)), (12, 'Aldred Collins', 2, True, datetime.datetime(2000, 2, 1, 0, 0)), (13, 'Mitchell Winehouse', 2, True, datetime.datetime(2011, 4, 15, 0, 0)), (14, 'Les Turner', 2, True, datetime.datetime(2003, 8, 2, 0, 0)),(15, 'Short Round', 2, True, datetime.datetime(1921, 9, 1, 0, 0)), (16, 'Henry Jones', 2, True, datetime.datetime(1920, 11, 3, 0, 0)), (17, 'Ben Hur', 2, True, datetime.datetime(2016, 5, 6, 0, 0)), (18, 'Ravi Dopinder', 2, True, datetime.datetime(2016, 6, 1, 0, 0)), (19, 'Wade Wilson', 2, True, datetime.datetime(2016, 5, 2, 0, 0)), (20, 'Korben Dallas', 2, True, datetime.datetime(2263, 5, 18, 0, 0))]
        
        self.assertEquals(expected, accounts_data)

    def test_update_profile(self):
        build_db()
        populate_db()

        first_update = ("Tom_Magliozzi_drives", "Tom Magliozzi" )
        second_update = ("Ray_Magliozzi_drives", "Ray Magliozzi")

        update_account(first_update)
        update_account(second_update)

        username1 = ("Tom_Magliozzi_drives")
        username2 = ("Ray_Magliozzi_drives")

        profile1 = view_profile(username1)
        profile2 = view_profile(username2)

        expected_one = [(1,'Tom_Magliozzi_drives', 1, True, datetime.datetime(2023, 2, 8, 0, 0))]
        expected_two = [(2, 'Ray_Magliozzi_drives', 1, True, datetime.datetime(2023, 2, 8, 0, 0))]

        self.assertEquals(expected_one, profile1)
        self.assertEquals(expected_two, profile2)

    def test_sign_up_for_accounts(self):
        build_db()
        populate_db()

        rider_data = (4,"Ms.Daisy", 1831220273934144, False, 30301, 43.1306, 0.0, 77.6260, "Drive safe", 1)
        driver_data = (8, "Hoke Colburn", 3.2, 145738913, "Toyota", "Camry", 30301, 42.5238, 72.2934, "Buckle up.", 1)

        add_new_driver(driver_data)
        add_new_rider(rider_data)

        account1 = ("Hoke Colburn", 1,  datetime.datetime(2023, 2, 8, 0, 0) )
        account2 = ("Ms.Daisy", 2, datetime.datetime(2023, 2, 8, 0, 0))

        create_new_account(account1)
        create_new_account(account2)

        data1 = view_profile(("Hoke Colburn"))
        data2 = view_profile(("Ms.Daisy"))

        expected1 = [(3, 'Hoke Colburn', 1, True, datetime.datetime(2023, 2, 8, 0, 0))]
        expected2 = [(4, 'Ms.Daisy', 2, True, datetime.datetime(2023, 2, 8, 0, 0))]

        self.assertEquals(data1, expected1)
        self.assertEquals(data2, expected2)

    def test_update_availability(self):
        build_db()
        populate_db()
        rider_data = (4,"Ms.Daisy", 1831220273934144, False, 30301, 43.1306,  77.6260, 0.0, "Drive safe", 1)
        add_new_rider(rider_data)

        input = (True, 4)
        set_availability(input)
        rider_info = ("Ms.Daisy")
        data = view_all_available_riders(rider_info)

        expected = [(1, 'Mike Easter', 1111222233334444, True, 12345, Decimal('42.729800'), Decimal('73.678900'), 4.3, None, 1, Decimal('0.00'), None), (2, 'Ray Magliozzi', None, True, 67890, Decimal('3.400000'), Decimal('43.130600'), 77.626, 'Do not drive like my brother.', 2, Decimal('0.00'), None), (4, 'Ms.Daisy', 1831220273934144, True, 30301, Decimal('43.130600'), Decimal('77.626000'), 0.0, 'Drive safe', 1, Decimal('0.00'), None)]

        self.assertEquals(data, expected)
    

    def test_view_drivers_by_zipcode(self):
        build_db()
        populate_db()
        driver_data = (8, "Hoke Colburn", 3.2, 145738913, "Toyota", "Camry", 30301, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_data)

        zipcode = (30301)
        driver_data = view_drivers_by_zipcode(zipcode)

        expected = [(8, 'Hoke Colburn', 3.2, 145738913, 'Toyota', 'Camry', 30301, Decimal('42.523800'), Decimal('72.293400'), 'Buckle up.', 1, None)]

        self.assertEquals(driver_data, expected)

    def test_drive_to_location(self):
        build_db()
        populate_db()

        rider_data = (4,"Ms.Daisy", 1831220273934144, False, 30301, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        driver_data = (8, "Hoke Colburn", 3.2, 145738913, "Toyota", "Camry", 30301, 42.5238, 72.2934, "Buckle up.", 1)

        add_new_driver(driver_data)
        add_new_rider(rider_data)

        ride_info = (4, "Hoke Colburn", '{"Ms.Daisy"}', 4, '{3}', 43.1306, 77.6260,datetime.datetime(2023, 2, 3, 0, 0) )
        add_new_ride(ride_info)

        insert_data = ("Ms.Daisy", "Hoke Colburn")
        ride_data = view_ride(insert_data)
        expected = [(4, 'Hoke Colburn', ['Ms.Daisy'], 4, [3], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, datetime.datetime(2023, 2, 3, 0, 0), None, None, None, False, False, False, Decimal('0.0'), None)]

        self.assertEquals(ride_data, expected)

    def test_rating_driver_and_rider(self):
        build_db()
        populate_db()

        rider_data = (4,"Ms.Daisy", 1831220273934144, False, 30301, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        driver_data = (8, "Hoke Colburn", 3.2, 145738913, "Toyota", "Camry", 30301, 42.5238, 72.2934, "Buckle up.", 1)

        add_new_driver(driver_data)
        add_new_rider(rider_data)       

        driver = (5.0, "Hoke Colburn")
        rider = (4.8, "Ms.Daisy")

        rate_driver(driver)
        rate_rider(rider)

        rating1 = driver_rating(("Hoke Colburn"))
        rating2 = rider_rating(("Ms.Daisy"))

        expected1 = (5.0,)
        expected2 = (4.8,)

        self.assertEquals(rating1, expected1)
        self.assertEquals(rating2, expected2)

    def test_drive_another_driver(self):
        build_db()
        populate_db()

        rider_data = (5,"Hoke Colburn", None, True, 30301, 43.1306, 77.6260, 0.0, "Drive faster", 2)

        add_new_rider(rider_data)

        ride_info = (5, "Tom Magliozzi", '{"Hoke Colburn"}', 6, '{5}', 43.1306, 77.6260, datetime.datetime(2023, 2, 4, 0, 0) )
        add_new_ride(ride_info)

        insert_data = ("Hoke Colburn", "Tom Magliozzi")
        ride_data = view_ride(insert_data)
        expected = [(5, 'Tom Magliozzi', ['Hoke Colburn'], 6, [5], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, datetime.datetime(2023, 2, 4, 0, 0),None, None, None, False, False, False, Decimal('0.0'), None)]

        self.assertEquals(ride_data, expected)

    def test_account_deactivation(self):
        build_db()
        populate_db()
        account = ("Ms.Daisy", 2, datetime.datetime(2023, 2, 8, 0, 0))

        create_new_account(account)
        remove_account(("Ms.Daisy"))

        data = view_profile(("Ms.Daisy"))
        expected = [(3, 'Ms.Daisy', 2, False, datetime.datetime(2023, 2, 8, 0, 0))]

        self.assertEquals(data, expected)

    def test_driver_marked_available(self):
        build_db()
        populate_db()
        #add the driver

        driver_values = (9, "Gadot", 3.2, 374838913, "Chevy", "Cruze", 90210, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_values)
        #Godot marks himself available
        availability = (True, "Gadot")
        update_driver_availability(availability)
        driver_data = view_driver_availability(availability)
        expected =[(9, 'Gadot', 3.2, 374838913, 'Chevy', 'Cruze', 90210, Decimal('42.523800'), Decimal('72.293400'), 'Buckle up.', 1, True)]

        self.assertEquals(driver_data, expected)

    def test_rider_accepts_ride(self):
        build_db()
        populate_db()

        #add the driver
        driver_values = (9, "Gadot", 3.2, 374838913, "Chevy", "Cruze", 90210, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_values)

        #Godot marks himself available
        availability = (True, "Gadot")
        update_driver_availability(availability)

        #add the rider
        rider_values = (5,"Vladmir", 1831220273934144, False, 90210, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        add_new_rider(rider_values)
        
        #create the ride
        ride_info = (5, "Gadot", '{"Vladmir"}', 9, '{5}', 43.1306, 77.6260, datetime.datetime(2023, 2, 8, 0, 0) )
        add_new_ride(ride_info)
        accept_ride(('{"Vladmir"}'))

        ride_info = (("Vladmir", "Gadot"))
        ride_data = view_ride(ride_info)

        expected = [(5, 'Gadot', ['Vladmir'], 9, [5], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, datetime.datetime(2023, 2, 8, 0, 0), None, None,None, False, False,False,Decimal('0.0'), None)]

        self.assertEquals(ride_data, expected)


    def test_rider_never_picked_up(self):
        build_db()
        populate_db()

        #add the driver
        driver_values = (9, "Gadot", 3.2, 374838913, "Chevy", "Cruze", 90210, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_values)

        #Godot marks himself available
        availability = (True, "Gadot")
        update_driver_availability(availability)

        #add the rider
        rider_values = (5,"Vladmir", 1831220273934144, False, 90210, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        add_new_rider(rider_values)
        
        #create the ride
        ride_info = (5, "Gadot", '{"Vladmir"}', 9, '{5}', 43.1306, 77.6260, datetime.datetime(2023, 2, 8, 0, 0) )
        add_new_ride(ride_info)
        accept_ride(("Vladmir"))

        ride_info = (("Vladmir", "Gadot"))

        driver_data = get_pickup_status(ride_info)
        expected = (False,)

        self.assertEquals(driver_data, expected)

    def test_no_receipt_generated(self):
        build_db()
        populate_db()

        #add the driver
        driver_values = (9, "Gadot", 3.2, 374838913, "Chevy", "Cruze", 90210, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_values)

        #Godot marks himself available
        availability = (True, "Gadot")
        update_driver_availability(availability)

        #add the rider
        rider_values = (5,"Vladmir", 1831220273934144, False, 90210, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        add_new_rider(rider_values)
        
        #create the ride
        ride_info = (5, "Gadot", '{"Vladmir"}', 9, '{5}', 43.1306, 77.6260, datetime.datetime(2023, 2, 5, 0, 0) )
        add_new_ride(ride_info)
        accept_ride(("Vladmir"))

        receipt = generate_receipt(("Vladmir","Vladmir",'2022-02-5 19:10:25-07','2022-02-8 19:10:25-07' ))
        expected = []

        self.assertEquals(receipt, expected)

    def test_pick_up_bobby(self):
        build_db()
        populate_db()

        availability = (True, "Alex")
        update_driver_availability(availability)

        first_rider = (5,"Bobby", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        add_new_rider(first_rider)

        ride = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, datetime.datetime(2023, 2, 6, 0, 0) )
        add_new_ride(ride)
        accept_ride("Bobby")

        ride_info = view_ride(("Bobby", "Alex"))

        expected = [(6, 'Alex', ['Bobby'], 10, [6], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, datetime.datetime(2023, 2, 6, 0, 0), None, None, None, False, False, True, Decimal('0.0'), None)]
        self.assertEquals(ride_info, expected)

    def test_carpooling(self):
        build_db()
        populate_db()

        availability = (True, "Alex")
        update_driver_availability(availability)

        first_rider = (5,"Bobby", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        third_rider = (6,"Louis", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        second_rider = (7,"Elaine", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        fourth_rider = (8,"Tony", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)

        add_new_rider(first_rider)
        add_new_rider(second_rider)
        add_new_rider(third_rider)
        add_new_rider(fourth_rider)

        ride = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, datetime.datetime(2023, 2, 8, 0, 0) )
        add_new_ride(ride)
        accept_ride("Bobby")
        add_fare((12,"Alex", "Bobby" ))

        accept_ride("Louis")
        #pick up louis
        add_to_carpool(('{"Louis"}', 6, "Alex", 6))
        #pick up elaine
        accept_ride("Elaine")
        add_to_carpool(('{"Elaine"}', 7, "Alex", 6))
        #pick up tony
        accept_ride("Tony")
        add_to_carpool(('{"Tony"}', 8, "Alex", 6))

        ride_info = view_ride(("Bobby", "Alex"))
        expected = [(6, 'Alex', ['Bobby', '{"Louis"}', '{"Elaine"}', '{"Tony"}'], 10, [6, 6, 7, 8], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('12.00'), None, None, datetime.datetime(2023, 2, 8, 0, 0), None, None, None, False, False, True, Decimal('0.0'), None)]

        self.assertEquals(ride_info, expected)

    def test_split_carpooling_fare(self):
        build_db()
        populate_db()

        availability = (True, "Alex")
        update_driver_availability(availability)

        first_rider = (5,"Bobby", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        third_rider = (6,"Louis", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        second_rider = (7,"Elaine", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        fourth_rider = (8,"Tony", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)

        add_new_rider(first_rider)
        add_new_rider(second_rider)
        add_new_rider(third_rider)
        add_new_rider(fourth_rider)

        ride = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, datetime.datetime(2023, 2, 8, 0, 0) )
        add_new_ride(ride)
        accept_ride("Bobby")
        add_fare((12,"Alex", "Bobby" ))

        accept_ride("Louis")
        #pick up louis
        add_to_carpool(('{"Louis"}', 6, "Alex", 6))
        #pick up elaine
        accept_ride("Elaine")
        add_to_carpool(('{"Elaine"}', 7, "Alex", 6))
        #pick up tony
        accept_ride("Tony")
        add_to_carpool(('{"Tony"}', 8, "Alex", 6))

        split_fare(('6'))
        fare = get_fare(('Bobby'))
        ride_info = view_ride(("Bobby", "Alex"))
        expected = [(Decimal('3.00'),)]

        self.assertEquals(fare, expected)

    def test_retrieve_carpooling_receipt(self):
        build_db()
        populate_db()

        availability = (True, "Alex")
        update_driver_availability(availability)

        first_rider = (5,"Bobby", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        third_rider = (6,"Louis", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        second_rider = (7,"Elaine", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        fourth_rider = (8,"Tony", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)

        add_new_rider(first_rider)
        add_new_rider(second_rider)
        add_new_rider(third_rider)
        add_new_rider(fourth_rider)
        #time = datetime.datetime.fromtimestamp(2023, 2, 8, 0, 0)
        ride = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, '2022-02-8 19:10:25-07') 
        add_new_ride(ride)
        accept_ride("Bobby")
        add_fare((12,"Alex", "Bobby" ))

        accept_ride("Louis")
        #pick up louis
        add_to_carpool(('{"Louis"}', 6, "Alex", 6))
        #pick up elaine
        accept_ride("Elaine")
        add_to_carpool(('{"Elaine"}', 7, "Alex", 6))
        #pick up tony
        accept_ride("Tony")
        add_to_carpool(('{"Tony"}', 8, "Alex", 6))
        
        split_fare(('6'))
        drop_off_rider((1,'2020-06-22 20:10:25-07', True, 6))
        receipt_data = (("Bobby", "Bobby",'2022-02-6 19:10:25-07','2022-02-10 19:10:25-07'))
        receipt = generate_receipt(receipt_data)
        expected = [(6, 'Bobby', Decimal('3.00'))]
        self.assertEquals(receipt, expected)

    def test_full_ride_info(self):
        build_db()
        populate_db()
        driver_values = (9, "Gadot", 3.2, 374838913, "Chevy", "Cruze", 90210, 42.5238, 72.2934, "Buckle up.", 1)
        add_new_driver(driver_values)

        #Godot marks himself available
        availability = (True, "Gadot")
        update_driver_availability(availability)

        #add the rider
        rider_values = (4,"Vladmir", 1831220273934144, False, 90210, 43.1306, 77.6260, 0.0, "Drive safe", 1)
        add_new_rider(rider_values)
        
        #create the ride for Gadot and Vladmir
        ride_info = (5, "Gadot", '{"Vladmir"}', 9, '{5}', 43.1306, 77.6260, datetime.datetime(2023, 2, 5, 0, 0) )

        availability = (True, "Alex")
        update_driver_availability(availability)

        first_rider = (5,"Bobby", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        third_rider = (6,"Louis", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        second_rider = (7,"Elaine", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)
        fourth_rider = (8,"Tony", None, False, 14834, 42.1306, 75.6260, 0.0, "I'm trying to catch a flight", 1)

        add_new_rider(first_rider)
        add_new_rider(second_rider)
        add_new_rider(third_rider)
        add_new_rider(fourth_rider)
        
        ride = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, '2022-02-8 19:10:25-07') 

        add_new_ride(ride)
        add_new_ride(ride_info)
        accept_ride("Bobby")
        add_fare((12,"Alex", "Bobby" ))

        accept_ride("Louis")
        #pick up louis
        add_to_carpool(('{"Louis"}', 6, "Alex", 6))
        #pick up elaine
        accept_ride("Elaine")
        add_to_carpool(('{"Elaine"}', 7, "Alex", 6))
        #pick up tony
        accept_ride("Tony")
        add_to_carpool(('{"Tony"}', 8, "Alex", 6))

        split_fare(('6'))
        drop_off_rider((1,'2020-06-22 20:10:25-07', True, 6))
        #Louis gives the ride a 2
        rate_ride((2.0, 6))
        #Bobby gives the ride a 5
        rate_ride((5.0, 6))
        update_ride_rating((6))
        full_ride = get_full_ride_info(('2020-06-22 20:10:25'))
        print(full_ride)
        expected = [('Gadot', Decimal('77.626000'), Decimal('43.130600'), ['Vladmir'], Decimal('0.0')),('Alex', Decimal('77.626000'), Decimal('43.130600'), ['Bobby', '{"Louis"}', '{"Elaine"}', '{"Tony"}'], Decimal('0.0'))]
        self.assertEquals(full_ride,expected)

    def test_fare_times(self):
        build_db()
        populate_db()

        ride_one = (6, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, '2022-02-8 03:30:00')
        add_new_ride(ride_one)
        add_fare((5,"Alex","Bobby" ))

        ride_two = (7, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, '2022-02-8 04:55:00')
        add_new_ride(ride_two)
        add_fare((10,"Alex","Bobby" ))

        ride_three = (8, "Alex", '{"Bobby"}', 10, '{6}', 43.1306, 77.6260, '2022-02-8 04:59:00')
        add_new_ride(ride_three)
        add_fare((20,"Alex","Bobby" ))

        fare_times = get_fare_times()

        #expected = []

        #self.assertEquals(fare_times, expected)