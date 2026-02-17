#!/usr/bin/env python3
"""
Test specific threat explanations for AI Security Assistant
"""

from src.chat_assistant import ChatAssistant

def test_specific_threats():
    assistant = ChatAssistant()
    
    test_cases = [
        'what is ddos',
        'explain sql injection', 
        'tell me about phishing',
        'how to prevent malware',
        'describe ransomware'
    ]
    
    print('🔍 Testing Specific Threat Explanations:')
    print('=' * 50)
    
    for i, query in enumerate(test_cases, 1):
        response = assistant.process_message(query)
        print(f'{i}. Query: "{query}"')
        print(f'   Type: {response["type"]}')
        print(f'   Response: {response["response"][:80]}...')
        print()

if __name__ == "__main__":
    test_specific_threats()
