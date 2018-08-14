class JWTConfig:
    JWT_SECRET = "JWT-API-SECRET-HERE"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKENS = ['access', 'refresh']
