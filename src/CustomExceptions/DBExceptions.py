class QueryExecuteError(Exception):
    def __init__(self, text, error):
        super(QueryExecuteError, self).__init__(f"{text} {error}")