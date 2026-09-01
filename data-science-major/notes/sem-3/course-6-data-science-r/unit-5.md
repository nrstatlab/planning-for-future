# Unit 5 — Advanced Topics in Data Science with R

**Syllabus topics:** Introduction to Time Series Analysis in R (ARIMA basics)
— concept of time series (trend, seasonality, noise), time series objects in R
(`ts`, `zoo`, `xts`), plotting and decomposing time series, stationarity and
differencing, autocorrelation and partial autocorrelation (ACF/PACF), AR, MA,
ARIMA model basics, forecasting using the `forecast` package. Creating
interactive visualizations with `plotly` — converting `ggplot2` plots to
interactive plots, animations and sliders. R Shiny: building interactive web
applications — introduction to the Shiny framework, UI and server functions,
reactive expressions and reactivity, input and output widgets, layouts and
dashboard design.

---

> ## ⚠ This unit contains three separate subjects
>
> **Time series analysis**, **interactive visualisation** and **web application
> development** share nothing beyond being done in R. Any one of them is
> normally a course. Compare Unit 2, which covers variables and loops.
>
> **If you are short of time, prioritise Part A (time series).** It carries the
> most exam weight, it is mathematically substantial, and it feeds directly into
> the Semester VI elective *Time Series Analysis and Forecasting*. Parts B and C
> are applied skills you can learn from documentation later.
>
> See [`SYLLABUS-REVIEW.md`](../../../SYLLABUS-REVIEW.md) finding **D12**.

This file is split into three independent parts. Study them separately.

---

# Part A — Time Series Analysis

## A.1 What makes a time series different

### 🎯 The big idea

In a time series the **order of the observations is the information**. Shuffle
a normal dataset and nothing is lost; shuffle a time series and you have
destroyed it.

### 📖 The story

You have monthly sales for three years. A standard regression treats each month
as an independent observation — but December's sales are not independent of
November's, and last December tells you far more about this December than last
July does. The dependence between neighbouring observations is exactly what a
time series model exploits and what ordinary regression throws away.

### The four components

| Component | Meaning | Example |
|---|---|---|
| **Trend (T)** | Long-run direction | Sales rising year on year |
| **Seasonality (S)** | A repeating pattern of **fixed** period | Higher sales every December |
| **Cyclic (C)** | Repeating but of **variable** period | Business cycles, 5–10 years |
| **Irregular / Noise (I)** | What is left | Random fluctuation |

**Seasonality vs cyclic** is a favourite two-mark question: seasonality has a
**fixed, known** period (12 months, 7 days); cycles do not.

### Decomposition models

> **Additive:  Y = T + S + I** — use when the seasonal swing is roughly
> constant in size
>
> **Multiplicative:  Y = T × S × I** — use when the seasonal swing grows with
> the level of the series

Plot the series first. If the peaks get taller as the series rises, it is
multiplicative — and taking logs converts it to additive, since
log(T × S × I) = log T + log S + log I.

```r
data(AirPassengers)
plot(AirPassengers)                          # classic multiplicative example
decompose(AirPassengers, type = "multiplicative")
stl(log(AirPassengers), s.window = "periodic")   # more robust
```

## A.2 Time series objects in R

| Class | Package | Use |
|---|---|---|
| `ts` | base | Regular, evenly spaced (monthly, quarterly, yearly) |
| `zoo` | zoo | **Irregular** spacing, arbitrary index |
| `xts` | xts | Extensible time series, built on zoo; strong for financial data |

```r
sales <- ts(c(112, 118, 132, 129, 121, 135),
            start = c(2024, 1), frequency = 12)   # monthly from Jan 2024

start(sales); end(sales); frequency(sales)
window(sales, start = c(2024, 3), end = c(2024, 5))
```

**`frequency` is observations per cycle, not per year:** 12 = monthly,
4 = quarterly, 7 = daily-with-weekly-seasonality, 1 = annual. Getting this wrong
silently disables all seasonal modelling — the commonest error in this part of
the course.

