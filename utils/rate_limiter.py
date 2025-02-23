import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 5, period: int = 60):
        self.max_requests = max_requests
        self.period = timedelta(seconds=period)
        self.requests = defaultdict(list)

    async def check(self, user_id: int) -> bool:
        now = datetime.utcnow()
        if user_id in self.requests:
            self.requests[user_id] = [req for req in self.requests[user_id] if now - req < self.period]

        if len(self.requests[user_id]) >= self.max_requests:
            return False

        self.requests[user_id].append(now)
        return True
