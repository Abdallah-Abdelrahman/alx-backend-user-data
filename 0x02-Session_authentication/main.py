#!/usr/bin/env python3
""" Main 5
"""
#!/usr/bin/env python3
""" Main 0
"""
from api.v1.auth.auth import Auth

a = Auth()
excluded_paths = ["/api/v1/stat*"]
print(a.require_auth("/api/v1/users", excluded_paths))
print(a.require_auth("/api/v1/status", excluded_paths))
print(a.require_auth("/api/v1/stats", excluded_paths))
