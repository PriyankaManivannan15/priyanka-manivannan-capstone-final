#Skyscanner Flight Price Tracker 

##Introduction
This project aims to empower budget-conscious travellers with a flight price tracking dashboard. I'll focus on Ryanair flight FR1882 from London to Lisbon, departing on August 21st, 2024.

The key focus is to help customers make informed financial decisions as flight prices tend to fluctuate for a multitude of reasons including demand, time of year, etc. Overall, price tracking allows customers to be smarter and more strategic shoppers, leading to informed decisions, potential savings, and a greater sense of control over their finances.

This project tracks the prices from Skyscanner by calling an unofficial API. Information gathered will be stored in a SQL database. Finally, the data will be visualised via an interactive graph on a Streamlit app. 


##Part 1
Created a Python script to obtain flight prices from the API and the current date and time the server running the python script. The .py script sits on a job server, running a CRON job every 3 hours. Next, it will store the data on a SQL database.

##Part 2 
A user-friendly Streamlit dashboard serves as the visual interface. It connects to the SQL database, retrieving the stored price data. This data is then transformed into a captivating and interactive graph, showcasing price fluctuations over time. 


This project equips travellers with a powerful tool to navigate the dynamic world of flight pricing. By tracking trends and identifying optimal booking windows, they can save money and plan better for their journeys.
