from typing import Dict, Any, Optional
import aiohttp
import json
from autogen_core.tools import FunctionTool
from models.client_information_request import ClientInformationRequest

async def get_client_information(client_information_request: ClientInformationRequest) -> Any:
    """
    Retrieve client information from the API based on ClientInformationRequest parameters.
    Can search by member_number or client_name, calling different services accordingly.
    
    Args:
        client_information_request: A ClientInformationRequest object containing search parameters
            - If member_number is provided, calls the clientInformation service
            - If client_name is provided, calls the clientSearch service
    
    Returns:
        Client information based on the search parameters
    """
    # Determine which service to call based on provided parameters
    if client_information_request.member_number:
        service_url = "http://localhost:5000/customers/customerRelationship/opsWorkstation/v1/private/clientInformation"
        search_param = {'memberNumber': client_information_request.member_number}
    elif client_information_request.client_name:
        service_url = "http://localhost:5000/customers/customerRelationship/opsWorkstation/v1/private/clientSearch"
        search_param = {'clientName': client_information_request.client_name}
    else:
        return {
            "error": "Missing required parameters",
            "message": "Either member_number or client_name must be provided"
        }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
                service_url,
                json=search_param,  # Send as JSON body
                headers={
                    'Content-Type': 'application/json',
                    # Add other required headers here
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {
                        "error": f"API request failed with status {response.status}",
                        "message": await response.text()
                    }
        except Exception as e:
            return {
                "error": "Failed to fetch client information",
                "message": str(e)
            }

# Create FunctionTool instance
get_client_info_tool = FunctionTool(
    func=get_client_information,
    description="""
    Retrieve client information using either member_number or client_name.
    
    Accepts a parameter of type ClientInformationRequest object with these optional fields:
    - member_number: The client's membership number (optional)
    - client_name: The client's full name (optional)
    
    You must provide EITHER member_number OR client_name (at least one must be provided).
    
    The function will:
    - Call clientInformation service if member_number is provided
    - Call clientSearch service if client_name is provided
    
    Examples of information returned:
    - Client's personal details
    - Contact information
    """,
    name="get_client_information",
    strict=True
)