## A.3 Stationarity

### 🎯 The big idea

A **stationary** series has statistical properties that do not change over time
— constant mean, constant variance, and a covariance that depends only on the
lag between two points, not on where they sit.

### 📖 Why it matters

ARIMA models assume stationarity. A series with a trend has a mean that keeps
moving, so "the mean" is not a fixed quantity to estimate — and a model fitted to
it will forecast badly. Almost every real series is non-stationary, so making it
stationary is the first modelling step, not an optional check.

### Testing for it

```r
library(tseries)
adf.test(series)      # Augmented Dickey-Fuller
kpss.test(series)     # KPSS
```

> **ADF:  H₀ = the series is NON-stationary (has a unit root)**
> → a small p-value means **reject H₀**, so the series **is** stationary
>
> **KPSS: H₀ = the series IS stationary**
> → a small p-value means **reject H₀**, so the series is **not** stationary

**The two tests have opposite null hypotheses.** Reading ADF's p-value as though
it were KPSS's gives exactly the wrong conclusion, and it is a standard exam
trap. Write the null down before interpreting either.

### Differencing

> **First difference:  Y′ₜ = Yₜ − Yₜ₋₁** — removes a linear trend
>
> **Second difference:  Y″ₜ = Y′ₜ − Y′ₜ₋₁** — removes a quadratic trend
>
> **Seasonal difference:  Yₜ − Yₜ₋ₛ** — removes seasonality of period s

```r
diff(series)                    # first difference -- d = 1
diff(series, differences = 2)   # second difference -- d = 2
diff(series, lag = 12)          # seasonal difference -- D = 1
ndiffs(series); nsdiffs(series) # how many are needed
```

**Rarely difference more than twice.** Over-differencing adds artificial
negative autocorrelation and makes the model worse, not better. If `ndiffs()`
says 1, use 1.

## A.4 ACF and PACF

| Function | Measures |
|---|---|
| **ACF** — autocorrelation | Correlation of Yₜ with Yₜ₋ₖ, **including** everything in between |
| **PACF** — partial autocorrelation | Correlation of Yₜ with Yₜ₋ₖ **after removing** the effect of the intermediate lags |

```r
acf(series); pacf(series)
```

### Reading them to identify the model

| Pattern | Model | Order |
|---|---|---|
| ACF **tails off**, PACF **cuts off** after lag p | **AR(p)** | p from PACF |
| ACF **cuts off** after lag q, PACF **tails off** | **MA(q)** | q from ACF |
| Both tail off | **ARMA(p,q)** | Use AIC to choose |
| ACF decays very slowly | Non-stationary | **Difference it first** |

**The mnemonic:** *PACF for AR, ACF for MA.* PACF gives **p**, ACF gives **q**.
Both alphabetically inverted, which is oddly the easiest way to remember it.

## A.5 AR, MA and ARIMA

> **AR(p) — Autoregressive:** Yₜ = c + φ₁Yₜ₋₁ + … + φₚYₜ₋ₚ + εₜ
> *The series regressed on its own past values.*
>
> **MA(q) — Moving Average:** Yₜ = c + εₜ + θ₁εₜ₋₁ + … + θ_qεₜ₋q
> *The series regressed on past forecast errors.*
>
> **ARIMA(p, d, q):** AR + differencing + MA combined

| Parameter | Is | Found from |
|---|---|---|
| **p** | AR order | PACF cut-off |
| **d** | Degree of differencing | `ndiffs()` / ADF test |
| **q** | MA order | ACF cut-off |

**SARIMA(p,d,q)(P,D,Q)[s]** adds the seasonal counterparts, where s is the
period.

### Special cases worth naming

| Model | Is |
|---|---|
| ARIMA(0,0,0) | White noise |
| ARIMA(0,1,0) | A random walk |
| ARIMA(0,1,0) with drift | A random walk with trend |
| ARIMA(p,0,0) | Pure AR |
| ARIMA(0,0,q) | Pure MA |
| ARIMA(0,1,1) | Simple exponential smoothing |

