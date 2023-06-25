import datetime
from decimal import Decimal
import unittest
from src.rideshare import *
from src.swen344_db_utils import *

class TestRideshareBuild(unittest.TestCase):

    def test_build_Drivers(self):
        """Build the tables"""
        buildDriversTable()
        result = exec_get_all('SELECT * FROM Drivers')
        self.assertEqual([], result, "no rows in Drivers")
    
    def test_build_Riders(self):
        """Build the tables"""
        buildRidersTable()
        result = exec_get_all('SELECT * FROM Riders')
        self.assertEqual([], result, "no rows in Riders")

    def test_build_Rides(self):
        """Build the tables"""
        buildRidesTable()
        result = exec_get_all('SELECT * FROM Rides')
        self.assertEqual([], result, "no rows in Rides")

    def test_build_Accounts(self):
        """Build the tables"""
        buildAccountsTable()
        result = exec_get_all('SELECT * FROM accounts')
        self.assertEqual([], result, "no rows in accounts")

    def test_build_Locations(self):
        """Build the tables"""
        buildLocationsTable()
        result = exec_get_all('SELECT * FROM locations')
        self.assertEqual([], result, "no rows in locations")

    def test_rebuild_Drivers_is_idempotent(self):
      """Drop and rebuild the tables twice"""
      buildDriversTable()
      buildDriversTable()
      result = exec_get_all('SELECT * FROM Drivers')
      self.assertEqual([], result, "no rows in Drivers")
    
    def test_rebuild_Riders_is_idempotent(self):
      """Drop and rebuild the tables twice"""
      buildRidersTable()
      buildRidersTable()
      result = exec_get_all('SELECT * FROM Riders')
      self.assertEqual([], result, "no rows in Riders")

    def test_rebuild_Rides_is_idempotent(self):
      """Drop and rebuild the tables twice"""
      buildRidesTable()
      buildRidesTable()
      result = exec_get_all('SELECT * FROM rides')
      self.assertEqual([], result, "no rows in rides")

    def test_rebuild_Accounts_is_idempotent(self):
      """Drop and rebuild the tables twice"""
      buildAccountsTable()
      buildAccountsTable()
      result = exec_get_all('SELECT * FROM accounts')
      self.assertEqual([], result, "no rows in accounts")

    def test_rebuild_Locations_is_idempotent(self):
      """Drop and rebuild the tables twice"""
      buildLocationsTable()
      buildLocationsTable()
      result = exec_get_all('SELECT * FROM locations')
      self.assertEqual([], result, "no rows in locations")

    """TEST POPULATING TABLES"""

    def test_populate_drivers_table_idepoptent(self):
      """Add two records to the table"""
      populateDriversTable()
      populateDriversTable()
      result = exec_get_all('SELECT * FROM Drivers')
      self.assertEqual([(1, 'Tom Magliozzi', 3.2, 145738913, 'Toyota', 'Camry', 23456, Decimal('42.523800'), Decimal('72.293400'), 'Do not drive like my brother.', 1, None), (2, 'Ray Magliozzi', 3.4, 123456789, 'Toyota', 'Rav-4', 23456, Decimal('43.773200'), Decimal('71.018400'), 'Do not drive like my brother.', 2, None),(3, 'ALEX', 0.0, 443006789, 'Honda', 'Crv', 83924, Decimal('41.700200'), Decimal('70.928400'), None, 2, None),(4, 'Bobby', 0.0, 148950089, 'Toyota', 'Prius', 14492, Decimal('41.773200'), Decimal('73.018400'), None, 2, None),(5, 'Louis', 0.0, 987456789, 'Toyota', 'Rav-4', 23456, Decimal('43.693200'), Decimal('70.918400'), None, 2, None),(6, 'Elaine', 3.4, 123456789, 'Toyota', 'Rav-4', 23456, Decimal('43.773200'), Decimal('71.018400'), None, 2, None),(7, 'Tony', 3.4, 987423081, 'Toyota', 'Rav-4', 83956, Decimal('43.773200'), Decimal('71.018400'), None, 2, None) ], result)


    def test_populate_riders_table_idepoptent(self):
      """Add two records to the table"""
      populateRidersTable()
      populateRidersTable()
      result = exec_get_all('SELECT * FROM Riders')
      self.assertEqual([((1, 'Mike Easter', 1111222233334444, True, 12345, Decimal('42.729800'), Decimal('73.678900'), 4.3, None, 1, Decimal('0.00'), None)), ((2, 'Ray Magliozzi', None, True, 67890, Decimal('3.400000'), Decimal('43.130600'), 77.626, 'Do not drive like my brother.', 2, Decimal('0.00'), None))], result)

    def test_populate_rides_table_idepoptent(self):
      """Add two records to the table"""
      populateRidesTable()
      populateRidesTable()
      result = exec_get_all('SELECT * FROM Rides')
      expected = [(1, 'Tom Magliozzi', ['Mike Easter'], 1, [1], Decimal('43.084800'), Decimal('77.671500'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None ), (2, 'Ray Magliozzi', ['Mike Easter'], 2, [1], Decimal('42.729800'), Decimal('73.678900'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None),(3, 'Tom Magliozzi', ['Ray Magliozzi'], 1, [2], Decimal('43.130600'), Decimal('77.626000'), None, None, Decimal('0.00'), None, None, None, None, None, None, False, False, False, Decimal('0.0'), None)]
      self.assertEqual(expected, result)

    def test_populate_accounts_table(self):
      """Add two records to the table"""
      populateAccountsTable()
      populateAccountsTable()
      result = exec_get_all('SELECT * FROM accounts')
      expected = [(3, 'Tom Magliozzi', 1, True, datetime.datetime(2023, 2, 8, 0, 0)), (4, 'Ray Magliozzi', 1, True, datetime.datetime(2023, 2, 8, 0, 0))]
      self.assertEqual(expected, result)

    def test_populate_locations_table_idepoptent(self):
      """Add two records to the table"""
      populateLocationsTable()
      populateLocationsTable()
      result = exec_get_all('SELECT * FROM locations')
      expected = [(3, 'RIT','1 Lomb Memorial Dr',  'Rochester', 14623), (4, 'UofR','300 Wilson Boulevard',  'Rochester', 14627)]
      self.assertEqual(expected, result)