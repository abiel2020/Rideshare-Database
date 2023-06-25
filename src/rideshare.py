import datetime
from src.swen344_db_utils import *


def buildDriversTable():
  """Create the tables to initialize the db"""
  conn = connect()
  cur = conn.cursor()
  drop_sql = """
        DROP TABLE IF EXISTS drivers CASCADE
    """
  create_sql = """
        CREATE TABLE drivers(
            id INTEGER NOT NULL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            average_rating DOUBLE PRECISION NOT NULL DEFAULT 0.0,
            license_number BIGINT NOT NULL,
            car_make VARCHAR NOT NULL,
            car_model VARCHAR NOT NULL,
            zipcode INT,
            longitude DECIMAL(9,6) NOT NULL,
            latitude DECIMAL(8,6) NOT NULL,
            special_instructions VARCHAR(100) DEFAULT 'Please wear your seatbelt.',
            location_id INT NOT NULL,
            available BOOLEAN
        )
  """

  cur.execute(drop_sql)
  cur.execute(create_sql)
  conn.commit()
  conn.close()

def populateDriversTable():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM drivers ")
  populate = """INSERT INTO drivers (id, name, average_rating, license_number, car_make, car_model, zipcode, longitude, latitude, special_instructions, location_id) VALUES (1, 'Tom Magliozzi', 3.2, 145738913, 'Toyota', 'Camry',23456, 42.5238, 72.2934, 'Do not drive like my brother.',1 ), (2, 'Ray Magliozzi', 3.4, 123456789,  'Toyota', 'Rav-4', 23456, 43.7732, 71.0184, 'Do not drive like my brother.', 2),(3, 'ALEX', 0.0, 443006789,  'Honda', 'Crv', 83924, 41.7002, 70.9284, NULL, 2), (4, 'Bobby', 0.0, 148950089,  'Toyota', 'Prius', 14492, 41.7732, 73.0184, NUll, 2), (5, 'Louis', 0.0, 987456789,  'Toyota', 'Rav-4', 23456, 43.6932, 70.9184, NULL, 2), (6, 'Elaine', 3.4, 123456789,  'Toyota', 'Rav-4', 23456, 43.7732, 71.0184, NULL, 2), (7, 'Tony', 3.4, 987423081,  'Toyota', 'Rav-4', 83956, 43.7732, 71.0184, NULL, 2)"""
  cur.execute(populate)
  conn.commit()
  cur.close
  conn.close()

def buildRidersTable():
  """Create the tables to initialize the db"""
  conn = connect()
  cur = conn.cursor()
  drop_sql = """
        DROP TABLE IF EXISTS riders CASCADE
    """
  create_sql = """
        CREATE TABLE riders(
            id INT NOT NULL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            credit_card_num BIGINT,
            available BOOLEAN NOT NULL,
            zipcode INT NOT NULL,
            longitude DECIMAL(9,6) NOT NULL,
            latitude DECIMAL(8,6) NOT NULL,
            average_rating DOUBLE PRECISION NOT NULL DEFAULT 0.0,
            special_instructions VARCHAR(100) DEFAULT 'No special instructions',
            location_id INT NOT NULL,
            receipt DECIMAL(8,2) NOT NULL DEFAULT 0.0,
            ride_id INT
            )
  """
  cur.execute(drop_sql)
  cur.execute(create_sql)
  conn.commit()
  conn.close()

def populateRidersTable():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM riders")
  populate = """INSERT INTO riders (id, name, credit_card_num, available, zipcode, longitude, latitude, average_rating, special_instructions, location_id) VALUES (1, 'Mike Easter', 1111222233334444, true, 12345, 42.7298, 73.6789, 4.3, NULL, 1), (2, 'Ray Magliozzi', NULL , true, 67890, 3.4, 43.1306, 77.6260, 'Do not drive like my brother.', 2)"""
  cur.execute(populate)
  conn.commit()
  cur.close
  conn.close()

