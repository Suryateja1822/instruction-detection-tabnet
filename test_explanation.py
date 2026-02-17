#!/usr/bin/env python3
"""
Test threat explanation method directly
"""

from src.chat_assistant import ChatAssistant

def test_explanation_method():
    assistant = ChatAssistant()
    
    # Test the method directly
    query = "what is ddos"
    print(f'Testing query: "{query}"')
    
    # Call the method directly
    result = assistant._handle_threat_explanation(query)
    
    print(f'Response type: {result["type"]}')
    print(f'Response: {result["response"][:100]}...')
    print()

if __name__ == "__main__":
    test_explanation_method()
