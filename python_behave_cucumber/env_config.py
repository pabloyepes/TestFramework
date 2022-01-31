class EnvironmentConfig(object):

    @staticmethod
    def employees_api():
        return {
            "PROD": "http://127.0.0.1:3000",
            "STAGE": "	http://notworking-127.0.0.1:3000",
            "QA": ""
        }

    @staticmethod
    def amazon():
        return {
            "PROD": "https://www.amazon.com/",
            "STAGE": "",
            "QA": ""
        }
