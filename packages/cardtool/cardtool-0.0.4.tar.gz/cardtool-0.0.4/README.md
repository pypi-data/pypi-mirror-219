# Cardtool
[![PyPI version](https://badge.fury.io/py/cardtool.svg)](https://badge.fury.io/py/cardtool)
[![codecov](https://codecov.io/gh/d4n13l-4lf4/cardtool/branch/master/graph/badge.svg?token=1CUDZLNZ9S)](https://codecov.io/gh/d4n13l-4lf4/cardtool)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A card data generation tool with DUKPT key derivation.

### Installation

---
You should have python 3.9 or later to run this tool. So, please be sure you have the python interpreter installed before trying this setup guide.

Create a virtual environment:
```bash
python3 -m venv .env
```
Activate the virtual environment:
```bash
source .env/bin/activate
```
For testing purposes with alpha or beta versions, install this tool from [TestPyPI](https://test.pypi.org/):
```bash
pip3 install -U --extra-index-url https://test.pypi.org/simple/ cardtool==x.y.z[ab]N
```
Otherwise, install this tool from [PyPI](https://pypi.org/):
```bash
pip3 install cardtool
```

Finally, use it:
```bash
cardtool --help
```

### Commands reference

---
#### Key decryption
A command to decrypt a TR-31 key block.
```bash
cardtool decrypt-key -kbpk <your_key_block_protection_key> -kcv <key_check_value> YOUR_KEY_BLOCK

```

#### Card data generation
A command to generate a file with encrypted card data using DUKPT key derivation.
```bash 
cardtool gen-card -cfg <path_to_config_yaml> -fmt json|yaml path_to_dump_card_data.[json|yaml]
```

### Card data generation configuration file

---
The following is a reference configuration file for the gen-card command.
```yaml
!CardConfig
# current version of command
version: "0.1" 
# terminal information
terminal:
  !Terminal
  # terminal country
  country: MEX
# encryption keys
key:
  # keys used to encrypt both data and pin
  shared:
    !Key
    # base derivation key
    bdk: 0123456789ABCDEFFEDCBA9876543210
    # key serial number
    ksn: FFFF4545450000100002
# transaction information
transaction:
  !Transaction
  # type of transaction
  type: charge
  # transaction amount
  amount: 10.2
  # another transaction amount, e.g., cashback amount
  other_amount: 10.23
  # transaction currency
  currency: USD
  # date of transaction with DDMMYY format
  date: "220125"
# array of cards to generate
cards:
  - !Card
    # card label, useful as an identifier for this card
    label: "Test"
    # primary account number 16-19 digits
    pan: "5477820000001234"
    # card pin 4-6 digits
    pin: "1234"
    # card brand (Visa, Mastercard, Carnet)
    brand: "Mastercard"
    # cardholder name
    cardholder_name: Test 1
    # card expiry month
    expiry_month: "12"
    # card expiry year
    expiry_year: "24"
    # card service code
    service_code: "201"
    # card sequence number
    sequence_number: 1

```