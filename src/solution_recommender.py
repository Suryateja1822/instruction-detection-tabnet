"""
Solution Recommender for TabNet-IDS
Provides recommended solutions and mitigation steps for detected threats
"""

import json
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import numpy as np

@dataclass
class ThreatSolution:
    """Data class to hold threat solution information"""
    name: str
    description: str
    severity: str
    solutions: List[str]
    mitigation_steps: List[str]

class SolutionRecommender:
    """Recommends solutions for detected security threats"""
    
    def __init__(self, solutions_file: str = 'solutions_db.json'):
        """Initialize with path to solutions database"""
        self.solutions_file = solutions_file
        self.solutions_db = self._load_solutions()
        
    def _load_solutions(self) -> Dict[str, Any]:
        """Load solutions from JSON file or use default solutions if file not found"""
        try:
            if os.path.exists(self.solutions_file):
                with open(self.solutions_file, 'r') as f:
                    return json.load(f)
            else:
                # Default solutions if file not found
                return {
                    "sql_injection": {
                        "name": "SQL Injection",
                        "description": "An attacker can execute malicious SQL statements that control a web application's database.",
                        "severity": "Critical",
                        "solutions": [
                            "Use parameterized queries (prepared statements)",
                            "Implement input validation and sanitization",
                            "Use ORM frameworks with built-in protection",
                            "Apply the principle of least privilege for database accounts"
                        ],
                        "mitigation_steps": [
                            "Audit all database queries for dynamic SQL",
                            "Implement Web Application Firewall (WAF) rules",
                            "Enable database logging for suspicious queries"
                        ]
                    },
                    "ddos": {
                        "name": "DDoS Attack",
                        "description": "Distributed Denial of Service attack overwhelms the target with traffic from multiple sources.",
                        "severity": "High",
                        "solutions": [
                            "Implement rate limiting and request throttling",
                            "Use a Content Delivery Network (CDN)",
                            "Deploy DDoS protection services (e.g., Cloudflare, AWS Shield)",
                            "Configure network infrastructure with anti-DDoS measures"
                        ],
                        "mitigation_steps": [
                            "Monitor network traffic for unusual patterns",
                            "Set up automated alerts for traffic spikes",
                            "Create an incident response plan for DDoS scenarios"
                        ]
                    },
                    "xss": {
                        "name": "Cross-Site Scripting (XSS)",
                        "description": "Malicious scripts are injected into trusted websites and executed in the victim's browser.",
                        "severity": "High",
                        "solutions": [
                            "Implement Content Security Policy (CSP) headers",
                            "Encode data on output, not just input",
                            "Use template engines that automatically escape XSS by default",
                            "Set HttpOnly flag on cookies"
                        ],
                        "mitigation_steps": [
                            "Conduct regular security audits and penetration testing",
                            "Use automated vulnerability scanners",
                            "Implement XSS filters in web application firewalls"
                        ]
                    },
                    "brute_force": {
                        "name": "Brute Force Attack",
                        "description": "Attackers attempt to gain access by systematically trying all possible combinations of credentials.",
                        "severity": "Medium",
                        "solutions": [
                            "Implement account lockout after failed attempts",
                            "Enforce strong password policies",
                            "Enable multi-factor authentication (MFA)",
                            "Use CAPTCHA for login forms"
                        ],
                        "mitigation_steps": [
                            "Monitor failed login attempts",
                            "Implement IP-based rate limiting",
                            "Set up alerts for multiple failed login attempts"
                        ]
                    },
                    "insider_threat": {
                        "name": "Insider Threat",
                        "description": "Malicious activities performed by individuals with legitimate access to systems and data.",
                        "severity": "High",
                        "solutions": [
                            "Implement least privilege access controls",
                            "Monitor user activity and access patterns",
                            "Conduct regular access reviews",
                            "Implement data loss prevention (DLP) solutions"
                        ],
                        "mitigation_steps": [
                            "Establish clear security policies and procedures",
                            "Provide security awareness training",
                            "Implement user behavior analytics"
                        ]
                    }
                }
        except Exception as e:
            print(f"Error loading solutions database: {e}")
            return {}
    
    def get_solution(self, threat_type: str) -> Optional[ThreatSolution]:
        """
        Get solution for a specific threat type
        
        Args:
            threat_type: Type of threat (e.g., 'sql_injection', 'ddos')
            
        Returns:
            ThreatSolution object if found, None otherwise
        """
        threat_type = threat_type.lower().replace(' ', '_')
        if threat_type in self.solutions_db:
            data = self.solutions_db[threat_type]
            return ThreatSolution(
                name=data['name'],
                description=data['description'],
                severity=data['severity'],
                solutions=data['solutions'],
                mitigation_steps=data['mitigation_steps']
            )
        return None
    
    def get_all_threats(self) -> List[Dict[str, str]]:
        """Get list of all available threat types"""
        return [
            {
                'id': threat_id,
                'name': data['name'],
                'severity': data['severity']
            }
            for threat_id, data in self.solutions_db.items()
        ]
    
    def find_similar_threats(self, query: str, top_n: int = 3) -> List[Dict[str, Any]]:
        """
        Find threats similar to the query string
        
        Args:
            query: Search query
            top_n: Number of results to return
            
        Returns:
            List of matching threats with similarity scores
        """
        query = query.lower()
        results = []
        
        for threat_id, data in self.solutions_db.items():
            # Simple text matching for now - could be enhanced with embeddings
            text = f"{data['name']} {data['description']} {' '.join(data['solutions'])}"
            text = text.lower()
            
            # Simple word overlap scoring
            query_terms = set(query.split())
            text_terms = set(text.split())
            score = len(query_terms.intersection(text_terms)) / len(query_terms) if query_terms else 0
            
            if score > 0.1:  # Threshold to filter out very poor matches
                results.append({
                    'id': threat_id,
                    'name': data['name'],
                    'description': data['description'],
                    'severity': data['severity'],
                    'score': score
                })
        
        # Sort by score and return top N
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_n]


# Example usage
if __name__ == "__main__":
    recommender = SolutionRecommender()
    
    # Example: Get solution for a specific threat
    threat = "sql injection"
    solution = recommender.get_solution(threat)
    
    if solution:
        print(f"\nSolution for {solution.name} ({solution.severity}):")
        print(f"Description: {solution.description}")
        print("\nRecommended Solutions:")
        for i, sol in enumerate(solution.solutions, 1):
            print(f"{i}. {sol}")
        
        print("\nMitigation Steps:")
        for i, step in enumerate(solution.mitigation_steps, 1):
            print(f"{i}. {step}")
    else:
        print(f"No solution found for: {threat}")
