# Phase-2---Forecasting_Module
The Granger-Casuality test is performed on each pair of attributes.The output is p value. If p < 0.05 then the feature pair has bidirectional relationship. ADF- Stationary test  is applied to each feature values in the historical database. The stationary test chosen is coint-johansen test. In the Johansen test, we check whether lambda has a zero eigenvalue. When all the eigenvalues are zero, that would mean that the series are not cointegrated, whereas when some of the eigenvalues contain negative values, it would imply that a linear combination of the time series can be created, which would result in stationarity.Stationary series is easier for statistical models to predict effectively and precisely. In Lag Selection The data is modelled for multiple orders and the lag value is order offering minimum value of Akaike Information Criterion(AIC), Bayesian Information Criterion(BIC), Hannah-Quinn Information Criterion(HQIC). Finally, the VAR model is implemented using the obtained lag value. The forecasting of the spatial data is done and the accuracy is measured using minmax accuracy parameter.
![fm](https://user-images.githubusercontent.com/62131312/175823598-6493947a-9ef6-4c62-903e-589e2aa7b4ca.png)
