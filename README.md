# 📈 Sales Forecasting Dashboard

A Streamlit-based time series forecasting app that predicts future sales based on historical data.

## Features

- Visualize historical sales data
- Forecast future sales using regression
- Adjustable forecast window
- Download predictions as CSV

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Matplotlib

## Run

```bash
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Project Structure

sales-forecasting-dashboard/
│
├── app.py
├── train_model.py
├── sales_data.csv
├── model.pkl
├── README.md
└── screenshots/

## Future Improvements

- Use ARIMA / Prophet models
- Add seasonality detection
- Use real-world sales dataset
- Deploy on cloud

## Author

Siddharth Shetty  
M.Sc. Artificial Intelligence