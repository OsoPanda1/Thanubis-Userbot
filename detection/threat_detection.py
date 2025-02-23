import re
from typing import Dict
from utils.rate_limiter import RateLimiter

# Clase de detección de amenazas
class ThreatDetector:
    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.pattern_weights = {
            r'(?i)t\.me/joinchat': 5,
            r'(?i)(?:crypto|eth|btc).*(?:invest|trade)': 8,
            r'(?i)(?:hack|crack).*(?:account|password)': 9,
            r'(?i)(?:sell|buy).*(?:followers|likes)': 4
        }
        self.model = self._load_threat_model()

    def _load_threat_model(self):
        pass

    async def analyze_message(self, message: str, user_id: int) -> Dict[str, float]:
        if not await self.rate_limiter.check(user_id):
            return {'threat_level': 1.0, 'reason': 'rate_limit'}
        ml_score = await self._get_ml_prediction(message)
        pattern_score = self._check_patterns(message)
        return {
            'threat_level': max(ml_score, pattern_score),
            'ml_confidence': ml_score,
            'pattern_match': pattern_score > 0.5
        }

    async def _get_ml_prediction(self, message: str) -> float:
        return 0.0

    def _check_patterns(self, message: str) -> float:
        score = 0.0
        for pattern, weight in self.pattern_weights.items():
            if re.search(pattern, message):
                score += weight / 10.0
        return min(score, 1.0)
