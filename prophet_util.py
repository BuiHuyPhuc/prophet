from io import BytesIO
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from flask import flash

def create_plots(filepath):
    forecast_fig, components_fig = get_figures(filepath)
    forecast_canvas = FigureCanvasAgg(forecast_fig)
    components_canvas = FigureCanvasAgg(components_fig)
    buf1 = BytesIO()
    buf2 = BytesIO()

    with open('static/img/img1.png', 'wb') as forecast_file:
        forecast_canvas.print_png(buf1)
        forecast_file.write(buf1.getvalue())
    with open('static/img/img2.png', 'wb') as components_file:
        components_canvas.print_png(buf2)
        components_file.write(buf2.getvalue())

def get_figures(filepath):
    df = pd.read_csv(filepath)
    df.columns = ['ds', 'y']
    m = Prophet().fit(df)
    future = m.make_future_dataframe(periods=90)
    forecast = m.predict(future)
    forecast_fig = m.plot(forecast)
    add_changepoints_to_plot(forecast_fig.gca(), m, forecast)
    components_fig = m.plot_components(forecast)
    return forecast_fig, components_fig

def custom_plots(filepath, txtFuture_periods, txtChangepoints, txtChangepoint_range, txtChangepoint_scale, ckbCountry_holidays, txtHolidays_scale, ckbMonthly_seasonality, txtSeasonality_days, txtFourier_monthly):
    forecast_fig, components_fig = get_custom_figures(filepath, txtFuture_periods, txtChangepoints, txtChangepoint_range, txtChangepoint_scale, ckbCountry_holidays, txtHolidays_scale, ckbMonthly_seasonality, txtSeasonality_days, txtFourier_monthly)
    forecast_canvas = FigureCanvasAgg(forecast_fig)
    components_canvas = FigureCanvasAgg(components_fig)
    buf1 = BytesIO()
    buf2 = BytesIO()

    with open('static/img/img1.png', 'wb') as forecast_file:
        forecast_canvas.print_png(buf1)
        forecast_file.write(buf1.getvalue())
    with open('static/img/img2.png', 'wb') as components_file:
        components_canvas.print_png(buf2)
        components_file.write(buf2.getvalue())

def get_custom_figures(filepath, txtFuture_periods, txtChangepoints, txtChangepoint_range, txtChangepoint_scale, ckbCountry_holidays, txtHolidays_scale, ckbMonthly_seasonality, txtSeasonality_days, txtFourier_monthly):
    df = pd.read_csv(filepath)
    df.columns = ['ds', 'y']
    custom_figures = {
        'n_changepoints': int(txtChangepoints),
        'changepoint_range': float(txtChangepoint_range),
        'changepoint_prior_scale': float(txtChangepoint_scale),
        'holidays_prior_scale': float(txtHolidays_scale),
    }
    if ckbCountry_holidays:
        ckbCountry = 'true'
    else:
        ckbCountry = 'false'
    if ckbMonthly_seasonality:
        ckbMonthly = 'true'
    else:
        ckbMonthly = 'false'
    messsage = 'Future periods = ' + txtFuture_periods + ' || n_changepoints = ' + txtChangepoints + ' || changepoint_range = ' + txtChangepoint_range + ' || changepoint_range = ' + txtChangepoint_scale + ' || add_country_holidays(VN) = ' + ckbCountry + ' || holidays_prior_scale = ' + txtHolidays_scale + ' || add_seasonality(monnthly) = ' + ckbMonthly + ' || Seasonality days = ' + txtSeasonality_days + ' || Fourier monthly = ' + txtFourier_monthly
    flash(messsage)
    m = Prophet(**custom_figures)
    if ckbCountry_holidays:
        m.add_country_holidays(country_name='VN')
    if ckbMonthly_seasonality:
        m.add_seasonality(name='monthly', period=float(txtSeasonality_days), fourier_order=int(txtFourier_monthly))
    m.fit(df)
    future = m.make_future_dataframe(periods=int(txtFuture_periods))
    forecast = m.predict(future)
    forecast_fig = m.plot(forecast)
    add_changepoints_to_plot(forecast_fig.gca(), m, forecast)
    components_fig = m.plot_components(forecast)
    return forecast_fig, components_fig
