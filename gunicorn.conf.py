bind = "127.0.0.1:8000" # Choose a free port, it doesn't have to be 5000
workers = 4 # Adjust this based on your VM resources; a good starting point is 2-4 times the number of CPU cores. 
timeout = 120 # Adjust as needed

# Logging configuration
accesslog = "-" # Log to standard output
errorlog = "-"  # Log errors to standard output
access_log_format = '%(t)s %(h)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
