from  flask import Flask,request,redirect,render_template_string
import string,random
app=Flask(__name__)
url_map={}

home_page="""
<!doctype html>
<title>URL SHORTENER</title>
<h1> Simple URL shortener</h1>
<form method="POST" action="/">
Original URL:<input type="text" name ="original_url" required>
<input type ="submit" value="shorten">
</form>
{% if short_url %}
<p> Short URL:<a href="{{short_url}}"target="_blank">{{ short_url }}</a></p>
{% endif %}
"""
def generate_short_code(length=6):
    charectars=string.ascii_letters+string.digits
    while True:
        code=''.join(random.choice(charectars) for _ in range (length))
        if code not in url_map:
            return code
@app.route('/',methods =['GET','POST'])
def home():
    short_url= None
    if request.method == 'POST':
        original_url=request.form['original_url']
        if not original_url.startswith(('http://','https://')):
            original_url='http://'+original_url
        code=generate_short_code()
        url_map[code]=original_url
        short_url=request.host_url+code
    return render_template_string(home_page,short_url=short_url)
@app.route('/<code>')
def redirect_to_url(code):
    original_url=url_map.get(code)
    if original_url:
        return redirect(original_url)
    else :
        return "URL  NOT FOUND",404
if __name__=='__main__':
    app.run(debug=True)
