from toolbox.images import *
i = draw_text("test", font_size=72, font_file=r"C:\Windows\Fonts\msyh.ttc")
print(i)
print(get_bounding_box(i))
i.save("sample.png")