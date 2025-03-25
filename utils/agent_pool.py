from typing import Dict, Optional
import time
from collections import OrderedDict
from agents.plan_agent import PlanAgent
from utils.api_key_utils import get_api_key
class AgentPool:
    def __init__(self, max_size: int = 1000, timeout_minutes: int = 30):
        self.max_size = max_size
        self.timeout_minutes = timeout_minutes
        self.user_agents: Dict[str, tuple[PlanAgent, float]] = OrderedDict()
        self.api_key = get_api_key()
    
    def _cleanup_expired(self):
        """清理超时的agent"""
        current_time = time.time()
        expired_users = [
            user_id for user_id, (_, last_access) in self.user_agents.items()
            if (current_time - last_access) / 60 > self.timeout_minutes
        ]
        for user_id in expired_users:
            del self.user_agents[user_id]
    
    def _check_api_key(self):
        """检查API key是否变化"""
        current_api_key = get_api_key()
        if current_api_key != self.api_key:
            self.user_agents.clear()
            self.api_key = current_api_key
    
    def get_agent(self, user_id: str) -> PlanAgent:
        """获取用户专属agent"""
        self._cleanup_expired()  # 清理过期agent
        self._check_api_key()    # 检查API key
        
        current_time = time.time()
        
        # 如果用户已有agent，更新访问时间并返回
        if user_id in self.user_agents:
            agent, _ = self.user_agents[user_id]
            self.user_agents.move_to_end(user_id)  # 移动到最新
            self.user_agents[user_id] = (agent, current_time)
            return agent
            
        # 如果池已满，移除最早的agent
        if len(self.user_agents) >= self.max_size:
            self.user_agents.popitem(last=False)  # 移除最早的
            
        # 创建新agent
        new_agent = PlanAgent()
        self.user_agents[user_id] = (new_agent, current_time)
        return new_agent 