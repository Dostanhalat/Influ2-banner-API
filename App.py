from flask import Flask, render_template, request, jsonify, url_for, redirect
from selenium import webdriver
from PIL import Image
app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        link = request.form.get('link')
        return redirect(url_for('result', link = link))
    return render_template('index.html')


@app.route('/result')
def result():
    link = request.args.get('link')
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("disable-infobars")
        wd = webdriver.Chrome('chromedriver',options=chrome_options)
        wd.get(str.format(link))

        wd.get_screenshot_as_file(r"screenshots/screenshot.png")
        #Loading in the screenshot
        im = Image.open(r"screenshots/screenshot.png").convert("RGB", palette = Image.ADAPTIVE, colors = 16)
        pix = im.load()

        x = im.size[0]
        y = im.size[1]
        
        #Putting all of the pixels in a list
        values = list()
        for x in range(x):
            for y in range(y):
                values.append([pix[x,y][0], pix[x,y][1], pix[x,y][2]])
        values.sort()

        #Creating a new list with all of the values and their amounts
        counter = 0
        lastValue = None
        newValues = list()
        for value in values:
            if lastValue == None:
                lastValue = value
            if lastValue !=  value:
                newValues.append([counter,str(lastValue)[1:-1]])
                counter = 0
                lastValue = value
            else:
                counter += 1
        newValues.sort(reverse=True)
        return render_template('result.html', c1 = newValues[0][1], c2 = newValues[1][1], c3 = newValues[2][1], c4 = newValues[3][1],c5 = newValues[4][1])
    except:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)