### Fitting and forecasting

```r
library(forecast)

fit <- auto.arima(series)          # searches (p,d,q) by AIC
summary(fit); checkresiduals(fit)

fc <- forecast(fit, h = 12)        # 12 periods ahead
plot(fc); accuracy(fit)
```

### 💡 The residual check is the part students skip

```r
checkresiduals(fit)
```

**If the model is adequate, its residuals should be white noise** — no
autocorrelation left, roughly normal, constant variance. Any structure remaining
in the residuals is signal the model failed to capture, and the fix is a
different model, not a bigger forecast horizon.

The **Ljung-Box test** formalises it: H₀ = residuals are independently
distributed. A **large** p-value is what you want here — the opposite of most
tests you have met, and worth stating carefully in an exam.

### Accuracy measures

| Measure | Formula | Note |
|---|---|---|
| **ME** | mean error | Shows bias |
| **RMSE** | √(mean squared error) | Penalises large errors; same units as the data |
| **MAE** | mean absolute error | Robust to outliers |
| **MAPE** | mean absolute percentage error | Unit-free; **fails when actuals are near zero** |

---

# Part B — Interactive Visualisation with plotly

## B.1 From ggplot2 to interactive, in one line

```r
library(plotly)

p <- ggplot(students, aes(x = hours, y = marks, colour = section)) +
       geom_point()

ggplotly(p)                # done -- hover, zoom, pan all work
```

**`ggplotly()` is the whole trick for most purposes.** Any `ggplot2` plot from
Unit 3 becomes interactive without rewriting it.

## B.2 Native plotly

```r
plot_ly(students, x = ~hours, y = ~marks, color = ~section,
        type = "scatter", mode = "markers",
        text = ~paste("Name:", name, "<br>Marks:", marks),
        hoverinfo = "text") %>%
  layout(title = "Marks against study hours",
         xaxis = list(title = "Hours"),
         yaxis = list(title = "Marks"))
```

**Note the `~`.** plotly uses formula notation to refer to columns; `x = hours`
without it looks for a variable called `hours` in your environment and fails.

**Layers chain with `%>%`, not `+`** — the reverse of `ggplot2`. Mixing the two
is the most common plotly error.

## B.3 Animations and sliders

```r
plot_ly(gapminder, x = ~gdpPercap, y = ~lifeExp,
        size = ~pop, color = ~continent,
        frame = ~year,                       # <- this creates the animation
        type = "scatter", mode = "markers") %>%
  layout(xaxis = list(type = "log")) %>%
  animation_opts(frame = 1000, transition = 500, redraw = FALSE)
```

**`frame = ~year` is all an animation needs** — plotly adds the play button and
slider automatically. This reproduces the famous Hans Rosling Gapminder chart in
about six lines.

For a manual slider, use `layout(sliders = list(...))` or `rangeslider()` for
time series.

## B.4 When interactivity helps and when it does not

| Use interactive | Use static |
|---|---|
| Exploration, dashboards, many points | Printed reports, exams, papers |
| Hovering reveals per-point detail | The message is a single clear comparison |
| Users need to zoom into dense regions | The reader has one takeaway |

Interactivity is not automatically better. A static chart with a clear title
often communicates more than an interactive one the reader must explore.

---

# Part C — R Shiny

## C.1 What Shiny is

Shiny turns an R script into a **web application** — with no HTML, CSS or
JavaScript required. You will meet those properly in Course 7; Shiny lets you
skip them.

## C.2 The two halves of every Shiny app

```r
library(shiny)

ui <- fluidPage(
  titlePanel("Student Marks Explorer"),
  sidebarLayout(
    sidebarPanel(
      selectInput("section", "Choose a section:",
                  choices = c("A", "B", "C")),
      sliderInput("minmarks", "Minimum marks:",
                  min = 0, max = 100, value = 40)
    ),
    mainPanel(
      plotOutput("marksPlot"),
      tableOutput("summaryTable")
    )
  )
)

server <- function(input, output, session) {
  filtered <- reactive({
    students %>%
      filter(section == input$section, marks >= input$minmarks)
  })

  output$marksPlot <- renderPlot({
    ggplot(filtered(), aes(x = marks)) + geom_histogram(bins = 10)
  })

  output$summaryTable <- renderTable({
    filtered() %>% summarise(n = n(), avg = mean(marks))
  })
}

shinyApp(ui = ui, server = server)
```

