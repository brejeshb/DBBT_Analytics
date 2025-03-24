# Travel Agency Digital Transformation Dashboard

This Streamlit application analyzes travel agency search and booking data to provide data-driven recommendations for digital transformation. The application includes comprehensive visualizations, predictive modeling, and strategic recommendations based on customer behavior patterns.

## Features

- **Interactive Data Analysis**: Explore search and booking patterns across multiple dimensions
- **Predictive Model**: ML-powered booking likelihood prediction
- **Strategic Recommendations**: Five key areas for digital transformation
- **Implementation Roadmap**: Phased approach with prioritized initiatives
- **KPI Dashboard**: Track progress with clear performance indicators

## Project Structure

```
travel-agency-analytics/
├── app.py                        # Main Streamlit application
├── data_loader.py                # Data loading and preprocessing functions
├── utils.py                      # Utility functions
├── tabs/                         # Directory for tab modules
│   ├── __init__.py              # Makes tabs a proper package
│   ├── key_metrics.py           # Key Metrics & Trends tab
│   ├── user_device.py           # User & Device Analysis tab
│   ├── trip_characteristics.py  # Trip Characteristics tab
│   ├── predictive_model.py      # Predictive Model tab
│   └── recommendations.py       # Recommendations tab
├── requirements.txt              # Required Python packages
└── README.md                     # Project documentation
```

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/travel-agency-analytics.git
   cd travel-agency-analytics
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Place your `travel.csv` file in the project root directory

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. The application will open in your default web browser at http://localhost:8501

## Data Requirements

The application expects a CSV file named `travel.csv` with the following columns:

- `date_time`: Search timestamp
- `site_name`: Site identifier
- `posa_continent`: Point of sale continent
- `user_location_country`: User's country
- `user_location_region`: User's region
- `user_location_city`: User's city
- `orig_destination_distance`: Distance between user and destination
- `user_id`: User identifier
- `is_mobile`: Whether search was performed on mobile (0/1)
- `is_package`: Whether search was for a package (0/1)
- `channel`: Marketing channel
- `srch_ci`: Check-in date
- `srch_co`: Check-out date
- `srch_adults_cnt`: Number of adults
- `srch_children_cnt`: Number of children
- `srch_rm_cnt`: Number of rooms
- `srch_destination_id`: Destination identifier
- `srch_destination_type_id`: Destination type
- `is_booking`: Whether search resulted in booking (0/1)
- `cnt`: Count of similar events
- `hotel_continent`: Hotel continent
- `hotel_country`: Hotel country
- `hotel_market`: Hotel market
- `hotel_cluster`: Hotel cluster

## Key Analysis Areas

1. **Key Metrics & Trends**
   - Overall conversion rates
   - Monthly trends
   - Seasonal patterns

2. **User & Device Analysis**
   - Mobile vs. desktop performance
   - Package vs. non-package comparison
   - Travel group composition

3. **Trip Characteristics**
   - Impact of trip duration
   - Booking window patterns
   - Distance and market analysis

4. **Predictive Model**
   - Machine learning model to predict booking likelihood
   - Feature importance analysis
   - Interactive prediction simulator

5. **Recommendations**
   - Five strategic initiatives for digital transformation
   - Implementation roadmap
   - Key performance indicators

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.