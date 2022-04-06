from fastapi.testclient import TestClient
from backend.api.api import app


class TestAPI:
    """
    This test class tests the API layer of the application.
    """
    client = TestClient(app)

    def test_health_check(self):
        """
        Tests the health check API endpoint that is used to check if the backend is still running.
        """
        response = TestAPI.client.get("/api/health")

        assert response.status_code == 200
        assert response.json() == {"response": "API is up and running!"}

    def test_tweet_analyzer(self, mocker):
        """
        Tests the tweet analyzer API endpoint that computes the argumentation models and does all the computation.
        """
        # Mock the controller to return "Success" as the controller is not being tested here, to ensure better
        # test separation and quality.
        mocker.patch("backend.controllers.tweet_analyzer_controller.TweetAnalyzerController.analyze_tweet",
                     return_value="Success")

        response = TestAPI.client.get("/api/analyze/123")

        assert response.status_code == 200
        assert response.json() == {"response": "Success"}

    def test_tweet_analyzer_error(self, mocker):
        """
        Tests the tweet analyzer API endpoint in the case of an error.
        """
        # Mock the controller and throw an exception
        mocker.patch("backend.controllers.tweet_analyzer_controller.TweetAnalyzerController.analyze_tweet",
                     side_effect=Exception("Oops"))

        response = TestAPI.client.get("/api/analyze/123")

        # The status code is an internal server error as it should be, along with a helpful error text
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Oops! Something went wrong while processing your request. Make sure the Tweet ID passed is "
                      "valid and try again later."}

