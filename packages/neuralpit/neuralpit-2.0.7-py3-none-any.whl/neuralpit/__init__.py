class NeuralPitSDK():

    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    @classmethod
    def init(cls, api_endpoint, api_key):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
            cls._instance.api_endpoint = api_endpoint
            cls._instance.api_key = api_key
        return cls._instance

