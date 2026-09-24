# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 16: Time series forecasting with ARIMA
# Python equivalent: python/16_arima.py (implements decomposition, differencing,
# ACF and PACF from first principles -- statsmodels is not installed there)

library(forecast); library(tseries)

data(AirPassengers)          # the classic monthly series, 1949-1960
ap <- AirPassengers

# --- 1. LOOK AT IT FIRST ---
plot(ap, main = "Monthly airline passengers")
# The seasonal swing GROWS with the level -> MULTIPLICATIVE, so take logs.
lap <- log(ap)
plot(lap)                    # now the swing is roughly constant -> additive

# --- 2. DECOMPOSE ---
decomp <- decompose(ap, type = "multiplicative")
plot(decomp)                 # observed / trend / seasonal / random
stl(lap, s.window = "periodic")   # more robust; works on the log series

# --- 3. TEST FOR STATIONARITY ---
adf.test(ap)
#   ADF:  H0 = NON-stationary (unit root)
#   large p  -> FAIL to reject -> the series is NOT stationary
kpss.test(ap)
#   KPSS: H0 = STATIONARY  -- the OPPOSITE null.
#   Reading one test's p-value as though it were the other's gives exactly
#   the wrong conclusion. Write the null down before interpreting.

ndiffs(lap)      # how many ordinary differences are needed
nsdiffs(lap)     # how many SEASONAL differences

# --- 4. DIFFERENCE ---
d1 <- diff(lap)              # removes the trend
d12 <- diff(d1, lag = 12)    # removes the 12-month seasonality
adf.test(d12)                # now small p -> stationary

# --- 5. IDENTIFY THE ORDERS ---
acf(ap,  main = "ACF of the RAW series")
# Slow monotonic decay and nothing else -- the trend swamps everything, and
# the seasonality is INVISIBLE here. This is why you difference first.

acf(d12,  main = "ACF after differencing")     # q, from where it CUTS OFF
pacf(d12, main = "PACF after differencing")    # p, from where it CUTS OFF
#   ACF tails off, PACF cuts off after lag p  -> AR(p)
#   ACF cuts off after lag q, PACF tails off  -> MA(q)
#   Mnemonic: PACF gives p, ACF gives q.

# --- 6. FIT ---
fit <- auto.arima(lap)       # searches (p,d,q)(P,D,Q)[12] by AIC
summary(fit)

# --- 7. CHECK THE RESIDUALS -- the step students skip ---
checkresiduals(fit)
# If the model is adequate its residuals are WHITE NOISE: no autocorrelation
# left, roughly normal, constant variance. Structure remaining in the
# residuals is signal the model failed to capture.
#
# Ljung-Box: H0 = residuals are independent.
# Here you WANT a LARGE p-value -- the opposite of most tests you have met.

# --- 8. FORECAST ---
fc <- forecast(fit, h = 24)
plot(fc)
exp(fc$mean)                 # back-transform from the log scale
accuracy(fit)                # ME, RMSE, MAE, MAPE

# MAPE is unit-free and therefore easy to compare across series, but it
# breaks down when actual values are near zero.
