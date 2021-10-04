import numpy as np
import plotly.express as px
import pandas as pd
import json

class Plotting():
    def density_plot(self,df):
        """Plotting 2d histogram for gc content and coverage.
        Cut off for coverage is required because there are some few very high coverage areas
        making the plot useless for low coverage interpretations."""
        counts,values = np.histogram(df['coverage'])
        min_count = 200
        for i,count in enumerate(counts):
            if count < min_count:
                break
        cut_off = values[i]
        self.heatmap = px.density_heatmap(df,x='gc_content',y='coverage',\
            marginal_x="histogram",marginal_y="histogram",range_y=[0,cut_off],\
            nbinsx=20,nbinsy=10)

    def update_labels(self,json_f):
        """This function can be used to update all labels of a plotly figure."""
        with open(json_f,'r') as handle:
            data = handle.read()
        labels = json.loads(data)

        self.heatmap.update_layout(
            title = labels['title'],
            xaxis_title = labels['xlabel'],
            yaxis_title= labels['ylabel'],
            template = labels['theme'])