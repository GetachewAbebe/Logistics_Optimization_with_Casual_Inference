import unittest
import os
import sys
from datetime import datetime
# Adjust the path to include the utils directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils/')))
from data_cleaning import DataPipeline

pipeline = DataPipeline('Nigeria')

class TestDataPipeline(unittest.TestCase):

    def test_isWeekend(self):
        date = datetime(2023, 1, 1)  # Sunday
        self.assertTrue(pipeline.is_weekend(date))

        date = datetime(2023, 1, 2)  # Monday
        self.assertFalse(pipeline.is_weekend(date))

    def test_isHoliday(self):
        # Assuming Nigeria's public holidays are set in the DataPipeline class
        date = datetime(2023, 1, 1)  # New Year's Day
        self.assertTrue(pipeline.is_holiday(date))

        date = datetime(2023, 12, 25)  # Christmas Day
        self.assertTrue(pipeline.is_holiday(date))

        date = datetime(2023, 1, 3)
        self.assertFalse(pipeline.is_holiday(date))

    def test_calculate_distance(self):
        origin_str = "6.4316714,3.4555375"
        dest_str = "6.4316714,3.4555375"
        distance = pipeline.calculate_distance(origin_str, dest_str)
        self.assertEqual(distance, 0)

        # Different coordinates
        origin_str = "6.5243793,3.3792057"  # Lagos Mainland
        dest_str = "6.465422,3.406448"     # Lagos Island
        distance = pipeline.calculate_distance(origin_str, dest_str)
        self.assertAlmostEqual(distance, 8.5, places=1)  # Example value, use actual distance

    def test_driver_recommendation(self):
        # Mock function or actual implementation to test driver recommendation logic
        # Assuming recommend_drivers is a method in DataPipeline that recommends drivers based on some logic
        orders = [{'lat': 6.5244, 'lng': 3.3792}, {'lat': 6.4654, 'lng': 3.4064}]
        recommendations = pipeline.recommend_drivers(orders)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

if __name__ == '__main__':
    unittest.main()