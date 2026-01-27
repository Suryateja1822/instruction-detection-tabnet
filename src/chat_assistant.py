"""
AI Chat Assistant for TabNet-IDS
Provides conversational interface for threat analysis and solutions
"""

import random
from typing import Dict, List, Optional
from solution_recommender import SolutionRecommender

class ChatAssistant:
    """AI Chat Assistant for security threat analysis"""
    
    def __init__(self, solutions_file: str = 'solutions_db.json'):
        """Initialize with solutions database"""
        self.recommender = SolutionRecommender(solutions_file)
        self.conversation_history = []
        self._setup_prompts()
    
    def _setup_prompts(self):
        """Initialize system prompts and greetings"""
        self.system_prompt = """
        You are a helpful security analyst assistant for TabNet-IDS, an Intrusion Detection System.
        Your role is to help users understand security threats, explain detection results, 
        and provide actionable solutions in a clear, professional manner.
        
        Guidelines:
        - Be concise and technical but avoid unnecessary jargon
        - Focus on practical, actionable advice
        - Reference specific threats and solutions from the knowledge base
        - If unsure, say so rather than guessing
        - Always maintain a professional and helpful tone
        - When explaining technical concepts, provide examples when possible
        - For security issues, always mention the potential impact and severity
        - Suggest next steps or additional resources when appropriate
        """
        
        self.greetings = [
            "🔒 Hello! I'm your TabNet-IDS security assistant. I can help you understand and mitigate security threats. What would you like to know?",
            "🛡️ Welcome to TabNet-IDS security support. I can explain detected threats and provide solutions. How can I assist you today?",
            "👋 Hi there! I'm here to help you with security analysis and threat mitigation. What security concerns would you like to discuss?"
        ]
        
        self.unknown_responses = [
            "I'm not sure I understand. Could you rephrase that or ask about a specific security concern? I can help with threat analysis, security best practices, and solution recommendations.",
            "I'm trained to help with security-related questions. Could you clarify what you'd like to know? For example, you can ask about specific threats, request a security analysis, or ask for mitigation strategies.",
            "I'm not sure how to respond to that. I can help with: \n- Explaining security threats \n- Providing mitigation strategies \n- Analyzing security events \n- Recommending security best practices"
        ]
        
        self.help_responses = [
            "I can help you with: \n• Threat analysis and explanation \n• Security recommendations \n• Mitigation strategies \n• Security best practices \n• Understanding detection results",
            "You can ask me things like: \n• 'Explain this threat: SQL injection' \n• 'How do I prevent DDoS attacks?' \n• 'What are the best practices for secure authentication?' \n• 'Help me understand this security alert'"
        ]
        
        self.security_tips = [
            "💡 **Security Tip:** Always keep your systems and software updated with the latest security patches.",
            "🔑 **Best Practice:** Use strong, unique passwords and enable multi-factor authentication (MFA) wherever possible.",
            "📊 **Did You Know?** Regular security audits can help identify vulnerabilities before they're exploited.",
            "🛡️ **Pro Tip:** Implement the principle of least privilege (PoLP) to minimize potential damage from security breaches.",
            "🔍 **Security Reminder:** Regularly review and update your backup strategy to ensure quick recovery from incidents."
        ]
    
    def get_greeting(self) -> str:
        """Return a random greeting message"""
        return random.choice(self.greetings)
    
    def get_unknown_response(self) -> str:
        """Return a random 'I don't understand' response"""
        return random.choice(self.unknown_responses)
        
    def get_help_response(self) -> str:
        """Return a help message with available commands"""
        return random.choice(self.help_responses)
        
    def get_security_tip(self) -> str:
        """Return a random security tip"""
        return random.choice(self.security_tips)
        
    def analyze_threat(self, threat_type: str) -> str:
        """Generate a detailed analysis of a specific threat"""
        solution = self.recommender.get_solution(threat_type)
        if not solution:
            return f"I don't have specific information about '{threat_type}'. Could you try a different term or ask about a general security topic?"
            
        response = [
            f"🔍 **{solution.name} Analysis**",
            f"**Severity:** {solution.severity}",
            "",
            f"**Description:** {solution.description}",
            "",
            "**Recommended Solutions:**",
        ]
        
        for i, sol in enumerate(solution.solutions, 1):
            response.append(f"{i}. {sol}")
            
        response.extend([
            "",
            "**Mitigation Steps:**"
        ])
        
        for i, step in enumerate(solution.mitigation_steps, 1):
            response.append(f"{i}. {step}")
            
        return "\n".join(response)
        
    def process_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Process a user message and generate a response
        
        Args:
            message: User's message
            context: Additional context (e.g., current threat being analyzed)
            
        Returns:
            Dict containing response text and any additional data
        """
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Simple keyword-based response generation
        message_lower = message.lower()
        
        # Check for greetings
        if any(word in message_lower for word in ["hi", "hello", "hey", "greetings"]):
            return {"response": f"{self.get_greeting()} {self.get_security_tip()}", "type": "greeting"}
        """Generate help response with available commands"""
        return """I can help you with:
        - Explaining security threats
        - Providing solutions for detected issues
        - Answering questions about your security alerts
        
        Try asking:
        • "What is a SQL injection attack?"
        • "How do I prevent DDoS attacks?"
        • "Explain the latest threats in my network"
        """
    
    def _handle_solution_request(self, message: str) -> Dict:
        """Handle requests for threat solutions"""
        # Try to find a matching threat in the knowledge base
        similar_threats = self.recommender.find_similar_threats(message)
        
        if similar_threats and similar_threats[0]['score'] > 0.3:  # Threshold for good match
            threat_id = similar_threats[0]['id']
            solution = self.recommender.get_solution(threat_id)
            
            if solution:
                response = f"🔒 {solution.name} ({solution.severity} Threat)\n\n"
                response += f"{solution.description}\n\n"
                response += "🛡️ Recommended Solutions:\n"
                for i, sol in enumerate(solution.solutions[:5], 1):  # Top 5 solutions
                    response += f"{i}. {sol}\n"
                
                response += "\n🚀 Immediate Actions:\n"
                for i, step in enumerate(solution.mitigation_steps[:3], 1):  # Top 3 actions
                    response += f"{i}. {step}\n"
                
                self.conversation_history.append({"role": "assistant", "content": response})
                return {
                    "response": response,
                    "type": "solution",
                    "threat_name": solution.name,
                    "severity": solution.severity
                }
        
        # If no specific threat found, provide general security advice
        response = "I'm not sure which specific threat you're referring to. "
        response += "Here are some general security best practices:\n\n"
        response += "1. Keep all systems and software up to date\n"
        response += "2. Use strong, unique passwords and enable MFA\n"
        response += "3. Regularly back up important data\n"
        response += "4. Use a firewall and keep it properly configured\n"
        response += "5. Educate users about phishing and social engineering"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "type": "general_advice"}
    
    def _handle_threat_explanation(self, message: str) -> Dict:
        """Handle requests for threat explanations"""
        # Try to find a matching threat in the knowledge base
        similar_threats = self.recommender.find_similar_threats(message)
        
        if similar_threats and similar_threats[0]['score'] > 0.3:  # Threshold for good match
            threat_id = similar_threats[0]['id']
            solution = self.recommender.get_solution(threat_id)
            
            if solution:
                response = f"🔍 {solution.name} - Threat Overview\n\n"
                response += f"{solution.description}\n\n"
                response += f"Severity: {solution.severity}\n"
                response += "\nCommon Indicators:\n"
                response += "• Unusual network traffic patterns\n"
                response += "• Unexpected system behavior\n"
                response += "• Unauthorized access attempts\n"
                response += "• System performance degradation"
                
                self.conversation_history.append({"role": "assistant", "content": response})
                return {
                    "response": response,
                    "type": "threat_explanation",
                    "threat_name": solution.name
                }
        
        # If no specific threat found, provide general information
        response = "I'm not sure which specific threat you're asking about. "
        response += "Here are some common security threats you might be interested in:\n\n"
        response += "• SQL Injection\n"
        response += "• Cross-Site Scripting (XSS)"
        response += "• DDoS Attacks\n"
        response += "• Malware & Ransomware\n"
        response += "• Phishing Attacks\n\n"
        response += "You can ask me about any of these for more details."
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "type": "general_info"}
    
    def _generate_default_response(self, message: str) -> Dict:
        """Generate a response for general queries"""
        # Check if the message contains any known threat keywords
        threat_keywords = [
            "sql", "injection", "ddos", "brute force", "xss", 
            "malware", "phishing", "ransomware", "attack", "breach"
        ]
        
        if any(keyword in message.lower() for keyword in threat_keywords):
            # If it's about a security topic but we're not sure what specifically
            response = "I can help you with security-related questions. "
            response += "Could you be more specific about what you'd like to know?\n\n"
            response += "For example, you could ask:\n"
            response += "• What is a " + message.split()[0] + " attack?\n"
            response += "• How to prevent " + message + "?\n"
            response += "• What are the signs of a " + message + " attack?"
        else:
            # For completely unrelated queries
            response = self.get_unknown_response()
            response += " I specialize in security-related questions. "
            response += "How can I assist you with network security or threat detection today?"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "type": "general_response"}
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the full conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []


# Example usage
if __name__ == "__main__":
    assistant = ChatAssistant()
    
    print(assistant.get_greeting())
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Assistant: Goodbye! Stay secure!")
            break
            
        response = assistant.process_message(user_input)
        print("\nAssistant:", response['response'])
