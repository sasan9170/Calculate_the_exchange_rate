BASE_PATH = "http://data.fixer.io/api/latest?access_key="
ACCESS_KEY = "93d73b265d14c596018dd8f9e9a0df3e"

url = BASE_PATH + ACCESS_KEY


rules = {
    'archive': True,
    'sms': {
        'enable': True,
        'preferred': ['BTC', 'IRR', "IQD", "USD", "CAD", "AED"],
    },
    'notification': {
        'enable': True,
        'receiver': '',
        'preferred': {
            'BTC': {'min': 3.4857483e-05, 'max': 3.4857493e-05},
            'IRR': {'min': 46120.340307, 'max': 46130.340307},
        }
    }
}
MAILGUN_APIKEY = "passwor"
KAVENEGAR_API_KEY ="password"