| Half | Responsibility |
|---|---|
| **`ui`** | What the app looks like — inputs and output *placeholders* |
| **`server`** | What the app does — reads `input$*`, writes `output$*` |

## C.3 Reactivity — the concept the whole framework rests on

### 🎯 The big idea

You never write "when the dropdown changes, redraw the plot". You declare that
the plot **depends on** the dropdown, and Shiny works out what to update.

### The three reactive constructs

| Construct | Purpose |
|---|---|
| `reactive({ })` | A **value** that recomputes when its inputs change; call it as `f()` |
| `observe({ })` | A **side effect** — no return value |
| `eventReactive(input$go, { })` | Recompute only when a specific input fires |
| `isolate({ })` | Read a value **without** creating a dependency |

**Two rules that cause most Shiny bugs:**

1. **Call a reactive with parentheses.** `filtered()`, not `filtered`. Without
   them you are referring to the function, not its value.
2. **`input$x` can only be read inside a reactive context** — a `reactive()`,
   `observe()` or `render*()`. Reading it at the top level of `server` throws
   "operation not allowed without an active reactive context".

### 💡 Why the `reactive()` in the example matters

`filtered` is used by **both** outputs. Written as a `reactive()`, the filtering
runs **once** per change and both outputs share the result. Copy the `filter()`
call into each `render*()` instead and it runs twice — wasteful here, and
genuinely slow on real data.

**Factor shared computation into a `reactive()`.** That is the single most
useful Shiny habit.

## C.4 Widgets

| Input | Widget |
|---|---|
| `textInput` | Free text |
| `numericInput` | A number |
| `sliderInput` | A slider; `value = c(a,b)` gives a range |
| `selectInput` | Dropdown; `multiple = TRUE` for many |
| `checkboxInput` / `checkboxGroupInput` | Tick boxes |
| `radioButtons` | One of several |
| `dateInput` / `dateRangeInput` | Dates |
| `fileInput` | Upload — used in lab experiment 18 |
| `actionButton` | Trigger, paired with `eventReactive` |

| Output | Render function |
|---|---|
| `plotOutput` | `renderPlot` |
| `tableOutput` / `dataTableOutput` | `renderTable` / `renderDataTable` |
| `textOutput` / `verbatimTextOutput` | `renderText` / `renderPrint` |
| `uiOutput` | `renderUI` — build UI dynamically |
| `plotlyOutput` | `renderPlotly` — Part B inside Shiny |

**Every output ID must match:** `plotOutput("marksPlot")` in the UI pairs with
`output$marksPlot` in the server. A typo produces a blank panel and no error
message — check the spelling first when something does not appear.

## C.5 Layout and deployment

```r
fluidPage()  sidebarLayout()  fluidRow() / column(width = 6)
tabsetPanel(tabPanel("Plot", ...), tabPanel("Data", ...))
navbarPage()
```

`shinydashboard` and `bs4Dash` give proper dashboard chrome. Bootstrap's grid is
12 columns wide, so `column(6)` is half the page.

**Deployment:** shinyapps.io (free tier), Shiny Server, or Posit Connect.

---

## 📝 Practice problems

### Problem 1

A monthly sales series shows a rising trend and a December peak that grows
larger each year. Which decomposition, and what transformation would help?

**Solution.**

**Multiplicative**, because the seasonal swing grows with the level — that is
the definition. An additive model assumes a constant-sized seasonal effect and
would systematically under-fit later years.

**Take logs.** Since Y = T × S × I, log Y = log T + log S + log I, so the
multiplicative structure becomes additive and any additive method applies.
Back-transform forecasts with `exp()`.

