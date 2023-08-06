import draw,colours,origins,fonts

app = draw.window()

box = draw.textbox(app,"5","5",30)

while app.running():
    app.update()