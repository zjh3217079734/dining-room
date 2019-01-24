from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/index2')
def index2():
    return render_template('index2.html')

@app.route('/about-us')
def about_us():
    return render_template('about-us.html')

@app.route('/blog-details-gallery')
def blog_details_gallery():
    return render_template('blog-details-gallery.html')

@app.route('/blog-details')
def blog_details():
    return render_template('blog-details.html')

@app.route('/blog-rightsidebar')
def blog_rightsidebar():
    return render_template('blog-rightsidebar.html')
    
@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/cart-page')
def cart_page():
    return render_template('cart-page.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login-register')
def login_register():
    return render_template('login-register.html')

@app.route('/my-account')
def my_account():
    return render_template('my-account.html')

@app.route('/product-details')
def product_details():
    return render_template('product-details.html')

@app.route('/reset-password')
def reset_password():
    return render_template('reset-password.html')

@app.route('/shop-list')
def shop_list():
    return render_template('shop-list.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/wishlist')
def wishlist():
    return render_template('wishlist.html')

if __name__ == '__main__':
    app.run(debug=True ,port=8001)
