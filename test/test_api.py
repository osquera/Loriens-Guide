"""Simple test script to verify the API endpoint functionality.

Run the server first with: python server.py
Then run this test with: python test_api.py.
"""

import pytest
import requests


def test_get_guidance_endpoint() -> None:
    """Test the POST /api/get-guidance endpoint."""
    url = "http://localhost:8000/api/get-guidance"
    timeout = 5.0

    # Test data matching the problem statement
    payload = {"latitude": 40.7128, "longitude": -74.0060, "question_text": "I'm looking for the exit, where is it?"}

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        result = response.json()
    except requests.exceptions.Timeout:
        pytest.fail(f"Request timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError as exc:
        pytest.fail(f"Connection error: {exc}")
    except requests.exceptions.RequestException as exc:
        pytest.fail(f"Request failed: {exc}")
    except ValueError:
        pytest.fail("Response is not valid JSON")

    # Verify response structure
    assert "answer_text" in result, "Response missing 'answer_text' field"
    assert isinstance(result["answer_text"], str), "'answer_text' should be a string"
    assert result["answer_text"].strip(), "'answer_text' should not be empty"


def test_health_check() -> None:
    """Test the root health check endpoint."""
    url = "http://localhost:8000/"
    timeout = 5.0

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        # ensure the response is JSON-decodable
        result = response.json()
    except requests.exceptions.Timeout:
        pytest.fail(f"Health check timed out after {timeout} seconds")
    except requests.exceptions.ConnectionError as exc:
        pytest.fail(f"Connection error while contacting {url}: {exc}")
    except requests.exceptions.RequestException as exc:
        pytest.fail(f"Health check request failed: {exc}")
    except ValueError:
        pytest.fail("Health check response is not valid JSON")

    # Basic structure checks
    assert response.status_code == requests.codes.ok, "Health check did not return 200 OK"
    assert result is not None


if __name__ == "__main__":
    # Run tests using pytest when executed as a script
    raise SystemExit(pytest.main([__file__]))
