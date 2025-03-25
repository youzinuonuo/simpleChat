import os

def setup_environment():
    """Setup necessary environment variables for proxy and SSL certificates"""
    # Proxy settings
    os.environ['NO_PROXY'] = 'localhost,127.0.0.1'
    os.environ['no_proxy'] = os.environ['NO_PROXY']  # Set lowercase version as well
    
    # Corporate proxy settings - uncomment and fill if needed
    # os.environ['HTTPS_PROXY'] = ''  # Fill in your company's proxy address
    # os.environ['HTTP_PROXY'] = ''
    
    # SSL certificate path
    # os.environ['SSL_CERT_FILE'] = './InternalCAChain.pem'
    
    # Any other environment variables can be added here
    
    print("Environment variables configured successfully") 