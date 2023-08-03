from utils.logger import get_logger

def main():
    logger = get_logger(logger_name="YO", log_dir="./logs")
    for i in range(10000):
        msg = str(i)
        logger.debug(msg)
        logger.info(msg)
        logger.warning(msg)
        logger.error(msg)
        logger.critical(msg)

main()
