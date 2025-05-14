import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = "./Godo M.otf"
font_prop = fm.FontProperties(fname=font_path)

print("폰트 이름:", font_prop.get_name())

plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False
plt.plot([1, 2, 3], [1, 4, 9])
plt.title("한글 테스트")
plt.savefig("test_plot.png")