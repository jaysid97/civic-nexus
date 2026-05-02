"""
Unit tests for the AI Services module.
"""

import pytest
from unittest.mock import MagicMock, patch
from services import ElectionAssistant, get_state_registration_deadline

def test_get_state_registration_deadline_known_state():
    """Test that the tool correctly returns data for a known state."""
    result = get_state_registration_deadline("California")
    assert "Oct 21" in result

def test_get_state_registration_deadline_unknown_state():
    """Test that the tool correctly handles unknown states."""
    result = get_state_registration_deadline("Narnia")
    assert "don't have the specific deadline data" in result

@patch('services.genai.GenerativeModel')
def test_election_assistant_initialization(mock_generative_model):
    """Test that the assistant initializes properly with the correct model and tools."""
    # Mock the return value of start_chat
    mock_chat_session = MagicMock()
    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat_session
    mock_generative_model.return_value = mock_model_instance

    assistant = ElectionAssistant()
    
    assert assistant.model is not None
    assert assistant.chat_session is not None
    mock_generative_model.assert_called_once()
    
    # Check that tools were passed
    _, kwargs = mock_generative_model.call_args
    assert 'tools' in kwargs
    assert get_state_registration_deadline in kwargs['tools']

@patch('services.genai.GenerativeModel')
def test_election_assistant_send_message(mock_generative_model):
    """Test that send_message correctly formats and sends input."""
    # Setup mocks
    mock_chat_session = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Mocked response"
    mock_chat_session.send_message.return_value = mock_response
    
    mock_model_instance = MagicMock()
    mock_model_instance.start_chat.return_value = mock_chat_session
    mock_generative_model.return_value = mock_model_instance
    
    assistant = ElectionAssistant()
    
    # Test sending text
    result = assistant.send_message("Hello")
    assert result == "Mocked response"
    mock_chat_session.send_message.assert_called_with(["Hello"])
