# app name

Web api for app - fondu interview

## How to run the app:

1. Install flask, mongodb and their requiremetns.
2. start mongodb service
3. start flask app

## Available API's:

<details>
<summary>cashbacks</summary>

`POST /cashback`

This endpoint is meant for merchant to post new cashback. Validations:

1. request
2. balance
3. screen
4. db

Example:

```python
import requests

cashback_params = {"cashback_id": 'goodId',
                   "amount": "10000",
                   "merchant_name": "Nike",
                   "customer_name": "goodName",
                   "customer_email": "goodUser@gmail.com"}
url = f'http://127.0.0.1:5000/cashback/'
resp = requests.post(url, params=cashback_params)
```

Returns:

| Status Code | Notes                                         | 
| ----------- | --------------------------------------------- | 
| 200         | on success - "cashback posted, id: <cashback_id>"
| 400         | Missing args - <exception message>
| 403         | "Reserve balance failed <exception message>"
| 403         | <exception message> , released balance status

</details>




####Notes:
1. Didnt check that params themselves are valid except of their type. for example: user can pass goodId with goodName but with badEmail@gmail.com

2. Used `_id` although it means this is a protected attribute. just to make db functionality easier. Can easily (and
should) be changed. 
   
3. Must add more tests.