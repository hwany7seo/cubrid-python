import logging

def setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("cubrid_driver.log"),
                                  logging.StreamHandler()])

    logger = logging.getLogger(__name__)
    return logger
