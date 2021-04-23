import os
import h5py
import dash
import dash_html_components as html

import numpy as np
import pandas as pd

import datashader as ds
import holoviews as hv
from holoviews import opts
from holoviews.plotting.plotly.dash import to_dash
from holoviews.operation.datashader import datashade, shade, dynspread, spread, rasterize


def read_file(*args, header = True):
    print(*args, header)
    file = os.path.join(*args)
    if os.path.exists(file) and os.path.isfile(file):
        if file.endswith('.pickle'):
            return pd.read_pickle(file)
        if header:
            print('header')
            return pd.read_csv(file, sep="\s+")
        else:
            print('no header')
            return pd.read_csv(file, sep="\s+", header=None)
    else:
        return pd.DataFrame()

def read_merge_dnb_file(file_dir, bin_size):
    merge_file = os.path.join(file_dir, 'dnb_merge', 'merge_dnb_bin{0}.pickle'.format(bin_size))
    return read_file(merge_file)

def read_merge_dnb_file_from_h5(file_dir, bin_size):
    h5_file = os.path.join(file_dir, 'stereomics.h5')
    dnb_df = pd.DataFrame()
    if os.path.exists(h5_file):
        h5_f = h5py.File(h5_file, 'r')
        try:
            dnb_df = pd.DataFrame(h5_f['dnb_merge'][f'bin{bin_size}'][()], columns = ['x','y','values','gene_counts'])
            return dnb_df
        except Exception as e:
            print(e)
        finally:
            h5_f.close()
    return pd.DataFrame()

def df_to_dataset(df):
    return hv.Dataset(df)

def polt_rasterize_dnb_figure(dataset, colormap, width=900, height=600):
    return rasterize(
        hv.Scatter(dataset, kdims=["x"], vdims=['y','values']),
        aggregator=ds.sum('values')
    ).opts(
        width=width,
        height=height,
        cmap=colormap,
        colorbar=True
    )

def plot_datashade_dnb_figure(dataset, colormap, width=900, height=600):
    return datashade(
        hv.Scatter(dataset, kdims=["x"], vdims=['y','values']),
        aggregator=ds.sum('values'),
        cmap=colormap,
    ).opts(
        width=width,
        height=height,
    )



def set_width_height(plot, element):
    fig = plot.state
    fig['layout']['width'] = 600
    fig['layout']['height'] = 800

# file = r'E:\01.program\11.st_RNA\03.data\20201202\DP8400014115BR_C3_h5_new\stereomics.h5'

# file = r'E:\01.program\11.st_RNA\03.data\batch30\dnb_merge\merge_dnb_bin1.pickle'


app = dash.Dash(__name__)
components = to_dash(app, [scatter], reset_button=True)

app.layout = html.Div(components.children)

if __name__ == '__main__':
    app.run_server(debug=True)