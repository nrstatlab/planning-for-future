# =====================================================================
# NOT EXECUTED IN VERIFICATION -- R is not installable in this environment
# (Debian repos blocked). Desk-checked only; numbers in comments come from
# the executed Python equivalent in python/. Run this in RStudio.
# =====================================================================
# Experiment 18: A Shiny app that lets users upload a CSV file
# No Python equivalent -- this demonstrates the Shiny framework itself.
#
# Run with:  shiny::runApp("18_shiny_app.R")
# or paste into RStudio and click "Run App".

library(shiny); library(ggplot2); library(dplyr)

ui <- fluidPage(
  titlePanel("CSV Explorer"),

  sidebarLayout(
    sidebarPanel(
      fileInput("file", "Upload a CSV file", accept = ".csv"),
      checkboxInput("header", "File has a header row", TRUE),
      uiOutput("column_picker"),          # built dynamically from the file
      sliderInput("bins", "Histogram bins:", min = 5, max = 50, value = 20),
      hr(),
      helpText("Upload any CSV. The app lists its columns and plots whichever",
               "numeric column you choose.")
    ),

    mainPanel(
      tabsetPanel(
        tabPanel("Data",    tableOutput("preview")),
        tabPanel("Summary", verbatimTextOutput("summary")),
        tabPanel("Plot",    plotOutput("histogram"))
      )
    )
  )
)

server <- function(input, output, session) {

  # ONE reactive, shared by every output. Written this way the file is read
  # ONCE per upload; copying read.csv() into each render*() would read it
  # three times.
  data <- reactive({
    req(input$file)                        # wait until a file is uploaded
    read.csv(input$file$datapath, header = input$header,
             stringsAsFactors = FALSE)
  })

  # Build the column dropdown from the uploaded file's numeric columns.
  output$column_picker <- renderUI({
    req(data())
    nums <- names(data())[sapply(data(), is.numeric)]
    selectInput("column", "Numeric column to plot:", choices = nums)
  })

  output$preview <- renderTable({
    head(data(), 10)                       # NOTE the parentheses: data()
  })

  output$summary <- renderPrint({
    summary(data())
  })

  output$histogram <- renderPlot({
    req(input$column)
    ggplot(data(), aes(x = .data[[input$column]])) +
      geom_histogram(bins = input$bins, fill = "#1e7fbf", colour = "white") +
      labs(title = paste("Distribution of", input$column),
           x = input$column) +
      theme_minimal()
  })
}

shinyApp(ui = ui, server = server)

# THE THREE RULES THAT CAUSE MOST SHINY BUGS:
#   1. Call a reactive WITH parentheses: data(), never data.
#   2. input$x can only be read inside a reactive context -- reactive(),
#      observe() or render*(). At the top level of server() it errors.
#   3. Every output ID must match: plotOutput("histogram") in the UI pairs
#      with output$histogram in the server. A typo gives a blank panel and
#      NO error message, so check spelling first when nothing appears.
#
# req() is the idiomatic way to wait for an input: it silently stops the
# reactive until its argument is available, instead of erroring on NULL.
