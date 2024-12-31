import secrets

# Generate a 32-character secret key
secret_key = secrets.token_urlsafe(32)  # URL-safe for use in headers or URLs
print(secret_key)