import os
import torch
import pandas as pd
import scanpy as sc
from sklearn import metrics
import multiprocessing as mp
import matplotlib.pyplot as plt
import seaborn as sns

def batch_effect(adata):
    """\
    Draw the batch effects figures in multi-sample integration task.
    """
    fig, ax_list = plt.subplots(1, 3, figsize=(14, 4))

    # do pca reduction
    sc.pp.normalize_total(adata)
    sc.pp.log1p(adata)
    sc.pp.pca(adata)
    ### Plotting UMAP before batch effect correction
    sc.pp.neighbors(adata, use_rep='X_pca', n_neighbors=10, n_pcs=40)
    sc.tl.umap(adata)
    sc.pl.umap(adata, color='data', title='Uncorrected data',
                    ax = ax_list[0],
                    show=False)

    ### Plotting UMAP after batch effect correction
    sc.pp.neighbors(adata, use_rep='embedding', n_neighbors=10)
    sc.tl.umap(adata)
    sc.pl.umap(adata,
            color='data',
            ax=ax_list[1],
            title='Batch corrected',
            #legend_loc = 'bottom margin',
            show=False)

    ### Color by predicted labels
    sc.pl.umap(adata, color='pre_label', ax=ax_list[2], title='Spatial clustering', show=False)

    plt.tight_layout(w_pad=0.02)
    
def split_cluster(adata):
    """\
    Draw the spatial clustering figures for each section in multi-sample intergration task.
    """
    adata_section1 = adata[adata.obs['data']=='Section 1', :]
    adata_section2 = adata[adata.obs['data']=='Section 2', :]
    rgb_values = sns.color_palette("husl", len(adata.obs['pre_label'].unique())) # husl  bright  
    color_fine = dict(zip(list(adata.obs['pre_label'].unique()), rgb_values))
    fig, ax_list = plt.subplots(1, 2, figsize=(9, 4))
    sc.pl.embedding(adata_section1,
                basis='spatial',
                color='pre_label',
                show = False,
                s=70,
                title='Section 1',
                palette=color_fine,
                ax = ax_list[0])

    sc.pl.embedding(adata_section2,
                basis='spatial',
                color='pre_label',
                show = False,
                s=70,
                title = ['Section 2'],
                palette=color_fine,
                ax = ax_list[1])

    plt.tight_layout(w_pad=0.3)
       
def integrate_cluster(adata):
    """\
    Draw the joint spatial clustering figure for each section in multi-sample intergration task.
    """

    adata.obsm['spatial'][:,1] = -1*adata.obsm['spatial'][:,1]
    rgb_values = sns.color_palette("bright", len(adata.obs['pre_label'].unique())) # husl  tab20
    color_fine = dict(zip(list(adata.obs['pre_label'].unique()), rgb_values))

    plt.rcParams["figure.figsize"] = (12, 6)
    sc.pl.embedding(adata, basis="spatial",
                    color="pre_label",
                    s=100,
                    palette=color_fine,
                    show=False,
                    title='Mouse Anterior & Posterior Brain (Section 1)')