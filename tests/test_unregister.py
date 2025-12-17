"""Tests for activity unregister functionality"""
import pytest


def test_unregister_from_activity_success(client):
    """Test successful unregistration from an activity"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Verify the participant is initially registered
    response1 = client.get("/activities")
    assert email in response1.json()[activity]["participants"]
    
    # Unregister
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity in data["message"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregistration from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_student_not_signed_up(client):
    """Test unregistration of a student who is not signed up"""
    email = "notsignedup@mergington.edu"
    activity = "Chess Club"
    
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"


def test_unregister_removes_participant_from_list(client):
    """Test that unregister actually removes the participant from the activity"""
    email = "michael@mergington.edu"
    activity = "Chess Club"
    
    # Get initial participants
    response1 = client.get("/activities")
    initial_participants = response1.json()[activity]["participants"]
    assert email in initial_participants
    
    # Unregister
    client.delete(f"/activities/{activity}/unregister?email={email}")
    
    # Check participants were updated
    response2 = client.get("/activities")
    updated_participants = response2.json()[activity]["participants"]
    
    assert email not in updated_participants
    assert len(updated_participants) == len(initial_participants) - 1


def test_signup_after_unregister(client):
    """Test that a student can sign up again after unregistering"""
    email = "test@mergington.edu"
    activity = "Programming Class"
    
    # Sign up
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Unregister
    response1 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response1.status_code == 200
    
    # Sign up again
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 200
    
    # Verify participant is in the list
    response3 = client.get("/activities")
    assert email in response3.json()[activity]["participants"]
