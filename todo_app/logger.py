import logging

def create_blueprint_logger(blueprint_name):
    logger = logging.getLogger(blueprint_name)
    logger.setLevel(logging.DEBUG)
    # Configure the logger as needed (e.g., set level, formatter, and handlers)
    # Example:
    handler = logging.FileHandler("todo.log")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s | %(module)s] %(message)s" , datefmt = "%B %d, %Y %H:%M:%S %Z")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger