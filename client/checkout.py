from flask import Flask
from flask import render_template


def add_new_route(app):
    
    @ app.route('/checkout.html',methods=['GET','POST'])
    def checkout():
        goodlsit = [{'name':'food','price':500,'num':2},{'name':'food','price':500,'num':2}]
        return render_template("checkout.html",goodlist = goodlsit)




