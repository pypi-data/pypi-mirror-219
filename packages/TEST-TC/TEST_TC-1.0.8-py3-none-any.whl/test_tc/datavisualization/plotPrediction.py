import numpy as np
import pandas as pd

import plotly
import plotly.express as px
import plotly.graph_objects as go

def obtain_dataset(df: pd.DataFrame, gerarchia: str, id_pred: str):

    """generate list of prediction dataframe for gerarchy specified

    df : pd.DataFrame
        prediction dataframe
    gerarchia : str
        hierarchy selected
    id_pred : str
        name of id pred column

    Returns
    -------
    _type_
        _description_
    """

    if gerarchia == "Italia":
        n_level = len(gerarchia.split("/")) - 1
        split = np.array_split(df,df[id_pred].unique().shape[0])
        result = [i for i in split if i[id_pred].unique()[0].count("/") == n_level]
    else:
        n_level = len(gerarchia.split("/")) 
        split = np.array_split(df,df[id_pred].unique().shape[0])
        
        select = [i for i in split if i[id_pred].unique()[0].count("/") <= n_level]
        result = [i for i in select if gerarchia in i[id_pred][0]]
    
    return result

class plotPrediction():

    """class for plot prediction,result of job
    """

    def __init__(self, id_pred: str, data: str, pred_mean: str, pi_lower: str, pi_upper: str, use_case: str):
        
        self.id_pred = id_pred
        self.data = data
        self.pred_mean = pred_mean
        self.pi_lower = pi_lower
        self.pi_upper = pi_upper
        self.use_case = use_case

    def plot_pred(self, df_pred: pd.DataFrame, id_pred: str = None,
                  df_real: pd.DataFrame = None, data_real: str = None, target: str = None, confidence_interval: bool = False) -> plotly.graph_objs._figure.Figure:
            
        """Plot prediction

        Parameters
        ----------
        df_pred : pd:DataFrame
            dataframe of prediction
        id_pred : str 
            id of prediction to be considered
        df_real : pd.DataFrame
            dataframe of real data
        target : str
            name column of real values

        Results
        -------
        plotly.graph_objs._figure.Figure
            plot prediction
        """
            
        if id_pred:
            lista_id = [id_pred]
        else:
            lista_id = df_pred[self.id_pred].unique()

        lista_fig = []
        for id_pre in lista_id:
            regione = id_pre

            df_pred_parz = df_pred[df_pred[self.id_pred] == id_pre]

            if not isinstance(df_real,type(None)):
                df_real_parz = df_real[df_real[self.id_pred] == id_pre]
                real = [go.Scatter(
                        x=df_real_parz[data_real],
                        y=df_real_parz[target],
                        marker=dict(color="blue"),
                        mode="lines",
                        name="past value (true)",showlegend=True
                    )]
            else:
                real = []

            fig = px.line(
                df_pred_parz,
                x=self.data,
                y=self.pred_mean,
                color_discrete_sequence=["green"],
                labels={self.data: "", self.pred_mean: f"numero {self.use_case}"},
                title=f"Predizione {self.use_case} - {regione}",
                width=800,
                height=500,
                template=dict(
                    layout=go.Layout(
                    title_font=dict(family="Rockwell", size=24, color="gray"),
                    title_x=0,
                    font=dict(color="green"),
                    )
                ),
            )

            fig.data[0].name = "predict value"
            fig.update_traces(showlegend=True)

            if confidence_interval:
                fig.add_traces(
                    [
                        go.Scatter(
                            x=df_pred_parz[self.data],
                            y=(df_pred_parz[self.pi_lower]),
                            mode="lines",
                            line_color="rgba(0,0,0,0)",
                            showlegend=False,
                        ),
                        go.Scatter(
                            x=df_pred_parz[self.data],
                            y=(df_pred_parz[self.pi_upper]),
                            mode="lines",
                            line_color="rgba(0,0,0,0)",
                            name="95% confidence interval",
                            fill="tonexty",
                            fillcolor="rgba(124, 252, 0, 0.2)",
                            showlegend=True,
                        )
                    ] 
                )

            fig.add_traces(real)

            fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

            lista_fig += [fig]

        return lista_fig

    def plot_hierarchical(self, df_pred: pd.DataFrame, gerarchia: str):

        """Plot a set of hierarchical time series

        Parameters
        ----------
        lista_df_pred : list
            list of dataframe of prediction for the low level of hierarchy
    
        Returns
        -------
        plotly.graph_objs._figure.Figure
            plot a set hierarchical time series
        """

        lista_df_pred = obtain_dataset(df_pred,gerarchia,self.id_pred)

        fig = go.Figure(
            layout=dict(
                template="plotly_white",
                title_font=dict(family="Rockwell", size=24, color="gray"),
                font=dict(color="green"),
                title=dict(text=f"Predizione gerarchia {self.use_case}"),
                legend=dict(yanchor="bottom", y=0, xanchor="left", x=-0.5),
                yaxis_title=f"numero {self.use_case}",
            )
        )

        list_fig = [
            go.Scatter(
                x=pred[self.data],
                y=pred[self.pred_mean],
                mode="lines",
                name=pred["Id_pred"][0],
                showlegend=True,
            )
            for pred in lista_df_pred
        ]

        # list_fig = [go.Scatter(x=pred[data],y=pred[pred_mean],marker=dict(color=col),mode="lines",name=pred['Id_pred'][0],showlegend=True)
        #             for pred, col in zip(lista_df_pred,["red","blue"])]

        fig.add_traces(list_fig)

        return fig

    def plot_sum_hierarchy(self, df_pred: pd.DataFrame, gerarchia: str):
        
        """Plot sum of hierarchical time series

        Parameters
        ----------
        df_pred : pd.DataFrame
            dataframe of high level of hierarchy
        lista_df_pred : list
            list of dataframe of prediction for the low level of hierarchy
        livello : str
            name of low level hierarchy

        Returns
        -------
        plotly.graph_objs._figure.Figure
            plot of sum hierarchical time series
        """

        lista_df_pred = obtain_dataset(df_pred,gerarchia,self.id_pred)
        
        df_pred_tot = lista_df_pred[0]
        lista_df_pred = lista_df_pred[1:]

        tot_hier_pred = pd.concat(lista_df_pred, axis=1)[self.pred_mean].sum(axis=1)

        fig = go.Figure(
            layout=dict(
                template="plotly_white",
                title_font=dict(family="Rockwell", size=24, color="gray"),
                font=dict(color="green"),
                title=dict(text=f"Predizione gerarchia aggregata {self.use_case}"),
                legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                yaxis_title=f"numero {self.use_case}",
            )
        )

        fig.add_traces(
            [
                go.Scatter(
                    x=df_pred_tot[self.data],
                    y=df_pred_tot[self.pred_mean],
                    marker=dict(color="green"),
                    mode="lines",
                    name=f"Predizione {df_pred_tot['Id_pred'][0]}",
                    showlegend=True,
                ),
                go.Scatter(
                    x=df_pred_tot[self.data],
                    y=tot_hier_pred.values,
                    marker=dict(color="blue"),
                    mode="lines",
                    name=f"Somma predizioni {df_pred_tot['Id_pred'][0]}",
                    showlegend=True,
                ),
            ]
        )

        return fig
