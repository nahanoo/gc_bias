import numpy as np
import plotly.express as px
import numpy as np

class Plotting():
    def density_plot(self,df):
        """Plotting 2d histogram for gc content and coverage.
        Cut off for coverage is required because there are some few very high coverage areas
        making the plot useless for low coverage interpretations."""
        self.heatmap = px.density_heatmap(df,x='coverage',y='gc_content',\
            nbinsy=20,width=1057.92*0.8,height=595.2*0.8)

    def distribution(self,df,end):
        """Plotting histogram of coverage to get more detailled view."""
        start = int(df['depth'].min())
        size = 10
        end = int(end)

        #Making a histogram
        largest_value = df['depth'].max()
        if largest_value > end:
            hist = np.histogram(df['depth'], bins=list(range(start, end+size, size)) + [largest_value])
        else:
            hist = np.histogram(df['depth'], bins=list(range(start, end+size, size)) + [end+size])

        #Adding labels to the chart
        labels = []
        for i, j in zip(hist[1][0::1], hist[1][1::1]):
            if j <= end:
                labels.append('{} - {}'.format(i, j))
            else:
                labels.append('> {}'.format(i))

        #Plotting the graph
        self.histogram =  px.bar(x=labels,y=hist[0])

    def update_labels(self,plot,labels):
        """This function can be used to update all labels of a plotly figure."""
        plot.update_layout(
            title = labels['title'],
            xaxis_title = labels['xlabel'],
            yaxis_title= labels['ylabel'],
            template = labels['theme']
            )