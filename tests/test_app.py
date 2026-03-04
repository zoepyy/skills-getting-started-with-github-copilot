"""
Comprehensive tests for the Mergington High School API.
Tests all endpoints and error scenarios.
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint."""

    def test_redirect_to_index_html(self, client):
        """Verify GET / redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Verify GET /activities returns all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_get_activities_contains_all_required_activities(self, client):
        """Verify all expected activities are present."""
        response = client.get("/activities")
        activities = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Club",
            "Painting Workshop",
            "Drama Club",
            "Math Olympiad",
            "Science Research",
        ]
        
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_data_structure(self, client):
        """Verify each activity has required fields."""
        response = client.get("/activities")
        activities = response.json()
        
        required_fields = {
            "description": str,
            "schedule": str,
            "max_participants": int,
            "participants": list,
        }
        
        for activity_name, details in activities.items():
            assert isinstance(activity_name, str)
            for field, field_type in required_fields.items():
                assert field in details, f"Missing field '{field}' in {activity_name}"
                assert isinstance(details[field], field_type), (
                    f"Field '{field}' in {activity_name} should be {field_type.__name__}"
                )


class TestSignupEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_activity, sample_email):
        """Verify successful signup adds participant."""
        # Get activities before signup
        before_response = client.get("/activities")
        before_activities = before_response.json()
        before_count = len(before_activities[sample_activity]["participants"])
        
        # Sign up
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email},
        )
        
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert sample_email in result["message"]
        
        # Verify participant was added
        after_response = client.get("/activities")
        after_activities = after_response.json()
        after_count = len(after_activities[sample_activity]["participants"])
        assert after_count == before_count + 1
        assert sample_email in after_activities[sample_activity]["participants"]

    def test_signup_activity_not_found(self, client, sample_email):
        """Verify HTTP 404 when activity doesn't exist."""
        response = client.post(
            "/activities/NonexistentActivity/signup",
            params={"email": sample_email},
        )
        
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]

    def test_signup_duplicate_email(self, client, sample_activity):
        """Verify HTTP 400 when student already signed up."""
        # Get an existing participant from the activity
        response = client.get("/activities")
        activities = response.json()
        existing_email = activities[sample_activity]["participants"][0]
        
        # Try to sign up with same email
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": existing_email},
        )
        
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"]


class TestUnregisterEndpoint:
    """Tests for POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client, sample_activity, sample_email):
        """Verify successful unregister removes participant."""
        # First sign up
        signup_response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email},
        )
        assert signup_response.status_code == 200
        
        # Verify participant is there
        get_response = client.get("/activities")
        activities = get_response.json()
        assert sample_email in activities[sample_activity]["participants"]
        
        # Now unregister
        unregister_response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email},
        )
        
        assert unregister_response.status_code == 200
        result = unregister_response.json()
        assert "message" in result
        assert sample_email in result["message"]
        
        # Verify participant was removed
        final_response = client.get("/activities")
        final_activities = final_response.json()
        assert sample_email not in final_activities[sample_activity]["participants"]

    def test_unregister_activity_not_found(self, client, sample_email):
        """Verify HTTP 404 when activity doesn't exist."""
        response = client.post(
            "/activities/NonexistentActivity/unregister",
            params={"email": sample_email},
        )
        
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]

    def test_unregister_student_not_signed_up(self, client, sample_activity, sample_email):
        """Verify HTTP 400 when student is not enrolled."""
        response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": sample_email},
        )
        
        assert response.status_code == 400
        result = response.json()
        assert "not signed up" in result["detail"]


class TestActivityParticipantIntegration:
    """Integration tests for signup/unregister workflow."""

    def test_signup_and_unregister_workflow(self, client, sample_activity):
        """Verify complete signup/unregister workflow."""
        test_email = "integration@mergington.edu"
        
        # Verify email is not in activity
        response = client.get("/activities")
        activities = response.json()
        assert test_email not in activities[sample_activity]["participants"]
        
        # Sign up
        signup_response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": test_email},
        )
        assert signup_response.status_code == 200
        
        # Verify email is in activity
        response = client.get("/activities")
        activities = response.json()
        assert test_email in activities[sample_activity]["participants"]
        
        # Unregister
        unregister_response = client.post(
            f"/activities/{sample_activity}/unregister",
            params={"email": test_email},
        )
        assert unregister_response.status_code == 200
        
        # Verify email is removed
        response = client.get("/activities")
        activities = response.json()
        assert test_email not in activities[sample_activity]["participants"]

    def test_multiple_signups(self, client, sample_activity):
        """Verify multiple different students can sign up."""
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu",
        ]
        
        for email in emails:
            response = client.post(
                f"/activities/{sample_activity}/signup",
                params={"email": email},
            )
            assert response.status_code == 200
        
        # Verify all are registered
        response = client.get("/activities")
        activities = response.json()
        for email in emails:
            assert email in activities[sample_activity]["participants"]