def buildRidesTable():
  """Create the tables to initialize the db"""
  conn = connect()
  cur = conn.cursor()
  drop_sql = """
        DROP TABLE IF EXISTS rides
    """
    
  create_sql = """
        CREATE TABLE rides(
        id INT PRIMARY KEY,
        driver_name VARCHAR(20) NOT NULL,
        rider_name VARCHAR(20)[] NOT NULL,
        driver_id INT NOT NULL,
        rider_id INT[] NOT NULL,
        longitude DECIMAL(9,6) NOT NULL,
        latitude DECIMAL(8,6) NOT NULL,
        driver_review VARCHAR(100),
        rider_review VARCHAR(100),
        fare DECIMAL(8,2) DEFAULT 0.0,
        start_location_id INT,
        end_location_id INT ,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        driver_response VARCHAR(100),
        rider_response VARCHAR(100),
        pick_up BOOLEAN NOT NULL DEFAULT FALSE,
        drop_off BOOLEAN NOT NULL DEFAULT FALSE,
        accepted BOOLEAN NOT NULL DEFAULT FALSE,
        average_rating DECIMAL(2,1) DEFAULT 0.0,
        rider_rating DECIMAL(2,1)[]
        )
        """
  cur.execute(drop_sql)
  cur.execute(create_sql)
  conn.commit()
  conn.close()

def populateRidesTable():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM rides")
  populate = """INSERT INTO rides (id, driver_name, rider_name,  driver_id, rider_id, longitude, latitude) VALUES (1, 'Tom Magliozzi', '{Mike Easter}', 1, '{1}', 43.0848, 77.6715), (2, 'Ray Magliozzi', '{Mike Easter}', 2, '{1}', 42.7298, 73.6789), (3, 'Tom Magliozzi', '{Ray Magliozzi}', 1, '{2}', 43.1306, 77.6260)"""
  cur.execute(populate)
  conn.commit()
  cur.close
  conn.close()

def buildAccountsTable():
  conn = connect()
  cur = conn.cursor()
  drop_sql = """
        DROP TABLE IF EXISTS accounts
    """
  create_sql = """
        CREATE TABLE accounts(
          id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          user_name VARCHAR(20) NOT NULL,
          account_type INT CHECK( account_type = 1 OR account_type = 2),
          active BOOLEAN NOT NULL DEFAULT true,
          join_date TIMESTAMP NOT NULL
        )
        """
  cur.execute(drop_sql)
  cur.execute(create_sql)
  conn.commit()
  conn.close()

def populateAccountsTable():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM accounts")
  time_stamp1 = datetime.datetime(2023,2,8)
  time_stamp2 = datetime.datetime(2023,2,8)
  data1 = ('Tom Magliozzi', 1, True, time_stamp1 )
  data2 = ('Ray Magliozzi', 1, True, time_stamp2) 
  cur.execute("""INSERT INTO accounts (user_name, account_type, active, join_date) VALUES(%s,%s,%s, %s) """, data1)
  cur.execute("""INSERT INTO accounts (user_name, account_type, active, join_date) VALUES(%s,%s,%s, %s) """, data2)
  conn.commit()
  cur.close
  conn.close()


def buildLocationsTable():
  conn = connect()
  cur = conn.cursor()
  drop_sql = """
        DROP TABLE IF EXISTS locations
    """  
  create_sql = """
      CREATE TABLE locations(
        id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        location_name VARCHAR(20),
        street_address VARCHAR(20) NOT NULL,
        city_name VARCHAR(20) NOT NULL,
        zipcode INT NOT NULL
      )
      """
  cur.execute(drop_sql)
  cur.execute(create_sql)
  conn.commit()
  conn.close()

def populateLocationsTable():
  conn = connect()
  cur = conn.cursor()
  cur.execute("DELETE FROM locations")
  populate = """INSERT INTO locations(location_name, street_address, city_name, zipcode) VALUES ('RIT', '1 Lomb Memorial Dr' , 'Rochester', 14623), ('UofR','300 Wilson Boulevard', 'Rochester', 14627)"""
  cur.execute(populate)
  conn.commit()
  cur.close
  conn.close()

def build_db():
  buildDriversTable()
  buildRidersTable()
  buildRidesTable()
  buildAccountsTable()
  buildLocationsTable()


def populate_db():
  populateDriversTable()
  populateRidersTable()
  populateRidesTable()
  populateAccountsTable()
  populateLocationsTable()