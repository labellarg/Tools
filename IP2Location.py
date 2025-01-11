import requests

def query_ip2location(ip_address):
    """
    Queries the IP2Location.io API for details about the provided IP address.

    Parameters:
        ip_address (str): The IP address to query.

    Returns:
        None
    """
    api_key = "<ENTER YOUR API KEY HERE>"  # Replace with your IP2Location.io API key
    url = f"https://api.ip2location.io/?key={api_key}&ip={ip_address}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse and display the JSON response
        data = response.json()

        print("\n--- IP2Location.io API Query Results ---")
        for key, value in data.items():
            print(f"{key}: {value}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    while True:
        ip_address = input("Enter the IP address to query (or type 'exit' to quit): ")
        if ip_address.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        query_ip2location(ip_address)
