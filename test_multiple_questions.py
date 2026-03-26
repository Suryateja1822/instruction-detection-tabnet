#!/usr/bin/env python3
"""
Test multiple questions functionality for AI Security Assistant
"""

from src.chat_assistant import ChatAssistant

def test_multiple_questions():
    assistant = ChatAssistant()
    
    # Test cases with multiple questions
    test_cases = [
        "What is DDoS and how to prevent SQL injection?",
        "Explain phishing and tell me about malware",
        "What is ransomware? How to secure my network? Also what are best practices?",
        "DDoS prevention plus SQL injection protection",
        "Tell me about phishing and explain malware and how to prevent attacks"
    ]
    
    print('🔍 Testing Multiple Questions Functionality:')
    print('=' * 60)
    
    for i, query in enumerate(test_cases, 1):
        print(f'\n📝 Test {i}: "{query}"')
        print('-' * 40)
        
        response = assistant.process_message(query)
        print(f'Type: {response["type"]}')
        print(f'Response: {response["response"][:200]}...')
        
        # Check if it detected multiple questions
        if response["type"] == "multiple_questions":
            print('✅ Multiple questions detected and handled!')
        else:
            print('⚠️ Multiple questions not detected')
        
        print()

if __name__ == "__main__":
    test_multiple_questions()