```r
fit <- auto.arima(log(sales))
fc  <- forecast(fit, h = 12)
exp(fc$mean)        # back to the original units
```

*(Note that `exp()` of the mean forecast on the log scale gives the **median**
on the original scale, not the mean — a subtlety worth mentioning for a full
answer.)*

### Problem 2

The ACF of a series decays slowly and the ADF test gives p = 0.42. What do you
conclude, and what next?

**Solution.**

**Both signs point the same way: the series is non-stationary.**

- A slowly decaying ACF is the classic signature of a trend.
- ADF's null hypothesis is *non-stationary*. p = 0.42 > 0.05, so we **fail to
  reject** H₀ — we cannot conclude stationarity.

**Next: difference it.**

```r
d1 <- diff(series)
adf.test(d1)        # expect a small p-value now
acf(d1); pacf(d1)   # now read p and q from these
ndiffs(series)      # confirms how many differences are needed
```

Re-test after differencing. If it is now stationary, **d = 1** in your
ARIMA(p,d,q). Read p from the PACF cut-off and q from the ACF cut-off of the
*differenced* series.

**Careful:** had this been a KPSS test, p = 0.42 would mean the **opposite** —
KPSS's null is stationarity, so a large p-value there supports it. Always write
down which null you are testing.

### Problem 3

A Shiny app has a dropdown and two outputs, both filtering the same data. Show
the wrong and right way to structure the server.

**Solution.**

**Wrong — the filter runs twice on every change:**

```r
server <- function(input, output) {
  output$plot <- renderPlot({
    d <- students %>% filter(section == input$section)   # filter #1
    ggplot(d, aes(marks)) + geom_histogram()
  })
  output$table <- renderTable({
    d <- students %>% filter(section == input$section)   # filter #2 -- duplicated
    summarise(d, n = n(), avg = mean(marks))
  })
}
```

**Right — one reactive, shared:**

```r
server <- function(input, output) {
  filtered <- reactive({
    students %>% filter(section == input$section)
  })

  output$plot <- renderPlot({
    ggplot(filtered(), aes(marks)) + geom_histogram()    # note the ()
  })
  output$table <- renderTable({
    summarise(filtered(), n = n(), avg = mean(marks))
  })
}
```

Three benefits: the filter runs **once** per change; the logic exists in **one
place**, so a fix applies everywhere; and Shiny **caches** the result until an
input actually changes.

**Remember the parentheses.** `filtered` is the reactive itself; `filtered()` is
its current value. Omitting them is the most common Shiny error there is.

---

## Exam questions from this unit

**Two marks**

1. Distinguish seasonality from a cycle.
2. What does the `d` in ARIMA(p,d,q) represent?
3. State the null hypothesis of the ADF test.
4. Which plot gives p, and which gives q?
5. What are the two halves of a Shiny app?
6. Why must a reactive be called with parentheses?

**Five marks**

1. Explain the components of a time series and the two decomposition models.
2. Explain stationarity, why it matters, and how to achieve it.
3. Explain how ACF and PACF identify AR and MA orders.
4. Explain reactivity in Shiny with an example.
5. Explain `ggplotly()` and native plotly, with the differences.

**Ten marks**

1. Explain ARIMA modelling end to end — stationarity testing, differencing,
   order identification, fitting, residual checking and forecasting.
2. Build and explain a complete Shiny application with inputs, reactive
   expressions and multiple outputs.

## Mistakes that cost marks

- Setting `frequency` wrongly in `ts()`, disabling all seasonal modelling
- Reading ADF's p-value as though its null were stationarity
- Over-differencing — twice is almost always enough
- Reading p from the ACF and q from the PACF (they are the other way round)
- Skipping the residual check after fitting
- Wanting a **small** Ljung-Box p-value; you want a large one
- Using `+` to chain plotly layers instead of `%>%`
- Omitting `~` in plotly column references
- Calling a Shiny reactive without `()`
- Mismatched output IDs between `ui` and `server`
