# =====================================================================
# Run with R 4.3.3. Rscript builds each chart but has nowhere to show it, so
# _drive_17_plotly.py runs this file with each chart saved as a web page, and
# opens each in Chromium for the screenshots on the lab page. (Until October
# 2026 R could not be installed where these labs are checked, so this file
# was desk-checked only.)
# =====================================================================
# Experiment 17: Interactive visualisations with plotly
# No Python equivalent -- this demonstrates plotly's R interface specifically.

library(plotly); library(ggplot2)

# Step 1: Make the students data frame
students <- data.frame(
  name    = c("Ananya","Bhavana","Charan","Divya","Eshwar",
              "Fiona","Gopal","Harika","Ismail","Jyothi"),
  section = c("A","A","B","B","A","C","C","B","A","C"),
  hours   = c(9, 5, 11, 4, 7, 8, 3, 10, 6, 2),
  marks   = c(85, 62, 91, 55, 74, 79, 48, 88, 68, 41))

# --- THE ONE-LINE ROUTE: convert any ggplot2 plot ---
# Step 2: Make a ggplot2 chart interactive
p <- ggplot(students, aes(x = hours, y = marks, colour = section)) +
       geom_point(size = 3) +
       labs(title = "Marks against study hours")
ggplotly(p)          # hover, zoom and pan now work. That is the whole trick.

# --- NATIVE plotly ---
# Step 3: Draw a native plotly scatter, with hover text
plot_ly(students,
        x = ~hours, y = ~marks, color = ~section,      # NOTE the ~
        type = "scatter", mode = "markers",
        marker = list(size = 12),
        text = ~paste("Name:", name, "<br>Marks:", marks),
        hoverinfo = "text") %>%
  layout(title = "Marks against study hours",
         xaxis = list(title = "Hours studied"),
         yaxis = list(title = "Marks"))

# TWO THINGS THAT CATCH PEOPLE:
#   1. plotly uses FORMULA notation (~hours) to name columns. Writing
#      x = hours looks for a variable in your environment and fails.
#   2. plotly layers chain with %>%, NOT with + . This is the reverse of
#      ggplot2, and mixing them is the commonest plotly error.

# --- BAR AND LINE ---
# Step 4: Draw a bar chart of the means
avg <- aggregate(marks ~ section, students, mean)
plot_ly(avg, x = ~section, y = ~marks, type = "bar",
        marker = list(color = "#1e7fbf"))

# --- ANIMATION: one extra argument ---
# library(gapminder)
# plot_ly(gapminder, x = ~gdpPercap, y = ~lifeExp,
#         size = ~pop, color = ~continent,
#         frame = ~year,                 # <- this creates the animation
#         type = "scatter", mode = "markers") %>%
#   layout(xaxis = list(type = "log")) %>%
#   animation_opts(frame = 1000, transition = 500, redraw = FALSE)
#
# frame = ~year is ALL an animation needs. plotly adds the play button and
# the slider automatically -- the famous Gapminder chart in six lines.

# --- RANGE SLIDER for a time series ---
# plot_ly(x = ~time(AirPassengers), y = ~AirPassengers,
#         type = "scatter", mode = "lines") %>%
#   rangeslider()

# --- EXPORT ---
# htmlwidgets::saveWidget(fig, "plot.html")
