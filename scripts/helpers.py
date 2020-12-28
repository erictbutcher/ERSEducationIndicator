import pandas as pd
import plotly.graph_objs as go
from sklearn.linear_model import LinearRegression
import json
from urllib.request import urlopen

#Regression
def county_wide_regression(data,dataset):
    preds = pd.DataFrame()
    for fip in data['fips'].unique():
        tmp = data.loc[(data['fips']==fip)&(data['Dataset']==dataset)][['1970', '1980', '1990', '2000', '2018']]
        tmp = tmp[tmp.columns[~tmp.isnull().all()]]
        x = tmp.values[0]
        if len(x) > 1:
            x = x.reshape((len(x),1))
            model = LinearRegression().fit(pd.DataFrame(tmp.columns.values).values.reshape(len(x),1),x)
            y_pred = model.predict([[2030],[2040]])
            preds=pd.concat([preds, pd.DataFrame({'fips':fip,'2030':y_pred[0],'2040':y_pred[1]})])
        else:
            print(fip)

    preds['Dataset'] = dataset
    return preds

#animated Choroplethmapbox
def animated_map(data):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    years = ['1970', '1980', '1990', '2000', '2018', '2030', '2040']
    fig_data =go.Choroplethmapbox(geojson=counties, locations=data['fips'].values,
                                  z=data[years[0]].values,
                                  zmin=0,
                                  zmax=100,
                                  name="",
                                  colorscale="blues", #ylgn
                                  marker_opacity=0.7,
                                  marker_line_width=0,
                                  customdata = data[['County_Name','State']],
                                  hovertemplate='%{customdata}<br>%{z}%')
    fig_layout = go.Layout(mapbox_style="carto-positron",
                           mapbox_zoom=2.5,
                           mapbox_center={"lat": 37.0902, "lon": -95.7129},
                           margin={"r":0,"t":0,"l":0,"b":0},
                           plot_bgcolor=None)

    fig_layout["updatemenus"] = [
        dict(type="buttons",
             buttons=[dict(label="Play",
                           method="animate",
                           args=[None,
                                 dict(frame=dict(duration=1000,
                                                 redraw=True),
                                      fromcurrent=True)]),
                      dict(label="Pause",
                           method="animate",
                           args=[[None],
                                 dict(frame=dict(duration=0,
                                                 redraw=True),
                                      mode="immediate")])],
             direction="left",
             pad={"r": 10, "t": 35},
             showactive=False,
             x=0.1,
             xanchor="right",
             y=0,
             yanchor="top")]

    sliders_dict = dict(active=0,
                        visible=True,
                        yanchor="top",
                        xanchor="left",
                        currentvalue=dict(font=dict(size=20),
                                          prefix="Date: ",
                                          visible=True,
                                          xanchor="right"),
                        pad=dict(b=10,t=10),
                        len=0.875,
                        x=0.125,
                        y=0,
                        steps=[])

    fig_frames = []
    for year in years:
        tmp_z = data[year].values
        frame = go.Frame(
            data=[
                go.Choroplethmapbox(
                    locations=data['fips'].values,
                    z=tmp_z,
                    name="",
                    customdata = data[['County_Name','State']],
                    hovertemplate='%{customdata}<br>%{z}%'
                )
            ],name=year)
        fig_frames.append(frame)

        slider_step = dict(args=[[year],
                                 dict(mode="immediate",
                                      frame=dict(duration=1000,
                                                 redraw=True))],
                           method="animate",
                           label=year)
        sliders_dict["steps"].append(slider_step)

    fig_layout.update(sliders=[sliders_dict])
    # Plot the figure
    fig=go.Figure(data=fig_data, layout=fig_layout, frames=fig_frames)
    return fig
