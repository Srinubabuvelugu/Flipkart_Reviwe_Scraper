from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

app=Flask(__name__)

@app.route("/",methods=['GET'])
 
def homapage():
    return render_template("FKsearch.html")


@app.route("/reviwe",methods=["POST","GET"])
 
def reviwe():
    if request.method == 'POST':
        try:
            search_ele=request.form['content'].replace(" ","")                          # Search flipkart item
            flipkart_page_url="https://www.flipkart.com/search?q=" + search_ele         ## creating link for search element
            open_webpage=uReq(flipkart_page_url)
            flipkart_page_read=open_webpage.read()
            open_webpage.close()
            flipkart_page_html=bs(flipkart_page_read,"html.parser")
            bigboxes=flipkart_page_html.findAll("div", {"class": "_1AtVbE col-12-12"})
            del bigboxes[:3]
            box=bigboxes[0]
            box_href=box.div.div.div.a['href']
            productlink = "https://www.flipkart.com" + box_href
            productReq=requests.get(productlink)
            productReq.encoding='utf-8'
            product_html=bs(productReq.text,"html.parser")
            commentboxes = product_html.find_all('div', {'class': "_16PBlm"})
            filename = search_ele + ".csv"
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Date, Heading, Comment \n"
            fw.write(headers)

            reviews_list=list()  ## to store the all reviwes in the list

            for comment in commentboxes:

                ### 1. Rating of the product
                
                try: 
                    rating = comment.div.div.div.div.text  
                except Exception as e:
                    rating = 'No rating'
                            
                            ### 2. Product comment Head
                try:
                    commentHead = comment.div.div.div.p.text
                except Exception as e:
                    commentHead = ' No comment Head'

                            ### 3. Product comment
                
                try:
                    comtag=comment.div.div.find_all('div', {'class': ''})
                    com = comtag[0].div.text
                except Exception as e:
                    com = "No comment"

                            ### 4. Reviwer Name
                try:
                    name = comment.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except Exception as e:
                    name = 'No name'

                            ## Date of rating is given
                try:
                    date = comment.div.div.find_all('p', {'class': '_2sc7ZR'})[1].text
                except:
                    date = ' Date Not avilable'

                            ## convert reviwe values into a dictnory
                dic={
                    'S.No' : commentboxes.index(comment)+1 ,
                    'Product Name' : search_ele,
                    'User Name' : name,
                    'Product Reating' : rating,
                    'Reviwe Date' : date,
                    'Reviwe Head' : commentHead,
                    'Product Reviwe' : com
                    }
                reviews_list.append(dic)
            return render_template("FKresult.html",reviews=reviews_list[0:(len(reviews_list)-1)])

        except Exception as e:
            return "Somthing Wrong"
    else:
        return render_template("FKsearch.html")


     

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000, debug=True)