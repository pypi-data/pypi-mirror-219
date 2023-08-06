# SHRT - Shortened URL service

An MVP to serve shortened URLs

## Usage

Serve using `uvicorn` by running

```shell
uvicorn --host=0.0.0.0 shrt.web:app
```

Manage URLs from the CLI

```shell
# List URLs
shrt url list
# Create a random short path
shrt url add https://x59.us
# Create a custom short path
shrt url add https://x59.co --path x59
# Create a new short path, even if the target exists in the DB
shrt url add https://x59.co --create-new
# Get details for a given short path
shrt url get x59
# Delete a given short path
shrt url delete x59
```
