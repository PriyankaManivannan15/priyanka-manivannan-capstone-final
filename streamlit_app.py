
#IMPORTS 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go



#LIMITATION! - I have hardcoded some lines which I would have called directly from the API. However, due to the limitations of the API calls due to a pay wall, I have had to hardcoded some lines. These are the values which stay the same such as airport names, times, etc., and I chose not to put them in the database to help with efficiency. If I were to do this project again, I would choose an API with unlimited calls. 


#BANNER
# Set page config - allow space for the banner 
st.set_page_config(layout="wide")
# Create custom HTML for the banner - contains HTML and CSS ('<style>' tag) needed for the style of the banner 
custom_html = """
<div class="banner">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Skyscanner_Logo_LockupHorizontal_SkyBlue_RGB.svg/2560px-Skyscanner_Logo_LockupHorizontal_SkyBlue_RGB.svg.png">
</div>
<style> 
    .banner {
        width: 100%;
        height: 1000px;
        overflow: hidden;
    }
    .banner img {
        width: 80%;
        object-fit: cover;
    }
</style>
"""
# Display the custom HTML as banner 
st.components.v1.html(custom_html)


#TITLE
st.title('SkyScanner Flight Price Tracker')


#BASIC FLIGHT INFO
ryanair_logo = 'https://asset.brandfetch.io/id4cYT-jDh/idzbGUuJm1.png'
st.header('  :blue[Flight Information]')
t1, t2 = st.columns((1,3.5)) 
t1.image(ryanair_logo, width = 160)
t2.subheader(" One-Way Flight: London   :arrow_right: Lisbon ")
t2.subheader(" Date: 21/08/2024 ")
t2.subheader(" Airline: Ryanair")




#DEPARTURE & ARRIVAL TIMES
col1, col2 = st.columns(2)
with col1:
    tile = col1.container(height=120)
    tile.subheader(f'**Departure**  :airplane_departure:- 9:55')
    tile.markdown(f'**Airport**: Standard Airport')
with col2:
    tile = col2.container(height=120)
    tile.subheader(f"**Arrival**    :airplane_arriving:- 12:45")
    tile.markdown("**Airport**: Lisbon")
col1, col2 = st.columns(2)




#CONNECT TO THE DB
conn = st.connection("postgresql", dialect = "postgresql", type = "sql")
#SQL query to fetch data from the DB and store results in pandas DF
df = conn.query('SELECT * FROM student.pm_flight_price;',ttl ="165m") # Cache the data for 2 hours and 45 minutes




#STAND OUT METRICS AND BUTTON TO PRUCHASE TICKET
st.header('  :blue[Metrics]')
st.markdown('Updated Every 3 Hours')
# Calculate required values
current_price = df['price'].iloc[-1]  # Last price in the DataFrame
average_price = df['price'].mean()
lowest_price = df['price'].min()
highest_price = df['price'].max()
# Calculate percentage difference with average price
price_diff_percentage = ((current_price - average_price) / average_price) * 100
# Format the price_diff_percentage with the correct symbol
if price_diff_percentage > 0:
    delta_symbol = "+"
elif price_diff_percentage < 0:
    delta_symbol = "-"
else:
    delta_symbol = ""
delta_text = f"{delta_symbol}{price_diff_percentage:.1f}% vs avg"
# Display metrics 
col3, col4, col5, col6, col7 = st.columns(5)
col3.metric(label="Current Price", value=f"£{current_price:.2f}", delta=delta_text)
col4.metric(label="Average Price", value=f"£{average_price:.2f}")
col5.metric(label="Lowest Price", value=f"£{lowest_price:.2f}")
col6.metric(label="Highest Price", value=f"£{highest_price:.2f}")
#Button link to Skyscanner webpage
col7.link_button("Buy Ticket","https://www.skyscanner.net/transport/flights/lond/lis/240821/config/16574-2408210955--31915-0-13577-2408211245?adultsv2=1&cabinclass=economy&childrenv2=&ref=home&rtn=0&preferdirects=true&outboundaltsenabled=false&inboundaltsenabled=false", type ='primary')



#GRAPH - Interactive Plotly chart
st.header('  :blue[Price History]')
# Create the chart data DataFrame - contains run_time and price
chart_data = pd.DataFrame({
    'Date & Time': df['run_time'],
    'Price (£)': df['price']
})
# Create the empty Plotly figure
# Figure object - container for all elements to make up graph - data tarces, graph layout, etc
fig = go.Figure()
# add_trace () method - allows the graph to be updated 
# Add the price line - flight price over time
fig.add_trace(go.Scatter(x=chart_data['Date & Time'], y=chart_data['Price (£)'],
                         mode='lines', name='Price', line=dict(color='LightBlue')))
# Add the average price line - average flight price over time for visual comparison 
fig.add_trace(go.Scatter(x=chart_data['Date & Time'], y=[average_price] * len(chart_data),
                         mode='lines', name=f'Average Price: £{average_price:.2f}', line=dict(color='lightgreen', dash='dash')))
# Add detail for graph
fig.update_layout(
    title='Price History',
    xaxis_title='Date & Time',
    yaxis_title='Price (£)',
    xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGray'),
    legend=dict( # Customise Legend
        font=dict(size=16, color="white"),  
        bgcolor="DarkBlue",  
        bordercolor="LightBlue",  
        borderwidth=2,  
    ),
    showlegend=True
)
# Display Plotly chart
st.plotly_chart(fig, use_container_width=True)





#SIDEBAR - POLICY INFORMATION 
st.sidebar.header("Policy Information")
data = ['Not Allowed'] * 4
index = ['Change Allowed', 'Partially Changeable', 'Cancellation Allowed', 'Partially Refundable']
policy_df = pd.DataFrame(data, index=index, columns=['Flight Policy'])
# Display the DataFrame in Streamlit
st.sidebar.write(policy_df)
st.sidebar.link_button("Terms of Service","https://www.skyscanner.net/terms-of-service#:~:text=To%20the%20maximum%20extent%20permitted,act%20of%20god%2C%20accident%2C%20delay", type ='secondary')

