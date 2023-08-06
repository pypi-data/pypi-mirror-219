from ..data_types.user import User
from ..exceptions import *
from .. import globals


class Query:
    def __init__(self, client, debug, queryName, resultType):
        self._client = client
        self._debug = debug
        self._result = None
        self.queryName = queryName
        self.resultType = resultType
        return

    def _getQueryString(self):
        return f"query {self.queryName} {{ {self.queryName} {self.resultType.getQueryString()} }}"

    def _processResult(self):
        if self._debug:
            print(f'DEBUG - processing query result: {self.queryName}')
            print(f'DEBUG - {self._result}')
        if 'errors' in self._result and len(self._result['errors']) > 0:
            print('ERROR - Query encountered error.')
            print(f'ERROR - Response/Error: {self._result}')
            if 'errorType' in self._result['errors'][0] and self._result['errors'][0]['errorType'] == "UnauthorizedException":
                raise UnauthorizedException
            elif 'message' in self._result['errors'][0]['message'] and self._result['errors'][0]['message'] == "Unauthorized":
                raise Unauthorized
            else:
                raise QueryFailed(
                    f"ERROR - Query {self.queryName} failed.", self._result)

        if self._result['data'][self.queryName] is None:
            raise MissingDataInResultException
