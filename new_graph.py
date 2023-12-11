import plotly.graph_objs as go
import sqlite3
from datetime import datetime, timedelta
import plotly.offline as pyo

# Function to create an interactive plot
def create_plot(data, title):
    traces = []
    for carpark_name, carpark_values in data.items():
        trace = go.Scatter(
            x=carpark_values["timestamps"],
            y=carpark_values["spaces"],
            mode='lines+markers',
            name=carpark_name,
            text=[f"{carpark_name}<br>Spaces: {spaces}" for spaces in carpark_values["spaces"]],
        )
        traces.append(trace)

    layout = go.Layout(
        title=title,
        xaxis=dict(title='Date'),
        yaxis=dict(title='Total Spaces'),
        hovermode='closest',
    )

    fig = go.Figure(data=traces, layout=layout)
    return pyo.plot(fig, output_type='div', include_plotlyjs=True, show_link=False)

# Connect to the SQLite database
conn = sqlite3.connect('parking_data.db')
cursor = conn.cursor()

# Example SQL query to fetch data for each carpark
query = "SELECT timestamp, spaces, name FROM parking_history WHERE timestamp >= ? AND timestamp <= ?"
end_date = int(datetime.now().timestamp())

# Create plots for the day, week, and month
plots = []
for duration, days_back in [("Day", 1), ("Week", 7), ("Month", 30)]:
    start_date = int((datetime.now() - timedelta(days=days_back)).timestamp())
    cursor.execute(query, (start_date, end_date))

    # Fetch the data
    data = cursor.fetchall()

    # Convert timestamp integers to datetime objects
    data = [{"timestamp": datetime.utcfromtimestamp(entry[0]), "spaces": entry[1], "name": entry[2]} for entry in data]

    # Create a dictionary to store data for each carpark
    carpark_data = {}

    # Populate the dictionary with data for each carpark
    for entry in data:
        carpark_name = entry["name"]
        if carpark_name not in carpark_data:
            carpark_data[carpark_name] = {"timestamps": [], "spaces": []}
        carpark_data[carpark_name]["timestamps"].append(entry["timestamp"])
        carpark_data[carpark_name]["spaces"].append(entry["spaces"])

    plots.append(create_plot(carpark_data, f'Parking Spaces Over Time for Each Carpark - Last {duration}'))

# Close the database connection
conn.close()

# Save the plot divs to separate files
for i, duration in enumerate(["day", "week", "month"]):
    with open(f"plot_{duration}.html", "w") as plot_file:
        plot_file.write(plots[i])

