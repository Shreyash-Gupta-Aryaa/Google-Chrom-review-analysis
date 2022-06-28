# -*- coding: utf-8 -*-
"""
Created on Sat Jun 25 17:26:57 2022

@author: shrey
"""

from flask import Blueprint, render_template, session ,request, flash, jsonify,Flask, redirect, url_for
from flask_login import login_required, current_user

import os
import pandas as pd

# importing libraries for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from nltk.stem import WordNetLemmatizer 
from textblob import TextBlob





# defining that this file is the blueprint of our website
views = Blueprint('views',__name__)

app = Flask(__name__)  
# defninig our first view or root 
            #('URL to get to this endpoint')

    
@views.route('/upload') 
@login_required 
def upload():  
    return render_template("home.html",user = current_user)  
 
@views.route('/success', methods = ['POST'])  
@login_required
def success():  
    if request.method == 'POST':  
        f = request.files['file'] 
        if f.filename != '':
            #f.filename='input.csv'
            UPLOAD_FOLDER = 'D:/Flask/Assignment/website/files'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
           
            # Storing uploaded file path in flask session
            session['uploaded_data_file_path'] = file_path
 
            f.save(file_path)  
            flash('File uploaded!', category='success')
            
            
            return redirect(url_for("views.process"))
        else:
            flash("File upload unsuccessful",category = 'error')
    return render_template("home.html", user=current_user)  
  


@views.route('/process')
@login_required
def process():
    file_path = session.get('uploaded_data_file_path', None)
    
    data = pd.read_csv(file_path)
    
    # making object
    
    lemmatizer = WordNetLemmatizer()  

    # setting stop words
    stop_word = set(stopwords.words('english'))
    stop_word.remove('not')
    stop_word.remove('no')


    clean_text =[]
    for review in data['Text']:
        review= re.sub(r'[^\w\s]', '', str(review))
        review = re.sub(r'\d','',review)
        review_token = word_tokenize(review.lower().strip()) #convert reviews into lower case and strip leading and tailing spaces followed by spliting sentnece into words
        review_without_stopword=[]
        for token in review_token:
            if token not in stop_word:
                token= lemmatizer.lemmatize(token)
                review_without_stopword.append(token)
        cleaned_review = " ".join(review_without_stopword)
        clean_text.append(cleaned_review)
                
                
    data["cleaned_review"] = clean_text
    Single_star_review = data[data.Star <=2 ]


    sia = SentimentIntensityAnalyzer()
    sentiment_list = []

    

    for i in Single_star_review["cleaned_review"]:
        score = sia.polarity_scores(i)
        blob_score = TextBlob(i).sentiment.polarity
        if (score['pos'] >= 0.7):
            sentiment_list.append('Positive')
        else:
            sentiment_list.append('Negative/Neutral')
        
    Single_star_review["sentiment"]= sentiment_list


    positive_review_with_1_2_star = Single_star_review[Single_star_review.sentiment == 'Positive']
    positive_review_with_1_2_star.drop("cleaned_review",axis = 1,inplace=True)


    final = positive_review_with_1_2_star.copy()
    final.drop(['Review URL','Thumbs Up','Developer Reply','Version','Review Date','App ID','sentiment'],axis=1,inplace=True)
    final = final.sample(frac=1)
    # pandas dataframe to html table flask
    uploaded_df_html = final.to_html()
    
    return render_template('process.html', data_var = uploaded_df_html,user= current_user)
    


