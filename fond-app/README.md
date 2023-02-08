# app name

Web api for app

## Available API's:

<details>
<summary>cashbacks</summary>

`GET /cashbacks`

This endpoint is meant for getting all cashbacks from db

Example:

```python
import requests

requests.post(url='/cashbacks')
```

Returns:

| Status Code | Data/Message | Notes | 
| ----------- | -------------| ----- | 
| 200         | {'cashbacks': all cashbacks from db}|
| 500         | failed to execute action, server error

</details>

<details>
<summary>Post Cashbacks</summary>

`POST /cashbacks`

This endpoint is meant for posting a new cashback

Example:

```python
import requests

requests.post(url='/kill_app', params={'cashback_id': '100',
                                       'type': 'created'})
```

Options:

| Option Name  | Required | Notes |
| ------------ | ---------| ------|
| cashback_id  | Yes      | cashback_id
| type     | Yes      | type of event

Returns:

| Status Code | Data/Message | Notes | 
| ----------- | -------------| ----- | 
| 200         | {'msg': 'success'}
| 400         | in case of missing \ not valid params_
| 500         | failed to execute action, server error

</details>