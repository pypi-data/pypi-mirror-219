# gw3-sdk-python

This repository contains the Python SDK for Gateway3, an IPFS decentralized gateway. The Gateway3 SDK provides a simple and easy-to-use interface to interact with IPFS, enabling developers to build scalable and distributed applications.

## Getting Started

### Prerequisites

- Python version 3.7 or higher

### Obtain Access Key and Access Secret

To use the Gateway3 SDK, you need to obtain an access key and access secret. You can get these by logging in to the Gateway3 website at https://www.gw3.io/.

### Installation

To install the Gateway3 SDK, use the following command:

```sh
pip install gw3
```

### Usage

Here's a simple example demonstrating the usage of the Gateway3 IPFS Gateway SDK:

```python
from gw3 import GW3Client

client = GW3Client(
    "YOUR-ACCESS-KEY",
    "YOUR-ACCESS-SECRET",
)

data = b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"

# Post the data to the IPFS network, receiving a CID as a result
cid = client.upload(data)
print(f"Data posted to IPFS network, CID is: {cid}")

# Request the gateway to pin the CID data, ensuring its persistence
client.pin(cid)
print("CID data is pinned by the Gateway3")

# Retrieve the data from the IPFS network using the CID
got = client.get_ipfs(cid)
print(f"Data retrieved from IPFS network: {got.decode()}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
