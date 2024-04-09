import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np
import re
import time
import psycopg2

def image_to_text(path):
    input_pic=Image.open(path)
    img_array=np.array(input_pic)

    reader=easyocr.Reader(['en'])
    text=reader.readtext(img_array,detail=0)
    return text

def extract_text(texts):
    extract_dic = {
        "Name": [],"Designation": [],"Company_Name": [],"Contact": [],"EMail": [],"Website": [],"Address": [],"Pincode": []}

    extract_dic["Name"].append(texts[0])
    lower = texts[1].lower()
    extract_dic["Designation"].append(lower)

    for i in range(2, len(texts)):
        if texts[i].startswith("+") or '-' in texts[i] or (texts[i].replace("-", " ").isdigit() and '-' in texts[i]):
            extract_dic["Contact"].append(texts[i])
            
        elif '@' in texts[i] and '.com' in texts[i]:
            extract_dic["EMail"].append(texts[i])
            
        elif 'www' in texts[i] or 'WWW' in texts[i] or 'wwW' in texts[i] or 'Www' in texts[i]:
            lower = texts[i].lower()
            extract_dic["Website"].append(lower)
            
        elif 'TamilNadu' in texts[i] or 'Tamil Nadu' in texts[i] or texts[i].isdigit():
            extract_dic["Pincode"].append(texts[i])
            
        elif re.match(r'^[A-Z a-z]', texts[i]):
            extract_dic["Company_Name"].append(texts[i])
            
        else:
            removeextra=re.sub(r'[,;]','',texts[i])
            extract_dic["Address"].append(removeextra)
            
    for key , value  in extract_dic.items():
        if len(value)>0:
            concad="".join(value)
            extract_dic[key]=[concad]
        else:
            value ="NA"
            extract_dic[key]=[value]         
            
    return extract_dic


st.set_page_config(layout="wide")

with st.sidebar:   
    
    st.image("OCRR.png") 
    selected = option_menu("Main Menu", ["Intro",'Upload Image','View & Modify','Delete','Contact Us'], 
        icons=['house','upload','pencil-square','download','phone'])

if selected=="Intro":
    st.title("*:green[Welcome to Boopathi's BizCardX] :sunglasses:*")
    
    
elif selected=="Upload Image":                  
    uploaded_files = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_files is not None:
        st.image(uploaded_files,width=330)  
        
        text_img = image_to_text(uploaded_files)
        text_dict = extract_text(text_img)
        
        if text_dict:
            st.success("Text is Extracted Successfully")
            df = pd.DataFrame(text_dict)
            st.dataframe(df)
            
        button1=st.button(":red[Save Text]",use_container_width=True)
        
        if button1:            
            mydb = psycopg2.connect(host="localhost",
                user="postgres", password="758595",
                database="bizcard",port="5432")
            cursor = mydb.cursor()

            create_table = '''create table if not exists bizcard_details(
                                name varchar(99),designation varchar(99),
                                company_name varchar(99),contact varchar(99),
                                email varchar(99),website text,
                                address text,pincode varchar(99))'''

            cursor.execute(create_table)
            mydb.commit()            
            cursor = mydb.cursor()
            insert_data = '''insert into bizcard_details(name,designation,company_name,contact,
                                email,website,address,pincode) values(%s,%s,%s,%s,%s,%s,%s,%s)'''
            data =df.values.tolist()
            cursor.executemany(insert_data, data)
            mydb.commit()
            st.success("Above the Text data Inserted Successfully")
            
elif selected=="View & Modify":                 
    selected_option = st.selectbox("View or Modify options", ["Select Below Options", "Preview text", "Modify text"])
    if selected_option == "Select Below Options":
        pass
    elif selected_option == "Preview text":
                    mydb = psycopg2.connect(host="localhost",
                                            user="postgres", password="758595",
                                            database="bizcard",port="5432")
                    cursor = mydb.cursor()                
                    select_data="select * from bizcard_details"
                    cursor.execute(select_data)
                    table=cursor.fetchall()
                    mydb.commit()
                    table_df=pd.DataFrame(table,columns=("name","designation","company_name","contact","email","website","address","pincode"))
                    table_df
        
    elif selected_option == "Modify text":
        pass   

elif selected=="Contact Us":
    
    st.title("Contact Us")
    
    coll1, coll2 = st.columns(2)

    with coll1: 
        st.subheader('Boopathi Venkatachalam :sunglasses:')
        st.caption('Mobile:- 9751959575, E-Mail - boopathi762000@gmail.com')

        st.caption(":red[Note: * fill all mandatory fields]")     
        Name = st.text_input("Name*")
        Mobile = st.text_input("Mobile*")
        Email = st.text_input("Email*")
        Message = st.text_area("Message (optional)")

        if st.button("Submit"):
            st.success('''Thank you for your Valuable Rationg and Message !
                        We will get back to you soon''')
    
          
    with coll2:
        st.image('photo.jpg')
        st.link_button("Git Hub", "https://streamlit.io/gallery")
        st.link_button("Linked in", "https://streamlit.io/gallery")
        st.link_button("Whatsapp", "https://streamlit.io/gallery")
        st.link_button("E-Mail", "https://streamlit.io/gallery")

  


