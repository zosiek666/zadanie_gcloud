if __name__ == '__main__':
    from wsgiref import simple_server
    from zadanie.settigns import API
    from zadanie.logger import logger

    logger.info('Starting app')
    httpd = simple_server.make_server('127.0.0.1', 8000, API)
    logger.info('App started')
    httpd.serve_forever()
