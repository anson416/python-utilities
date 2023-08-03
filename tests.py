from utils.logger import get_logger

def main():
    logger = get_logger()
    for i in range(1):
        msg = str(i)
        logger.debug(msg)
        logger.info(msg)
        logger.warning(msg)
        logger.error(msg)
        logger.critical(msg)

main()
