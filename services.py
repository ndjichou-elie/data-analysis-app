from alpha_vantage.timeseries import TimeSeries

class FinancialAPIService:
    def __init__(self, api_key):
        self.ts = TimeSeries(key=api_key, output_format='pandas')

    def get_stock_data(self, symbol):
        try:
            data, meta_data = self.ts.get_intraday(symbol=symbol, interval='1min', outputsize='full')
            return data
        except Exception as e:
            return {'error': str(e)}
