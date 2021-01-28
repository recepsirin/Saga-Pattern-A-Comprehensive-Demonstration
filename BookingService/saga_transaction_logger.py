import logging


def write_transaction(mesage):
    logging.basicConfig(filename='saga.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning(mesage)
