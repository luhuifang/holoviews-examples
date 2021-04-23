# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
from plotly.data import iris

import holoviews as hv
from holoviews import opts
from holoviews.plotting.plotly.dash import to_dash

df = iris()
dataset = hv.Dataset(df)

selection_linker = hv.selection.link_selections.instance()
scatter = selection_linker(
    hv.Scatter(dataset, kdims=['sepal_length'], vdims=['sepal_width'])
)

hist = selection_linker(
    hv.operation.histogram(dataset, dimension='sepal_width', normed=False)
)

def set_dragmode(plot, element):
    fig = plot.state
    # print(element)
    # print(len(fig['data'][0]['x']))
    fig['layout']['dragmode'] = 'select'
    if isinstance(element, hv.Histogram):
        fig['layout']['selectdirection'] = 'h'

scatter.opts(opts.Scatter(hooks = [set_dragmode]))
hist.opts(opts.Histogram(hooks = [set_dragmode]))

app = dash.Dash(__name__)
components = to_dash(
    app, [scatter, hist], reset_button=True
)

app.layout = html.Div(components.children)

if __name__ == "__main__":
    app.run_server(debug=True)