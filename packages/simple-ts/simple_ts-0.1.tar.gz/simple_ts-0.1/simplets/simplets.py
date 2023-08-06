from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import kpss
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
from pmdarima import auto_arima

def simple_ts(ts, plot=False):
    result_adf = adfuller(ts)
    result_kpss = kpss(ts)
    if plot:
        result = seasonal_decompose(ts, model='additive', period=12)

# Obter as componentes da decomposição
        trend = result.trend
        seasonal = result.seasonal
        residuals = result.resid

# Plotar as componentes da decomposição
        plt.figure(figsize=(10, 8))
        plt.subplot(411)
        plt.plot(serie_ar, label='Original')
        plt.legend(loc='upper left')

        plt.subplot(412)
        plt.plot(trend, label='Tendência')
        plt.legend(loc='upper left')

        plt.subplot(413)
        plt.plot(seasonal, label='Sazonalidade')
        plt.legend(loc='upper left')

        plt.subplot(414)
        plt.plot(residuals, label='Resíduos')
        plt.legend(loc='upper left')

        plt.tight_layout()
        plt.show()
        
    if result_adf[1] < 0.01:
        print("------------ Dickey-Fuller Test Summary --------------------")
        print('The Dickey-Fuller test statistic:', result_adf[0])
        print('p-value:', result_adf[1])
        print('lags used:', result_adf[2])
        print('The critical values:', result_adf[4])
        print('Conclusion: The series is stationary because p-value = {} < 0.01 (99% level of confidence)'.format(result_adf[1]))
    else:
        print("------------ Dickey-Fuller Test Summary --------------------")
        print('The Dickey-Fuller test statistic:', result_adf[0])
        print('p-value:', result_adf[1])
        print('lags used:', result_adf[2])
        print('The critical values:', result_adf[4])
        print('Conclusion: The series is not stationary because p-value = {} > 0.01 (99% level of confidence)'.format(result_adf[1]))

    print("\n")
    print("-------------Kwiatkowski–Phillips–Schmidt–Shin (KPSS) Test Summary--------------")
    print('The KPSS test statistic:', result_kpss[0])
    print('p-value:', result_kpss[1])
    print('lags:', result_kpss[2])
    print('The critical values:', result_kpss[3])

    if result_adf[1] < 0.01:
        conclusion = 'The series is stationary because t-test = {} < {} (The critical value for 99% level of confidence)'.format(result_kpss[0], result_kpss[3]['1%'])
    else:
        conclusion = 'The series is not stationary because t-test = {} > {} (The critical value for 99% level of confidence)'.format(result_kpss[0], result_kpss[3]['1%'])

    print('Conclusion:', conclusion)
    print("\n")
    print("Optimal order for an ARIMA model by auto-ARIMA:")
    arima_model = auto_arima(ts, seasonal=False, trace=True)