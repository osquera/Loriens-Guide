"""
Integration tests for Flask API
"""

import unittest
import json
from app import app


class TestAPI(unittest.TestCase):
    """Test cases for Flask API endpoints."""
    
    def setUp(self):
        """Set up test client."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_list_cameras(self):
        """Test listing all cameras."""
        response = self.client.get('/api/v1/cameras')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('cameras', data)
        self.assertIsInstance(data['cameras'], list)
        self.assertGreater(len(data['cameras']), 0)
    
    def test_find_nearest_camera_success(self):
        """Test finding nearest camera with valid coordinates."""
        payload = {
            "lat": 55.6761,
            "long": 12.5683
        }
        
        response = self.client.post(
            '/api/v1/cameras/nearest',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('camera', data)
        self.assertIn('camera_id', data['camera'])
    
    def test_find_nearest_camera_missing_fields(self):
        """Test finding nearest camera with missing fields."""
        payload = {
            "lat": 55.6761
            # Missing 'long'
        }
        
        response = self.client.post(
            '/api/v1/cameras/nearest',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertTrue(data['error'])
    
    def test_find_nearest_camera_invalid_data(self):
        """Test finding nearest camera with invalid data types."""
        payload = {
            "lat": "invalid",
            "long": 12.5683
        }
        
        response = self.client.post(
            '/api/v1/cameras/nearest',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertTrue(data['error'])
    
    def test_query_missing_fields(self):
        """Test query endpoint with missing required fields."""
        payload = {
            "lat": 55.6761,
            "long": 12.5683
            # Missing 'question_text'
        }
        
        response = self.client.post(
            '/api/v1/query',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertTrue(data['error'])
    
    def test_query_invalid_json(self):
        """Test query endpoint with invalid JSON."""
        response = self.client.post(
            '/api/v1/query',
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_query_not_json(self):
        """Test query endpoint with non-JSON content type."""
        response = self.client.post(
            '/api/v1/query',
            data='some data',
            content_type='text/plain'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertTrue(data['error'])
        self.assertIn('JSON', data['message'])


if __name__ == '__main__':
    unittest.main()
