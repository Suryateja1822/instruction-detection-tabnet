"""
AI Chat Assistant for TabNet-IDS
Provides conversational interface for threat analysis and solutions
"""

import random
from typing import Dict, List, Optional
try:
    from solution_recommender import SolutionRecommender
except ImportError:
    # Fallback if solution_recommender is not available
    SolutionRecommender = None

class ChatAssistant:
    """AI Chat Assistant for security threat analysis"""
    
    def __init__(self, solutions_file: str = 'solutions_db.json'):
        """Initialize with solutions database"""
        if SolutionRecommender is not None:
            self.recommender = SolutionRecommender(solutions_file)
        else:
            self.recommender = None
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
        if self.recommender is None:
            return f"I don't have access to the threat database right now, but I can tell you that '{threat_type}' is a security concern that requires proper monitoring and prevention strategies."
            
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
        
        # Check for multiple questions in the message
        if self._has_multiple_questions(message):
            return self._handle_multiple_questions(message)
        
        # Simple keyword-based response generation
        message_lower = message.lower()
        
        # Check for greetings
        greeting_words = ["hi", "hello", "hey", "greetings", "hi there", "good morning", "good afternoon"]
        if any(word in message_lower for word in greeting_words):
            response = f"{self.get_greeting()} {self.get_security_tip()}"
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "greeting"}
        
        # Check for help requests
        if any(word in message_lower for word in ["help", "what can you do", "how can you help"]):
            response = self.get_help_response()
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "help"}
        
        # Check for solution/mitigation requests
        solution_keywords = ["how to prevent", "how to stop", "solution", "mitigate", "fix", "protect against", "secure against", "how to protect"]
        if any(word in message_lower for word in solution_keywords):
            return self._handle_solution_request(message)
        
        # Check for explanation requests
        explanation_keywords = ["what is", "explain", "tell me about", "describe", "define", "tell me about", "what does"]
        if any(word in message_lower for word in explanation_keywords):
            return self._handle_threat_explanation(message)
        
        # Check for security best practices
        if any(word in message_lower for word in ["best practice", "security tips", "how to secure"]):
            response = "🔒 **Security Best Practices:**\n\n"
            response += "1. Keep all systems updated with latest patches\n"
            response += "2. Use strong, unique passwords and MFA\n"
            response += "3. Implement principle of least privilege\n"
            response += "4. Regular security audits and monitoring\n"
            response += "5. Employee security training\n"
            response += "6. Backup and disaster recovery planning\n"
            response += "7. Network segmentation and firewalls\n"
            response += "8. Incident response planning\n\n"
            response += f"{self.get_security_tip()}"
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "best_practices"}
        
        # Default response
        return self._generate_default_response(message)
    
    def _handle_solution_request(self, message: str) -> Dict:
        """Handle requests for threat solutions"""
        message_lower = message.lower()
        
        # Specific threat solutions
        if "ddos" in message_lower:
            response = "🚨 **DDoS Attack Prevention:**\n\n"
            response += "1. **Rate Limiting**: Implement rate limiting on your servers\n"
            response += "2. **CDN Protection**: Use Content Delivery Networks with DDoS protection\n"
            response += "3. **Firewall Rules**: Configure firewalls to block suspicious traffic\n"
            response += "4. **Load Balancing**: Distribute traffic across multiple servers\n"
            response += "5. **Monitoring**: Set up real-time traffic monitoring and alerts\n"
            response += "6. **ISP Coordination**: Work with your ISP for upstream filtering\n\n"
            response += "💡 **Quick Tip**: Cloud services like AWS Shield and Cloudflare offer excellent DDoS protection."
            
        elif "sql injection" in message_lower or "sql" in message_lower:
            response = "💉 **SQL Injection Prevention:**\n\n"
            response += "1. **Parameterized Queries**: Use prepared statements instead of string concatenation\n"
            response += "2. **Input Validation**: Validate and sanitize all user inputs\n"
            response += "3. **ORM Frameworks**: Use Object-Relational Mapping frameworks\n"
            response += "4. **Least Privilege**: Limit database user permissions\n"
            response += "5. **Web Application Firewall**: Deploy WAF with SQL injection rules\n"
            response += "6. **Regular Updates**: Keep database and application software updated\n\n"
            response += "💡 **Quick Tip**: Always assume user input is malicious and validate accordingly."
            
        elif "phishing" in message_lower:
            response = "🎣 **Phishing Attack Prevention:**\n\n"
            response += "1. **Email Filtering**: Implement advanced email filtering systems\n"
            response += "2. **User Training**: Regular security awareness training\n"
            response += "3. **Multi-Factor Authentication**: Enable MFA on all accounts\n"
            response += "4. **Email Verification**: Verify suspicious emails before clicking\n"
            response += "5. **URL Scanning**: Use tools to scan links before visiting\n"
            response += "6. **Report Mechanisms**: Easy ways for users to report phishing\n\n"
            response += "💡 **Quick Tip**: When in doubt, verify requests through a separate communication channel."
            
        elif "brute force" in message_lower:
            response = "🔨 **Brute Force Attack Prevention:**\n\n"
            response += "1. **Account Lockout**: Lock accounts after multiple failed attempts\n"
            response += "2. **Strong Passwords**: Enforce complex password requirements\n"
            response += "3. **Multi-Factor Authentication**: Add MFA as mandatory requirement\n"
            response += "4. **Rate Limiting**: Limit login attempts per time period\n"
            response += "5. **CAPTCHA**: Implement CAPTCHA on login forms\n"
            response += "6. **Monitoring**: Monitor for unusual login patterns\n\n"
            response += "💡 **Quick Tip**: Account lockout policies should be balanced to avoid denial of service."
            
        elif self.recommender is None:
            response = "I don't have access to my threat database right now, but here are some general security best practices:\n\n"
            response += "1. Keep all systems and software up to date\n"
            response += "2. Use strong, unique passwords and enable MFA\n"
            response += "3. Regularly back up important data\n"
            response += "4. Use a firewall and keep it properly configured\n"
            response += "5. Educate users about phishing and social engineering"
        else:
            # Try to find a matching threat in the knowledge base
            similar_threats = self.recommender.find_similar_threats(message)
            
            if similar_threats and similar_threats[0]['score'] > 0.3:  # Threshold for good match
                threat_id = similar_threats[0]['id']
                solution = self.recommender.get_solution(threat_id)
                response = f"🛡️ **Solution for {threat_id}:**\n\n{solution}"
            else:
                response = "I don't have specific information about that threat. Here are general security practices:\n\n"
                response += "1. Keep systems updated and patched\n"
                response += "2. Use strong authentication methods\n"
                response += "3. Monitor network activity regularly\n"
                response += "4. Educate users about security best practices"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "type": "solution"}
    
    def _handle_threat_explanation(self, message: str) -> Dict:
        """Handle requests for threat explanations"""
        message_lower = message.lower()
        
        # Specific threat explanations
        if "ddos" in message_lower:
            response = "🚨 **DDoS (Distributed Denial of Service) Attack Explanation:**\n\n"
            response += "**What it is:** A DDoS attack overwhelms a target server or network with massive traffic from multiple sources, making it unavailable to legitimate users.\n\n"
            response += "**How it works:**\n"
            response += "• Attackers use botnets (networks of compromised computers)\n"
            response += "• Simultaneously send requests to overwhelm server resources\n"
            response += "• Target bandwidth, CPU, memory, or application resources\n\n"
            response += "**Common types:**\n"
            response += "• Volume-based attacks (UDP floods, ICMP floods)\n"
            response += "• Protocol attacks (SYN floods, fragmented packets)\n"
            response += "• Application layer attacks (HTTP floods, slowloris)\n\n"
            response += "**Impact:** Service disruption, revenue loss, reputation damage\n\n"
            response += "💡 **Detection**: Monitor for unusual traffic spikes and connection patterns."
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "threat_explanation"}
            
        elif "sql injection" in message_lower or "sql" in message_lower:
            response = "💉 **SQL Injection Attack Explanation:**\n\n"
            response += "**What it is:** SQL injection is a code injection technique that exploits vulnerabilities in an application's database layer.\n\n"
            response += "**How it works:**\n"
            response += "• Attacker inserts malicious SQL statements into input fields\n"
            response += "• Application executes these statements on the database\n"
            response += "• Can bypass authentication, steal data, or modify database\n\n"
            response += "**Common examples:**\n"
            response += "• Authentication bypass: ' OR '1'='1\n"
            response += "• Data extraction: UNION SELECT statements\n"
            response += "• Database modification: DROP TABLE commands\n\n"
            response += "**Impact:** Data theft, data corruption, system compromise\n\n"
            response += "💡 **Prevention**: Use parameterized queries and input validation."
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "threat_explanation"}
            
        elif "phishing" in message_lower:
            response = "🎣 **Phishing Attack Explanation:**\n\n"
            response += "**What it is:** Phishing is a social engineering attack that tricks users into revealing sensitive information.\n\n"
            response += "**How it works:**\n"
            response += "• Attackers send deceptive emails or messages\n"
            response += "• Impersonate legitimate organizations or individuals\n"
            response += "• Create fake websites or login pages\n"
            response += "• Steal credentials, financial information, or personal data\n\n"
            response += "**Common types:**\n"
            response += "• Email phishing: Fake emails from banks, services, etc.\n"
            response += "• Spear phishing: Targeted attacks on specific individuals\n"
            response += "• Whaling: Attacks targeting high-level executives\n"
            response += "• Smishing: SMS-based phishing attacks\n\n"
            response += "**Impact:** Credential theft, financial loss, identity theft\n\n"
            response += "💡 **Protection**: Verify sender identity and never click suspicious links."
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "threat_explanation"}
            
        elif "malware" in message_lower or "ransomware" in message_lower:
            response = "🦠 **Malware & Ransomware Explanation:**\n\n"
            response += "**What it is:** Malicious software designed to damage, disrupt, or gain unauthorized access to computer systems.\n\n"
            response += "**Types of Malware:**\n"
            response += "• **Viruses**: Self-replicating programs that attach to other files\n"
            response += "• **Worms**: Self-replicating programs that spread across networks\n"
            response += "• **Trojans**: Disguised as legitimate software\n"
            response += "• **Spyware**: Collects user information without consent\n"
            response += "• **Ransomware**: Encrypts files and demands payment\n\n"
            response += "**How infections occur:**\n"
            response += "• Email attachments and malicious links\n"
            response += "• Software downloads from untrusted sources\n"
            response += "• Exploitation of software vulnerabilities\n"
            response += "• Removable media (USB drives, etc.)\n\n"
            response += "**Impact:** Data loss, system damage, financial extortion\n\n"
            response += "💡 **Protection**: Use antivirus software and keep systems updated."
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "threat_explanation"}
            
        else:
            # If no specific threat matched, provide general threat list
            response = "I don't have access to my threat database right now. "
            response += "Here are some common security threats you might be interested in:\n\n"
            response += "• SQL Injection\n"
            response += "• Cross-Site Scripting (XSS)\n"
            response += "• DDoS Attacks\n"
            response += "• Malware & Ransomware\n"
            response += "• Phishing Attacks\n\n"
            response += "You can ask me about any of these for more details."
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return {"response": response, "type": "general_info"}
        
        # Try to find a matching threat in the knowledge base
        similar_threats = None
        if self.recommender is not None:
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
    
    def _has_multiple_questions(self, message: str) -> bool:
        """
        Check if the message contains multiple questions
        """
        question_indicators = ['?', 'what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe', 'tell me']
        message_lower = message.lower()
        
        # Count question indicators
        question_count = sum(1 for indicator in question_indicators if indicator in message_lower)
        
        # Check for multiple sentences with question marks
        question_mark_count = message.count('?')
        
        # Check for common question patterns
        multiple_question_patterns = [
            ' and ', ' also ', ' plus ', ' additionally ', ' furthermore ',
            ' what about ', ' how about ', ' can you also '
        ]
        
        pattern_matches = any(pattern in message_lower for pattern in multiple_question_patterns)
        
        return question_count >= 2 or question_mark_count >= 2 or pattern_matches
    
    def _handle_multiple_questions(self, message: str) -> Dict:
        """
        Handle multiple questions in a single message
        """
        # Split the message into individual questions
        questions = self._split_into_questions(message)
        
        response = "🤖 **I'll help you with all your questions:**\n\n"
        
        for i, question in enumerate(questions, 1):
            if question.strip():
                response += f"**Question {i}:** {question.strip()}\n"
                
                # Generate response for each question
                question_response = self._generate_response_for_question(question.strip())
                response += f"**Answer {i}:** {question_response}\n\n"
        
        # Add a helpful closing
        response += "💡 **Tip:** You can ask me about any security topic, and I'll provide detailed explanations and solutions!"
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return {"response": response, "type": "multiple_questions"}
    
    def _split_into_questions(self, message: str) -> List[str]:
        """
        Split a message into individual questions
        """
        # Common question separators
        separators = ['?', '. ', '! ', ' and ', ' also ', ' plus ', ' additionally ']
        
        questions = [message]
        
        for separator in separators:
            new_questions = []
            for question in questions:
                new_questions.extend(question.split(separator))
            questions = new_questions
        
        # Filter out empty strings and clean up
        questions = [q.strip() for q in questions if q.strip()]
        
        # Remove trailing punctuation from questions
        questions = [q.rstrip('?!.,') for q in questions]
        
        return questions[:5]  # Limit to 5 questions to avoid very long responses
    
    def _generate_response_for_question(self, question: str) -> str:
        """
        Generate a response for a single question
        """
        question_lower = question.lower()
        
        # Check for specific threat explanations
        if "ddos" in question_lower:
            return "🚨 **DDoS (Distributed Denial of Service)** is an attack that overwhelms servers with massive traffic, making them unavailable to legitimate users. Prevention includes rate limiting, CDN protection, and firewalls."
        
        elif "sql injection" in question_lower or "sql" in question_lower:
            return "💉 **SQL Injection** is a code injection technique that exploits database vulnerabilities. Prevention includes parameterized queries, input validation, and using ORMs."
        
        elif "phishing" in question_lower:
            return "🎣 **Phishing** is a social engineering attack that tricks users into revealing sensitive information. Prevention includes email filtering, user training, and MFA."
        
        elif "malware" in question_lower or "ransomware" in question_lower:
            return "🦠 **Malware/Ransomware** is malicious software that damages systems or encrypts files for ransom. Prevention includes antivirus software, system updates, and backups."
        
        # Check for solution requests
        elif any(word in question_lower for word in ["how to prevent", "how to stop", "solution", "mitigate", "fix"]):
            return "🛡️ For prevention, I recommend: 1) Keep systems updated, 2) Use strong authentication, 3) Implement firewalls, 4) Regular monitoring, 5) User training."
        
        # Check for explanation requests
        elif any(word in question_lower for word in ["what is", "explain", "tell me about", "describe"]):
            return "🔍 I can explain various security threats including DDoS attacks, SQL injection, phishing, malware, and more. Each has specific prevention strategies."
        
        # Check for best practices
        elif any(word in question_lower for word in ["best practice", "security tips", "how to secure"]):
            return "🔒 **Security Best Practices:** 1) Keep systems updated, 2) Use strong passwords & MFA, 3) Implement least privilege, 4) Regular audits, 5) Employee training, 6) Backup planning, 7) Network segmentation, 8) Incident response."
        
        # Default response
        else:
            return "🤔 I can help with security topics like threat analysis, prevention strategies, and best practices. Could you be more specific about what you'd like to know?"


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
