"""Tests for activity signup functionality"""
import pytest


def test_signup_for_activity_success(client):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=test@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "test@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_for_nonexistent_activity(client):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_duplicate_signup_prevention(client):
    """Test that a student cannot sign up twice for the same activity"""
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Student is already signed up"


def test_signup_adds_participant_to_list(client):
    """Test that signup actually adds the participant to the activity"""
    email = "newstudent@mergington.edu"
    activity = "Programming Class"
    
    # Get initial participants
    response1 = client.get("/activities")
    initial_participants = response1.json()[activity]["participants"]
    
    # Sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Check participants were updated
    response2 = client.get("/activities")
    updated_participants = response2.json()[activity]["participants"]
    
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_with_special_characters_in_activity_name(client):
    """Test signup with URL encoding for special characters"""
    # This tests that the endpoint handles URL encoding properly
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@mergington.edu"
    )
    assert response.status_code in [200, 400]  # Either success or already signed up
