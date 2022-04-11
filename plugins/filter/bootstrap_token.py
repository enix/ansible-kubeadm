import base64

try:
    import arrow
    HAS_ARROW = True
except ImportError:
    HAS_ARROW = False

class FilterModule(object):

    def filters(self):
        return {
            'bootstrap_token_valid': self.bootstrap_token_valid
        }


    def bootstrap_token_valid(self, token_list):
        if not HAS_ARROW:
            raise ValueError('You need to install python-arrow on deployer host')
        return list(self._token_filter(token_list))

    def _token_filter(self, token_list, now=None):
        """Return valid token in a token list

        >>> f = FilterModule()
        >>> list(f._token_filter([{'data': {'expiration': 'MjAxNy0wMy0xMFQwMzoyMjoxMVoK'}}], '2017-03-10T02:22:11Z'))
        [{'data': {'expiration': 'MjAxNy0wMy0xMFQwMzoyMjoxMVoK'}}]
        >>> f.bootstrap_token_valid([{'data': {'expiration': 'MjAxNy0wMy0xMFQwMzoyMjoxMVoK'}}])
        []
        """
        if now:
            threshold = arrow.get(now)
        else:
            threshold = arrow.utcnow()
        for token in token_list:
            if arrow.get(base64.b64decode(token['data']['expiration']).decode('utf-8')) >= threshold:
                yield token


if __name__ == '__main__':
    import doctest
    doctest.testmod()
