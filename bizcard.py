import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import pandas as pd
import numpy as np


def image_to_text(path):
    input_pic=Image.open(path)
    img_array=np.array(input_pic)

    reader=easyocr.Reader(['en'])
    text=reader.readtext(img_array,detail=0)

    return text


import re

def extract_text(texts):
    extract_dic = {
        "Name": [],
        "Designation": [],
        "Company_Name": [],
        "Contact": [],
        "EMail": [],
        "Website": [],
        "Address": [],
        "Pincode": []
    }

    extract_dic["Name"].append(texts[0])
    extract_dic["Designation"].append(texts[1])

    for i in range(2, len(texts)):
        if texts[i].startswith("+") or (texts[i].replace("-", " ").isdigit() and '-' in texts[i]):
            remove = texts[i].replace("-", " ")
            extract_dic["Contact"].append(remove)
            
        elif '@' in texts[i] and '.com' in texts[i]:
            extract_dic["EMail"].append(texts[i])
            
        elif 'www' in texts[i] or 'WWW' in texts[i]:
            lower = texts[i].lower()
            extract_dic["Website"].append(lower)
            
        elif 'TamilNadu' in texts[i] or 'Tamil Nadu' in texts[i] or texts[i].isdigit():
            extract_dic["Pincode"].append(texts[i])
            
        elif re.match(r'^[A-Z a-z]', texts[i]):
            extract_dic["Company_Name"].append(texts[i])
            
        else:
            extract_dic["Address"].append(texts[i])

    return extract_dic
