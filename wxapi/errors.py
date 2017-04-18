# encoding: utf-8


class WXError(Exception):
    """基础错误类"""

    errcode = None
    errmsg = None

    def __init__(self, code, msg):
        self.errcode = code
        self.errcode = msg

    def __unicode__(self):
        return u'<{cls}:{code}> {msg}'.format(cls=self.__class__.__name__, code=self.errcode,
                                              msg=self.errmsg)

    def __str__(self):
        return u'<{cls}:{code}> {msg}'.format(cls=self.__class__.__name__, code=self.errcode,
                                              msg=self.errmsg)


class HttpError(WXError):
    """http请求异常"""

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return u'HTTP请求错误: {error}'.format(error=self.error)

    def __str__(self):
        return 'HTTP请求错误: {error}'.format(error=self.error)


class BusinessError(WXError):
    """业务异常"""

    def __init__(self, error):
        super(BusinessError, self).__init__(error.get('errcode'), error.get('errmsg'))
