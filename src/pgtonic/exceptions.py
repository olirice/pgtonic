class PGTonicException(Exception): pass

class LexFailureException(PGTonicException): pass
class ParseFailureException(PGTonicException): pass
