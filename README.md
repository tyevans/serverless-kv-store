# Simple Serverless Key-Value Store


## Usage Examples:

Creating entries:

	$ curl -X POST https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1 --data '{ "key": "sports", "value": ["baseball", "soccer", "football"]}'

  		{"key": "sports", "value": ["baseball", "soccer", "football"]}

	$ curl -X POST https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1 --data '{ "key": "food", "value": ["apple", "orange", "pizza"]}'
  		
  		{"key": "food", "value": ["apple", "orange", "pizza"]}

Retrieving entries:

	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/sports
  		
  		{"key": "sports", "value": ["soccer", "football", "baseball"]}


	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/food
  		
  		{"key": "food", "value": ["apple", "orange", "pizza"]}

Retrieving all entries:

	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1
  		
  		{"entries": [{"key": "sports", "value": ["football", "soccer", "baseball"]}, {"key": "food", "value": ["pizza", "apple", "orange"]}]}


Updating an Entry:

	$ curl -X PUT https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/food --data '{"key": "food", "value": ["burger", "fries"]}'
  		
  		{"key": "food", "value": ["fries", "burger"]}

	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/food
  		
  		{"key": "food", "value": ["fries", "burger"]}

Deleting an Entry:

	$ curl -X DELETE https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/food


	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1/food
  		
  		{"error_message": "Entry Not Found"}

	$ curl https://XXXXXXXXXX.execute-api.us-west-1.amazonaws.com/dev/kvstore/v1
  		
  		{"entries": [{"key": "sports", "value": ["baseball", "soccer", "football"]}]}
