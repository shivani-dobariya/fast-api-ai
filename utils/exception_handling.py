import logging


class ExceptionHandling:
    """
    class to lof exception and send message to user
    """

    def __init__(self, function_name, e):
        self.function_name = function_name
        self.e = e

    def log_exception(self):
        """
        log exception function detail and exception message
        :return: None
        """

        logging.error(msg=f"Exception occur at function: {self.function_name}")
        logging.error(msg=f"exception message :{self.e}")
        return None

    def exception_handling(self, message=True):
        """
        function to call methods to handle exception
        :param message: (str) message to display on web
        :return: None if message else dict contain exception details
        """

        self.log_exception()
        return {'class-method': self.function_name, 'exception_msg': self.e}


class SerializerError:
    """
    class to lof serializer error
    """

    def __init__(self, errors, serializer_name):
        self.serializer_name = serializer_name
        self.errors = errors

    def log_serializer_error(self):
        """
        function to log serializer exception
        :return: None
        """
        logging.error(msg=f'Error at serializer :{self.serializer_name}: {str(self.errors)}')
        return None
