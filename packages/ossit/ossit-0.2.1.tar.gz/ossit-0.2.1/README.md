# Ossit API Documentation

Ossit is an easy-to-use statistic collecting application that analyzes and displays your data. It follows a three-tier structure:

## Structure

1. **Domains**: The highest level, which produces keys for user authentication. To set your Ossit domain key, import the Ossit library and set the domain key as follows:

2. **Statistic Groups**: This tier allows you to group common statistics, providing better organization and analysis of your data. For example, you could create a group for "Website Traffic" that includes statistics such as page views, unique visitors, and bounce rate.

3. **Statistics**: The lowest level, consisting of individual statistics with a name and value.


## Authentication and Authorization

To authenticate your requests, set your Ossit domain key. You can find your domain key in the Ossit dashboard.

```python
import ossit
ossit.set_domain_key('YOUR_SECRET_KEY')
ossit.set_time_zone('America/Toronto')
```

## Base URL

The base URL for the Ossit API is https://ossit.ca/v1/api. All API responses will be in JSON format.


## Endpoint Structure

Each tier and future objects will follow the same URL path structure. For example, the Statistic Groups resource has the following endpoints:

- POST /statistic-groups: Creates a new statistic group.
- GET /statistic-groups: Retrieves a list of all statistic groups.
- PUT /statistic-groups/:id: Updates the specified statistic group.
- GET /statistic-groups/:id: Retrieves the specified statistic group.

## Examples

Here's an example of creating a new statistic group using the Ossit package:

```python
import ossit

ossit.domain_key = 'YOUR-KEY'
group = ossit.StatisticGroup.create('Automations')
print(group)
```

To retrieve a list of all statistic groups:

```python
groups = ossit.StatisticGroup.list()
print(groups)
```

## Error Handling

If an error occurs, the API will return an error response in the following format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```
Common error codes include:

- 400 Bad Request: The request is malformed or contains invalid data.
- 401 Unauthorized: The request is missing or has an invalid authentication token.
- 403 Forbidden: The authenticated user does not have permission to perform the requested action.
- 404 Not Found: The requested resource could not be found.
- 500 Internal Server Error: An unexpected error occurred on the server side.

## Rate Limiting and Throttling

To ensure fair usage, the Ossit API enforces rate limiting. By default, users are limited to 1000 requests per hour. If you exceed this limit, you will receive a 429 Too Many Requests response.

## Versioning

The current version of the Ossit API is v1. To access different versions of the API (if available), replace the version number in the base URL (e.g., https://ossit.ca/v2/api).

## Changelog

Maintain a changelog of API updates and improvements. Include the version, release date, and a brief summary of changes for each update.

## Support and Contact Information

For API support and feedback, please contact our support team at wesleyh@stratusadv.com