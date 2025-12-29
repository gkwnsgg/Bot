import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import textwrap

font_path = "./GodoM.ttf"
fontprop = fm.FontProperties(fname=font_path)
plt.rcParams['axes.unicode_minus'] = False

def auto_wrap_text(text, max_line_length=18):
    if not isinstance(text, str):
        return text
    return '\n'.join(textwrap.wrap(text, width=max_line_length))
def wrap_text_in_df(df, max_line_length=18):
    return df.applymap(lambda x: auto_wrap_text(x, max_line_length))

def save_sah_df_img(df, filename="2512.png", background_image="1747197564.219887.PNG"):
    df = wrap_text_in_df(df, max_line_length=18)
    print(df[['날짜']])
    row_count = len(df) + 1
    row_height = 0.5
    fig_width = 16
    fig_height = max(8, row_count * row_height)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center',
        colColours=["#d3d3d3"] * df.shape[1]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 0.8)

    cell_texts = [df.columns.tolist()] + df.values.tolist()
    max_line_count_per_row = [
        max(str(cell).count('\n') + 1 if isinstance(cell, str) else 1 for cell in row)
        for row in cell_texts
    ]
    for (row, col), cell in table.get_celld().items():
        cell.get_text().set_fontproperties(fontprop)
        cell.PAD = 0.01
        line_count = max_line_count_per_row[row]
        if row == 0:
            cell.set_height(0.18)
        else:
            base_height = 0.15
            line_height = 0.05
            cell.set_height(base_height + (line_count - 1) * line_height)
    if background_image:
        img = plt.imread(background_image)
        fig.figimage(img, xo=100, yo=100, alpha=0.2, zorder=1)
    fig.subplots_adjust(bottom=0.1, top=0.95)
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()