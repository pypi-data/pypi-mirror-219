simple_ts package

--------------How to install:

pip install simple_ts

---------------How to use:

simple_ts(x, plot=False)

    A simple package for analyze and check time series stationarity.

    Parameters

        x: array_like

        The time series data.

        plot: bool, default False
        if true, plots the decomposition of the time series.

Returns
   -original plot, trend plot, seasonal plot and resid plot for the time series: (optional)
   -summary of Augmented Dickey-Fuller unit root test.
   -summary of Kwiatkowski-Phillips-Schmidt-Shin test for stationarity.
   -best ARIMA model for the time series