import pandas as pd
import matplotlib.pyplot as plt

def save_sah_df_img(df, filename="2506.png", background_image="1747197564.219887.PNG"):
    fig, ax = plt.subplots(figsize=(10, len(df) * 0.5 + 2))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=["#d3d3d3"] * df.shape[1])
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)
    if background_image:
        img = plt.imread(background_image)
        fig.figimage(img, xo=0, yo=0, alpha=0.2, zorder=1)
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()