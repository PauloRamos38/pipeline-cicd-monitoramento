#!/usr/bin/env python3
"""
Gunicorn configuration file for production deployment
Handles logging, worker configuration, and error handling
"""

import os
import multiprocessing
import logging

# =======================
# Server Socket Configuration
# =======================
bind = "0.0.0.0:5000"
backlog = 2048
workers = max(2, multiprocessing.cpu_count())
worker_class = "sync"
worker_connections = 1000
timeout = 60
keepalive = 2

# =======================
# Logging Configuration
# =======================
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"  # Change to "debug" for development

# Log format - professional and parseable
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# =======================
# Process Naming and Application
# =======================
proc_name = "pipeline-cicd-api"
default_proc_name = "pipeline-cicd-api"

# =======================
# Server Mechanics
# =======================
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# =======================
# SSL Configuration (if needed)
# =======================
# keyfile = None
# certfile = None
# ssl_version = 3
# cert_reqs = 0
# ca_certs = None

# =======================
# Security
# =======================
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# =======================
# Monitoring and Hooks
# =======================
def when_ready(server):
    """Called when the server is ready to accept connections"""
    logger = logging.getLogger(__name__)
    logger.info(f"✅ Server started with {workers} workers")
    logger.info(f"🚀 Listening on {bind}")
    logger.info(f"🔍 Application: {proc_name}")

def on_exit(server):
    """Called when the server is exiting"""
    logger = logging.getLogger(__name__)
    logger.info("⛔ Shutting down server gracefully...")

# =======================
# Environment Variables
# =======================
environment = {
    "ENVIRONMENT": os.getenv("ENVIRONMENT", "production"),
    "LOG_LEVEL": os.getenv("LOG_LEVEL", "info"),
}

# =======================
# Development/Production Switch
# =======================
if os.getenv("ENVIRONMENT") == "development":
    loglevel = "debug"
    reload = True
    reload_extra_files = ["/app"]
