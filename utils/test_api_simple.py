import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.client_information_request import ClientInformationRequest
from utils.client_functions import get_client_information

async def test_simple():
    # Test 1: Using member number
    print("Test 1: Query with member number")
    request1 = ClientInformationRequest(member_number="12345")
    result1 = await get_client_information(request1)
    print(f"Result: {result1}\n")
    
    # Test 2: Using client name
    print("Test 2: Query with client name")
    request2 = ClientInformationRequest(client_name="John Doe")
    result2 = await get_client_information(request2)
    print(f"Result: {result2}\n")

if __name__ == "__main__":
    asyncio.run(test_simple()) 