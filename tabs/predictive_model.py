import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

def prepare_model_features(df):
    """
    Prepare features for the predictive model
    """
    # Select relevant features and target
    features_df = df.copy()
    
    # Create dummy variables for categorical features
    features_df = pd.get_dummies(
        features_df, 
        columns=['travel_group', 'duration_category', 'window_category', 'device_package'],
        drop_first=True
    )
    
    # Select important features
    selected_features = [
        'is_mobile', 'is_package', 'srch_adults_cnt', 'srch_children_cnt', 'srch_rm_cnt',
        'trip_duration', 'booking_window'
    ]
    
    # Add dummy columns if they exist
    for col in features_df.columns:
        if col.startswith(('travel_group_', 'duration_category_', 'window_category_', 'device_package_')):
            selected_features.append(col)
    
    # Filter to include only the selected features that actually exist
    valid_features = [f for f in selected_features if f in features_df.columns]
    
    # Create feature matrix X and target vector y
    X = features_df[valid_features].fillna(0)
    y = features_df['is_booking']
    
    return X, y

@st.cache_data
def train_model(X, y):
    """
    Train a Random Forest model and return evaluation metrics
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
    # Get feature importances
    feature_importances = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Create confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    return model, accuracy, precision, recall, f1, feature_importances, cm, X_test

def show_predictive_model_tab(df):
    """
    Display predictive model analysis in the fourth tab
    """
    st.header("Predictive Modeling: Booking Likelihood")
    
    st.write("This model predicts the likelihood of a search resulting in a booking based on the dataset characteristics.")
    
    # Create a subset for modeling to avoid memory issues
    model_df = df.dropna(subset=['trip_duration', 'booking_window']).sample(n=min(50000, len(df)), random_state=42)
    
    # Calculate overall booking rate for reference
    total_searches = df.shape[0]
    total_bookings = df[df['is_booking'] == 1].shape[0]
    booking_rate = (total_bookings / total_searches) * 100
    
    # Prepare features and train model
    with st.spinner('Training predictive model...'):
        try:
            X, y = prepare_model_features(model_df)
            model, accuracy, precision, recall, f1, feature_importances, cm, X_test = train_model(X, y)
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Accuracy", f"{accuracy:.2f}")
            col2.metric("Precision", f"{precision:.2f}")
            col3.metric("Recall", f"{recall:.2f}")
            col4.metric("F1 Score", f"{f1:.2f}")
            
            # Display feature importances
            st.subheader("Feature Importance")
            fig = px.bar(
                feature_importances.head(15),
                x='importance',
                y='feature',
                orientation='h',
                title='Top 15 Features for Predicting Booking Likelihood',
                height=500
            )
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Display confusion matrix
            st.subheader("Confusion Matrix")
            cm_labels = ['Not Booked', 'Booked']
            fig = ff.create_annotated_heatmap(
                z=cm,
                x=cm_labels,
                y=cm_labels,
                colorscale='Blues'
            )
            fig.update_layout(title='Confusion Matrix', height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Interactive prediction
            st.subheader("Booking Likelihood Prediction Simulator")
            st.write("Adjust the parameters to see how they affect booking likelihood:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                is_mobile = st.selectbox("Device Type", [("Desktop", 0), ("Mobile", 1)], format_func=lambda x: x[0])
                is_package = st.selectbox("Package Type", [("Non-Package", 0), ("Package", 1)], format_func=lambda x: x[0])
                adults = st.slider("Number of Adults", 1, 10, 2)
                children = st.slider("Number of Children", 0, 5, 0)
            
            with col2:
                rooms = st.slider("Number of Rooms", 1, 5, 1)
                trip_days = st.slider("Trip Duration (days)", 1, 30, 3)
                booking_window_days = st.slider("Days Before Check-in", 0, 120, 14)
            
            # Create a sample for prediction
            if 'travel_group_Solo' in X.columns:
                travel_group_cols = [col for col in X.columns if col.startswith('travel_group_')]
                duration_cols = [col for col in X.columns if col.startswith('duration_category_')]
                window_cols = [col for col in X.columns if col.startswith('window_category_')]
                device_package_cols = [col for col in X.columns if col.startswith('device_package_')]
                
                # Create a sample with all features (initialized to 0)
                sample = pd.DataFrame(0, index=[0], columns=X.columns)
                
                # Set the provided feature values
                sample['is_mobile'] = is_mobile[1]
                sample['is_package'] = is_package[1]
                sample['srch_adults_cnt'] = adults
                sample['srch_children_cnt'] = children
                sample['srch_rm_cnt'] = rooms
                sample['trip_duration'] = trip_days
                sample['booking_window'] = booking_window_days
                
                # Determine travel group
                if adults == 1 and children == 0:
                    travel_group = 'Solo'
                elif adults == 2 and children == 0:
                    travel_group = 'Couple'
                elif adults == 1 and children > 0:
                    travel_group = 'Single Parent'
                elif adults == 2 and children > 0:
                    travel_group = 'Family'
                elif adults > 2:
                    travel_group = 'Group'
                else:
                    travel_group = 'Other'
                
                # Set travel group dummy
                for col in travel_group_cols:
                    if col == f'travel_group_{travel_group}':
                        sample[col] = 1
                
                # Determine duration category
                if trip_days <= 3:
                    duration = '1-3 days'
                elif trip_days <= 7:
                    duration = '4-7 days'
                elif trip_days <= 14:
                    duration = '8-14 days'
                else:
                    duration = '15+ days'
                
                # Set duration dummy
                for col in duration_cols:
                    if col == f'duration_category_{duration}':
                        sample[col] = 1
                
                # Determine booking window category
                if booking_window_days < 7:
                    window = '0-6 days'
                elif booking_window_days < 14:
                    window = '7-13 days'
                elif booking_window_days < 30:
                    window = '14-29 days'
                elif booking_window_days < 60:
                    window = '30-59 days'
                elif booking_window_days < 90:
                    window = '60-89 days'
                else:
                    window = '90+ days'
                
                # Set window dummy
                for col in window_cols:
                    if col == f'window_category_{window}':
                        sample[col] = 1
                
                # Set device package combination
                device = 'Mobile' if is_mobile[1] == 1 else 'Desktop'
                package = 'Package' if is_package[1] == 1 else 'Non-Package'
                device_package = f'{device}, {package}'
                
                for col in device_package_cols:
                    if col == f'device_package_{device_package}':
                        sample[col] = 1
                
                # Make prediction
                prediction_prob = model.predict_proba(sample)[0][1]  # Probability of booking
                
                # Display prediction with gauge
                st.subheader("Booking Likelihood Prediction")
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = prediction_prob * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Booking Probability (%)"},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 25], 'color': "lightgray"},
                            {'range': [25, 50], 'color': "gray"},
                            {'range': [50, 75], 'color': "lightblue"},
                            {'range': [75, 100], 'color': "royalblue"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': booking_rate
                        }
                    }
                ))
                
                fig.add_annotation(
                    x=0.5,
                    y=0.25,
                    text=f"Average: {booking_rate:.1f}%",
                    showarrow=False
                )
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                # Interpretation
                st.markdown(f"""
                **Interpretation:**
                - The predicted booking likelihood is **{prediction_prob * 100:.1f}%**
                - The average booking rate is **{booking_rate:.1f}%**
                - This search is **{(prediction_prob * 100 / booking_rate):.1f}x** {'more' if prediction_prob * 100 > booking_rate else 'less'} likely to convert than average
                """)
                
                # Suggestions to improve booking likelihood
                if prediction_prob * 100 < 15:
                    st.markdown("""
                    **Suggestions to improve booking likelihood:**
                    """)
                    suggestions = []
                    
                    if is_package[1] == 1:
                        suggestions.append("- Consider offering non-package options, which have higher conversion rates")
                    
                    if is_mobile[1] == 1:
                        suggestions.append("- Optimize the mobile user experience to close the conversion gap with desktop")
                    
                    if trip_days > 3:
                        suggestions.append("- Focus on promoting shorter stay options (1-3 days) which convert better")
                    
                    if booking_window_days > 60 or booking_window_days < 7:
                        suggestions.append("- Target the 30-59 day booking window which shows optimal conversion rates")
                    
                    if adults == 2 and children > 0:
                        suggestions.append("- Create special offers for families to improve their conversion rates")
                    
                    if len(suggestions) > 0:
                        for suggestion in suggestions:
                            st.markdown(suggestion)
                    else:
                        st.markdown("- Consider bundling complementary services to increase value perception")
            else:
                st.error("Insufficient data to create interactive prediction. Try increasing the sample size.")
        
        except Exception as e:
            st.error(f"Error in model training or prediction: {e}")