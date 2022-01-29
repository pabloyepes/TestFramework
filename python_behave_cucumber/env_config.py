class EnvironmentConfig(object):

    @staticmethod
    def employees_api():
        return {
            "PROD": "http://localhost:3000",
            "STAGE": "	http://notworking-localhost:3000",
            "QA": ""
        }

    @staticmethod
    def amazon():
        return {
            "PROD": "https://www.amazon.com/",
            "STAGE": "",
            "QA": ""
        }
