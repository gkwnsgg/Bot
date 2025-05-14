import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "./GodoM.otf"
font_prop = fm.FontProperties(fname=font_path)

print("폰트 이름:", font_prop.get_name())

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False