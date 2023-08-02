from utils.logger import get_logger

def main():
    logger = get_logger(logger_name="YO")
    for _ in range(10000):
        logger.debug("test")
        logger.info("test")
        logger.warning("test")
        logger.error("test")
        logger.critical("test")

main()

# from utils.color import Color

# print(Color().fore)
