#!/usr/bin/env python3
"""
Debug AI Security Assistant keyword matching
"""

from src.chat_assistant import ChatAssistant

def debug_keyword_matching():
    assistant = ChatAssistant()
    
    test_cases = [
        'what is ddos',
        'explain sql injection', 
        'tell me about phishing',
        'describe ransomware'
    ]
    
    print('🔍 Debugging Keyword Matching:')
    print('=' * 50)
    
    for query in test_cases:
        message_lower = query.lower()
        print(f'Query: "{query}"')
        print(f'Lowercase: "{message_lower}"')
        
        # Test explanation keywords
        explanation_keywords = ["what is", "explain", "tell me about", "describe", "define", "what does"]
        explanation_match = any(word in message_lower for word in explanation_keywords)
        print(f'Explanation keywords match: {explanation_match}')
        
        # Test threat keywords
        ddos_match = "ddos" in message_lower
        sql_match = "sql injection" in message_lower or "sql" in message_lower
        phishing_match = "phishing" in message_lower
        malware_match = "malware" in message_lower or "ransomware" in message_lower
        
        print(f'DDoS match: {ddos_match}')
        print(f'SQL match: {sql_match}')
        print(f'Phishing match: {phishing_match}')
        print(f'Malware match: {malware_match}')
        print('-' * 30)

if __name__ == "__main__":
    debug_keyword_matching()
