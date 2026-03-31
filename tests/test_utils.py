from src.app import normalize_email


def test_normalize_email_trims_and_lowercases():
    # Arrange
    raw_email = "  Student@Mergington.EDU  "

    # Act
    normalized_email = normalize_email(raw_email)

    # Assert
    assert normalized_email == "student@mergington.edu"


def test_normalize_email_handles_already_normalized_input():
    # Arrange
    raw_email = "student@mergington.edu"

    # Act
    normalized_email = normalize_email(raw_email)

    # Assert
    assert normalized_email == "student@mergington.edu"


def test_normalize_email_blank_input_returns_blank():
    # Arrange
    raw_email = "   "

    # Act
    normalized_email = normalize_email(raw_email)

    # Assert
    assert normalized_email == ""