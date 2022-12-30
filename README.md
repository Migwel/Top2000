# NPO Radio 2 Top 2000 - Data extraction and (quick) analysis

This is a program I created because I wanted to find out the decennia-distribution evolution over the years for songs in the [NPO Radio 2 Top 2000](https://www.nporadio2.nl/top2000).

It works in 2 steps.

## Download the data

First, we need to download all the data from the years. That's done in `ManualTestTop2000Processor#test_downloadRankings_valid`. It will make some calls to NPO's APIs and save the results in a sqlite `top2000.db` database.

If you prefer to save this using CSV, you can change the test to use the CSVWriter (or create your own writer if you'd rather use another format. It should be fairly straightforward).

## Analyze and display the data

Now that the data are available locally, we can show the evolution of the decennia-distribution using `ManualTestGraphDrawer#test_plot_year_popularity`.