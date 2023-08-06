# Cmotions Nnect
cmo_nnect is a Python library created by [Cmotions](https://cmotions.nl/). This library aims to ease the interaction with different API's of software packages. Examples include Microsoft Dynamics, Exact Online, AFAS Profit etc. You only need the right authentication credentials, and the target endpoints of the source/destination API to start interacting!

From our experience with integrating data from a variety of software packages we decided to publish our connectors to ease the use of the API's with Python. We encourage collaboration to increase the number of connectors and improvements of existing connectors!

The library always returns a Pandas dataframe by default.

## Installation
Install cmo_nnect using pip
```bash
pip install cmo-nnect
```

## Usage
Choose the [connector](#Available-connectors) from the list, and import the connector by using the reference name. For example for AFAS Profit the reference name is afasprofit:
```bash
from cmo_nnect import afasprofit
```
From the [connector usage documentation](#Connector-usage) determine the authentication requirements, for example for AFAS Profit we need a token, a company-id, and an optional environment name. We can then initialize a client:
```bash
# define authentication credentials
token = "<token><version>1</version><data>54740093832496081845474abcdefghijklmnopq740093832496081841234127</data></token>"
company_id = 12345
environment = "development"

# set up a client to ease interaction
client = afasprofit(token,company_id)
```
We are now able to start interacting with the API. To extract data you can use the format client.get_data(). In the documentation of the specific connector you can see what is expected for the specific method. For example for AFAS Profit we need to provide a get_connector name, and optional parameters:
```bash
# define parameters
params = {"skip": "-1", "take": "-1"}

# extract data from the software package
contacts = client.get_data("get_contacts", params)
```
## Available connectors
- [AFAS Profit](https://help.afas.nl/help/NL/SE/App_Cnr_Rest_Api.htm) (afasprofit)
- [Nmbrs](https://support.nmbrs.nl/hc/nl/articles/205903718-Visma-Nmbrs-API-for-developers-) (nmbrs)
- [Mautic](https://developer.mautic.org/#rest-api) (mautic)

## Connector usage
### AFAS Profit
**Authentication**<br>
To authenticate with AFAS Profit you need:
- A profit token (e.g. "<token><version>1</version><data>54740093832496081845474abcdefghijklmnopq740093832496081841234127</data></token>")
- A company ID (e.g. 12345)
Optionally:
- An environment, defaults to production (e.g. "test")

**Interaction**<br>
For each interaction you can provide optional parameters in a dictionary (e.g. {"skip": "-1", "take": "-1"}).

**Extracting data**<br>
To get data, you need:
- A get_connector name of a get connector which is [set-up in AFAS profit](https://help.afas.nl/help/NL/SE/App_Apps_Custom_Add.htm) (e.g. "get_contacts")

**Inserting data**<br>
T.B.A.

**Updating data**<br>
T.B.A.

**Deleting data**<br>
T.B.A.

### Mautic
**Authentication**<br>
To authenticate with Mautic you need:
- A company name, you can find the company name in the url of your mautic instance (e.g. cmotions)
- A client id, the client id will be generated when the mautic administrator enables the API. Check the [Mautic documentation](https://developer.mautic.org/#authorization) for setting this up.
- A client secret, the client secret will be generated when the mautic administrator enables the API. Check the [Mautic documentation](https://developer.mautic.org/#authorization) for setting this up.

**Interaction**<br>
For each interaction you can provide optional parameters in a dictionary (e.g. "limit=10&minimal=true").

**Extracting data**<br>
To get data, you need:
- A entity name, check the [Mautic documentation](https://developer.mautic.org/#endpoints) for the available entities (e.g. "campaigns")

**Inserting data**<br>
T.B.A.

**Updating data**<br>
T.B.A.

**Deleting data**<br>
T.B.A.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Contributors
Thijs van der Velden, Koen Leijsten<br>
[Contact us](mailto:info@cmotions.nl)