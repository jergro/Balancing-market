# SAVE TO CSV
client = EntsoePandasClient(api_key="da2215ea-932c-46c4-a302-223f0388a0ce")

start = pd.Timestamp('20200101', tz='Europe/Stockholm')
end = pd.Timestamp('20210101', tz='Europe/Stockholm')

country_codes = ['SE_1','SE_2','SE_3','SE_4']

for country_code in country_codes:
    imbalance_prices = client.query_imbalance_prices(country_code, start=start, end=end)
    imbalance_prices.to_csv('data/imbalance_prices_'+country_code+'.csv', index_label = ['Date'])

for country_code in country_codes:
    day_ahead_prices = client.query_day_ahead_prices(country_code, start=start, end=end)
    day_ahead_prices.to_csv('data/day_ahead_prices_'+country_code+'.csv', index_label = ['Date'], header = ['EUR'])

for country_code in country_codes:
    # day-ahead load forecast
    load_forecast = client.query_load_forecast(country_code, start=start, end=end)
    load_forecast.to_csv('data/load_forecast_'+country_code+'.csv', index_label = ['Date'], header = ['Forecasted MWh'])

client = EntsoePandasClient(api_key="da2215ea-932c-46c4-a302-223f0388a0ce")
for country_code in country_codes:
    load = client.query_load(country_code, start=start, end=end)
    load.to_csv('data/load_'+country_code+'.csv', index_label = ['Date'], header = ['Actual MWh'])

client = EntsoePandasClient(api_key="da2215ea-932c-46c4-a302-223f0388a0ce")
for country_code in country_codes:
    generation = client.query_generation(country_code, start=start, end=end)
    generation.to_csv('data/generation_'+country_code+'.csv' , index_label = ['Date'])

client = EntsoePandasClient(api_key="da2215ea-932c-46c4-a302-223f0388a0ce")
for country_code in country_codes:
    generation_forecast = client.query_generation_forecast(country_code, start=start, end=end)
    generation_forecast.to_csv('data/generation_forecast_'+country_code+'.csv' , index_label = ['Date'])

client = EntsoePandasClient(api_key="da2215ea-932c-46c4-a302-223f0388a0ce")
for country_code in country_codes:
    wind_generation_forecast = client.query_wind_and_solar_forecast(country_code, start=start, end=end)
    wind_generation_forecast.to_csv('data/wind_generation_forecast_'+country_code+'.csv', index_label = ['Date'])


# LOAD FROM CSV
country_codes = ['SE_1','SE_2','SE_3','SE_4']
imbalance_prices = []
day_ahead_prices = []
load_forecasts = []
loads = []
generation_forecasts = []
wind_and_solar_generation_forecasts = []

for country_code in country_codes:
    imbalance_price = pd.read_csv('data/imbalance_prices_'+country_code+'.csv', index_col=[0])
    imbalance_price.index = pd.to_datetime(imbalance_price.index, utc=True)
    imbalance_prices += [imbalance_price]

    day_ahead_price = pd.read_csv('data/day_ahead_prices_'+country_code+'.csv', index_col=[0])
    day_ahead_price.index = pd.to_datetime(day_ahead_price.index, utc=True)
    day_ahead_prices += [day_ahead_price]

    load_forecast = pd.read_csv('data/load_forecast_'+country_code+'.csv', index_col=[0])
    load_forecast.index = pd.to_datetime(load_forecast.index, utc=True)
    load_forecasts += [load_forecast]

    load = pd.read_csv('data/load_'+country_code+'.csv', index_col=[0])
    load.index = pd.to_datetime(load.index, utc=True)
    loads += [load]

    generation = pd.read_csv('data/generation_'+country_code+'.csv', index_col=[0])

    generation_forecast = pd.read_csv('data/generation_forecast_'+country_code+'.csv', index_col=[0])
    generation_forecast.index = pd.to_datetime(generation_forecast.index, utc = True)
    generation_forecasts += [generation_forecast]

    wind_and_solar_generation_forecast = pd.read_csv('data/wind_generation_forecast_'+country_code+'.csv', index_col=[0])
    wind_and_solar_generation_forecast.index = pd.to_datetime(wind_and_solar_generation_forecast.index, utc=True)
    wind_and_solar_generation_forecast += [wind_and_solar_generation_forecast]


    # PLOT BOKEH

    data = {
    'Date': np.array(imbPrice2020.index, dtype=np.datetime64),
    'Upward_price': np.array(imbPrice2020['SE4']['Up']),
    'Downward_price': np.array(imbPrice2020['SE4']['Down']),
    'Upward_volume': np.array(imbVol2020['SE4']['Up']),
    'Downward_volume': np.array(imbVol2020['SE4']['Down']),
    'Day': np.array(imbPrice2020.index.strftime('%A'))
    }

source = ColumnDataSource(data=data)

hover = HoverTool(
    tooltips=[
        ('Date', '@Date{%F}'),
        ('Upward Price', 'SEK @Upward_price{%0.2f}'),
        ('Upward Volume', '@Upward_volume MWh'),
        ('Downward Price', 'SEK @Downward_price{%0.2f}'),
        ('Downward Volume', '@Downward_volume MWh'),
        ('Day', '@Day')
    ],
    formatters ={
        '@Date': 'datetime',
        '@Upward_price': 'printf',
        '@Upward_volume': 'printf',
        '@Downward_price': 'printf',
        '@Downward_volume': 'printf'

    },
    mode='vline'
)
plot_options = dict(x_axis_type='datetime', width=1100, plot_height=200, tools=[hover, 'pan,wheel_zoom,box_zoom,crosshair,reset'])

p_price_up = figure(title='Upward regulation price', **plot_options)
p_vol_up = figure(x_range=p_price_up.x_range, title='Upward regulation Volume', **plot_options)
p_price_dwn = figure(x_range=p_price_up.x_range, y_range=p_price_up.y_range, title='Downward regulation price',**plot_options)
p_vol_dwn = figure(x_range=p_price_up.x_range, title='Downward regulation Volume', **plot_options)

p_price_up.line(x='Date', y='Upward_price', line_width=2, color='navy', alpha=.5, source=source)
p_vol_up.line(x='Date', y='Upward_volume', line_width=2, color='olive', alpha=.5, source=source)
p_price_dwn.line(x='Date', y='Downward_price', line_width=2, color='firebrick', alpha=.5, source=source)
p_vol_dwn.line(x='Date', y='Downward_volume', line_width=2, color='olive', alpha=.5, source=source)

for fig in [p_price_up, p_price_dwn, p_vol_up, p_vol_dwn]:
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_alpha = 0.5

# LABELS = [header[0] for header in list(imbPrice2020)[::2]]

# selector = CheckboxButtonGroup(labels=LABELS, active=[5])
# selector.js_on_click(CustomJS(code="""
#     console.log('checkbox_button_group: active=' + this.active, this.toString())
# """))

p = gridplot([[p_price_up], [p_vol_up], [p_price_dwn], [p_vol_dwn]])
# show(column(selector, p))
show(p)
