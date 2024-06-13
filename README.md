## Logistic Optimization: Delivery Drivers Location Optimization with Causal Inference
# Overview
This project is focused on optimizing the placement of delivery drivers for Gokada, the largest last-mile delivery service in Nigeria. The goal is to increase the fraction of completed orders by analyzing the causes of unfulfilled requests and recommending optimal driver locations using causal inference techniques.

# Business Need
Gokada has experienced a high number of unfulfilled delivery requests due to sub-optimal placement of drivers. By understanding the primary causes of these unfulfilled requests and optimizing driver locations, Gokada aims to enhance client satisfaction and business growth.

# Proposed Methodology
Tasks
Data Exploration (EDA)

Analyze the datasets to understand their structure and contents.
Identify and treat missing values and outliers.
Create new features using external data (e.g., weather, traffic, holidays).
Compute distances, driving speeds, and other key variables between geographic coordinates and timestamps.
Visualize clusters of delivery start and end locations.
Creative Visualization

Produce an interactive web-based visualization to tell a story about the delivery data.
Causal Learning

Split data into training and hold-out sets.
Create and validate causal graphs.
Answer key business questions using causal inference techniques.
Logistic Optimization

Formalize the problem of driver placement using integer optimization techniques.
Blog Reporting

Write a blog-like report detailing the process, challenges, insights, and lessons learned.
Data
Datasets
Completed Orders

Contains information about completed deliveries.
Delivery Requests

Contains information about delivery requests, both completed and unfulfilled.
Columns in Completed Orders
Trip ID: Unique identifier for each trip.
Trip Origin: Address of the trip origin.
Trip Destination: Address of the trip destination.
Trip Start Time: Timestamp of when the trip started.
Trip End Time: Timestamp of when the trip ended.
Columns in Delivery Requests
id: Unique identifier for each request.
order_id: Unique identifier for each order.
driver_id: Unique identifier for each driver.
driver_action: Action taken by the driver (e.g., accepted, declined).
lat: Latitude of the request.
lng: Longitude of the request.
Expected Outcomes
Skills
Modeling problems as causal graphs.
Statistical modeling and inference extraction.
Building model pipelines and orchestration.
Knowledge
Causal inference and statistical learning.
Hypothesis formulation and testing.
Data filtering, transformation, and warehouse management.
MLOps and AutoML.
