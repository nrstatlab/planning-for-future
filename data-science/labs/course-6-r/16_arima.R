# =====================================================================
# Run with R 4.3.3 (Rscript --vanilla). What it prints, and the plots it
# draws, are on the lab page, and tools/data-science/run_r_equivalents.py
# runs it again. (Until October 2026 R could not be installed where these
# labs are checked, so this file was desk-checked only; every number in its
# comments has since been checked against R's own output.)
# =====================================================================
# Experiment 16: Time series forecasting with ARIMA
# Python equivalent: python/16_arima.py (implements decomposition, differencing,
# ACF and PACF from first principles, on a series of its own)

library(forecast); library(tseries)

# Step 1: Load and plot the series, and take logs
data(AirPassengers)          # the classic monthly series, 1949-1960
ap <- AirPassengers

# --- 1. LOOK AT IT FIRST ---
plot(ap, main = "Monthly airline passengers")
# The seasonal swing GROWS with the level -> MULTIPLICATIVE, so take logs.
lap <- log(ap)
plot(lap)                    # now the swing is roughly constant -> additive

# --- 2. DECOMPOSE ---
# Step 2: Decompose it
decomp <- decompose(ap, type = "multiplicative")
plot(decomp)                 # observed / trend / seasonal / random
stl(lap, s.window = "periodic")   # more robust; works on the log series

# --- 3. TEST FOR STATIONARITY ---
# Step 3: Test for stationarity
adf.test(ap)
#   ADF:  H0 = NON-stationary (unit root)
#   large p  -> FAIL to reject -> the series is NOT stationary
#   Here, though, p is below 0.01: adf.test() allows for a linear trend, and
#   around that trend this series is stationary. [Corrected: this said the
#   raw series gives a large p.]
kpss.test(ap)
#   KPSS: H0 = STATIONARY  -- the OPPOSITE null.
#   Reading one test's p-value as though it were the other's gives exactly
#   the wrong conclusion. Write the null down before interpreting.
#   Here KPSS rejects (p below 0.01): the level is not constant. With ADF,
#   that makes the series trend-stationary; differencing deals with both.

ndiffs(lap)      # how many ordinary differences are needed
nsdiffs(lap)     # how many SEASONAL differences

# --- 4. DIFFERENCE ---
# Step 4: Difference it
d1 <- diff(lap)              # removes the trend
d12 <- diff(d1, lag = 12)    # removes the 12-month seasonality
adf.test(d12)                # now small p -> stationary

# --- 5. IDENTIFY THE ORDERS ---
# Step 5: Read the ACF and PACF
acf(ap,  main = "ACF of the RAW series")
# Slow decay -- the trend swamps everything -- with the seasonality only a
# ripple on it: the ACF falls to 0.66 at lag 8 and rises again to 0.76 at
# lag 12. This is why you difference first. [Corrected: this said the decay
# is monotonic and the seasonality invisible. That is true of the Python
# version's series, not of this one.]

acf(d12,  main = "ACF after differencing")     # q, from where it CUTS OFF
pacf(d12, main = "PACF after differencing")    # p, from where it CUTS OFF
#   ACF tails off, PACF cuts off after lag p  -> AR(p)
#   ACF cuts off after lag q, PACF tails off  -> MA(q)
#   Mnemonic: PACF gives p, ACF gives q.

# --- 6. FIT ---
# Step 6: Fit the model
fit <- auto.arima(lap)       # searches (p,d,q)(P,D,Q)[12] by AIC
summary(fit)

# --- 7. CHECK THE RESIDUALS -- the step students skip ---
# Step 7: Check the residuals
checkresiduals(fit)
# If the model is adequate its residuals are WHITE NOISE: no autocorrelation
# left, roughly normal, constant variance. Structure remaining in the
# residuals is signal the model failed to capture.
#
# Ljung-Box: H0 = residuals are independent.
# Here you WANT a LARGE p-value -- the opposite of most tests you have met.

# --- 8. FORECAST ---
# Step 8: Forecast two years ahead
fc <- forecast(fit, h = 24)
plot(fc)
exp(fc$mean)                 # back-transform from the log scale
accuracy(fit)                # ME, RMSE, MAE, MAPE

# MAPE is unit-free and therefore easy to compare across series, but it
# breaks down when actual values are near zero.
