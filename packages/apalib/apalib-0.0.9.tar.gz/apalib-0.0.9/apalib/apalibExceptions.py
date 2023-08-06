# class ExceptionWrapper(Exception):
#     def __init__(self, message):
#         self.message = message
#
#     def __str__(self):
#         return self.message


class MutationError(Exception):
    # When a constant variable is mutated
    def __init__(self):
        self.message = 'Attempt to mutate a protected variable'


class NoFetchError(Exception):
    # Used when a fetched pdb file is required but not provided
    def __init__(self):
        self.message = 'No fetched protein. Use method Fetch(PDB_CODE) to fetch a protein.\n'
        return self.message

    def __str__(self):
        return self.message


class BadInternet(Exception):
    def __init__(self):
        self.message = 'Poor or no internet connection. Some functionality may be lost\n\t' \
                       r'Connection to http://www.google.com timeout or failure'

    def __str__(self):
        return self.message


class BadKwarg(Exception):
    def __init__(self, accepted):
        self.message = f'Bad parameter provided. Accepted parameters are as follows: {accepted}'

    def __str__(self):
        return self.message


class BadMethodException(Exception):
    pass

class NegativeProbabilityException(Exception):
    pass

class ProbabilityOverflowException(Exception):
    pass

class PolarProbabilityOverflowException(Exception):
    pass

class ChargedProbabilityOverflowException(Exception):
    pass

class ChargeLengthMismatchException(Exception):
    pass

class BadBatchSizeException(Exception):
    pass

class InvalidURLException(Exception):
    pass

class BadJSONException(Exception):
    pass

class InvalidPresetDistributionException(Exception):
    pass

class BadMaxAttemptsException(Exception):
    pass

class ImpossibleSettingsException(Exception):
    pass
