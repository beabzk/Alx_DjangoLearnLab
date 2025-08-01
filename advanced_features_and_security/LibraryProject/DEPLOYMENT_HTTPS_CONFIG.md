# HTTPS Deployment Configuration Guide

## Overview
This document provides comprehensive instructions for configuring HTTPS and secure redirects in production environments for the Django Library Management application.

## Django HTTPS Settings Configuration

### Required Settings in settings.py
```python
# HTTPS Redirect Configuration
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year (31536000 seconds)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Include all subdomains in HSTS policy
SECURE_HSTS_PRELOAD = True  # Allow HSTS preloading

# Secure Cookie Configuration
SESSION_COOKIE_SECURE = True  # Ensure session cookies are only transmitted over HTTPS
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookies are only transmitted over HTTPS

# Security Headers
SECURE_BROWSER_XSS_FILTER = True  # Enable browser's XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking attacks
```

## Web Server Configuration

### Nginx Configuration Example
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect all HTTP traffic to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;
    
    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Django Application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files
    location /static/ {
        alias /path/to/your/static/files/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files
    location /media/ {
        alias /path/to/your/media/files/;
        expires 1y;
        add_header Cache-Control "public";
    }
}
```

### Apache Configuration Example
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # Redirect all HTTP traffic to HTTPS
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    
    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/your/chain.crt
    
    # SSL Security Settings
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305
    SSLHonorCipherOrder off
    SSLSessionTickets off
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"
    
    # Django Application
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On
    ProxyAddHeaders On
</VirtualHost>
```

## SSL Certificate Setup

### Let's Encrypt (Certbot) - Free SSL Certificates
```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal setup
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

### Commercial SSL Certificate Setup
1. Generate a Certificate Signing Request (CSR)
2. Purchase SSL certificate from a trusted CA
3. Install the certificate on your web server
4. Configure your web server to use the certificate

## Environment-Specific Configuration

### Production Settings
```python
# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Proxy Settings (if behind a reverse proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_TZ = True
```

### Development Settings
```python
# settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Disable HTTPS requirements for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

## Testing HTTPS Configuration

### SSL Testing Tools
1. **SSL Labs Test**: https://www.ssllabs.com/ssltest/
2. **Mozilla Observatory**: https://observatory.mozilla.org/
3. **Security Headers**: https://securityheaders.com/

### Manual Testing Commands
```bash
# Test HTTPS redirect
curl -I http://yourdomain.com

# Test HSTS header
curl -I https://yourdomain.com

# Test SSL certificate
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

## Security Checklist

### Pre-Deployment Checklist
- [ ] SSL certificate installed and valid
- [ ] HTTP to HTTPS redirects working
- [ ] HSTS headers configured
- [ ] Secure cookies enabled
- [ ] Security headers implemented
- [ ] SSL/TLS configuration tested
- [ ] Certificate auto-renewal configured

### Post-Deployment Verification
- [ ] SSL Labs test shows A+ rating
- [ ] All pages load over HTTPS
- [ ] No mixed content warnings
- [ ] HSTS preload submission (optional)
- [ ] Security headers verified
- [ ] Performance impact assessed

## Troubleshooting

### Common Issues
1. **Mixed Content**: Ensure all resources (CSS, JS, images) use HTTPS
2. **Certificate Errors**: Verify certificate chain and domain matching
3. **Redirect Loops**: Check proxy configuration and Django settings
4. **Performance Issues**: Optimize SSL/TLS configuration

### Monitoring
- Set up SSL certificate expiration monitoring
- Monitor HTTPS redirect functionality
- Track security header compliance
- Monitor SSL/TLS performance metrics

## Maintenance

### Regular Tasks
- Monitor SSL certificate expiration
- Update SSL/TLS configuration as needed
- Review security headers periodically
- Test HTTPS functionality after updates
- Keep web server and SSL libraries updated
