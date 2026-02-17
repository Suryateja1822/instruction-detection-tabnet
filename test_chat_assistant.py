#!/usr/bin/env python3
"""
Test script for AI Security Assistant functionality
"""

from src.chat_assistant import ChatAssistant

def test_ai_assistant():
    print('🔍 Testing AI Security Assistant...')
    print('=' * 50)
    
    # Initialize assistant
    assistant = ChatAssistant()
    print('✅ Assistant initialized successfully')
    
    # Test 1: Greeting
    print('\n📝 Test 1: Greeting Response')
    response1 = assistant.process_message('hello')
    print(f'Input: "hello"')
    print(f'Response: {response1["response"][:100]}...')
    print(f'Type: {response1["type"]}')
    
    # Test 2: Help Request
    print('\n📝 Test 2: Help Request')
    response2 = assistant.process_message('help')
    print(f'Input: "help"')
    print(f'Response: {response2["response"][:100]}...')
    print(f'Type: {response2["type"]}')
    
    # Test 3: Threat Explanation
    print('\n📝 Test 3: Threat Explanation')
    response3 = assistant.process_message('what is ddos')
    print(f'Input: "what is ddos"')
    print(f'Response: {response3["response"][:100]}...')
    print(f'Type: {response3["type"]}')
    
    # Test 4: Solution Request
    print('\n📝 Test 4: Solution Request')
    response4 = assistant.process_message('how to prevent sql injection')
    print(f'Input: "how to prevent sql injection"')
    print(f'Response: {response4["response"][:100]}...')
    print(f'Type: {response4["type"]}')
    
    # Test 5: Best Practices
    print('\n📝 Test 5: Best Practices')
    response5 = assistant.process_message('security best practices')
    print(f'Input: "security best practices"')
    print(f'Response: {response5["response"][:100]}...')
    print(f'Type: {response5["type"]}')
    
    # Test 6: Unknown Query
    print('\n📝 Test 6: Unknown Query')
    response6 = assistant.process_message('random query')
    print(f'Input: "random query"')
    print(f'Response: {response6["response"][:100]}...')
    print(f'Type: {response6["type"]}')
    
    # Test 7: Conversation History
    print('\n📝 Test 7: Conversation History')
    history = assistant.get_conversation_history()
    print(f'Conversation length: {len(history)} messages')
    if len(history) >= 2:
        print(f'Last user message: {history[-2]["content"]}')
    else:
        print('Last user message: None')
    
    print('\n' + '=' * 50)
    print('🎉 AI Security Assistant Testing Complete!')
    
    # Summary
    print('\n📊 Test Summary:')
    print(f'✅ Greeting Test: {"PASS" if "hello" in response1["response"].lower() else "FAIL"}')
    print(f'✅ Help Test: {"PASS" if "help" in response2["response"].lower() else "FAIL"}')
    print(f'✅ Threat Explanation Test: {"PASS" if "ddos" in response3["response"].lower() else "FAIL"}')
    print(f'✅ Solution Request Test: {"PASS" if "prevent" in response4["response"].lower() else "FAIL"}')
    print(f'✅ Best Practices Test: {"PASS" if "security" in response5["response"].lower() else "FAIL"}')
    print(f'✅ Unknown Query Test: {"PASS" if "not sure" in response6["response"].lower() or "security" in response6["response"].lower() else "FAIL"}')
    print(f'✅ Conversation History Test: {"PASS" if len(history) > 0 else "FAIL"}')

if __name__ == "__main__":
    test_ai_assistant()
