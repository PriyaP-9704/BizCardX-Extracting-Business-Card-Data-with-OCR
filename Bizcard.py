import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import numpy as np
import pandas as pd
import re
import io


def image_to_text(path):

    input_img = Image.open(path)

    # Converting image to array format
    image_arr = np.array(input_img)

    reader = easyocr.Reader(['en'])
    text = reader.readtext(image_arr, detail= 0)

    return text, input_img

# text to dictionary format

def extracted_text(text):
    extrd_text_dict = {"NAME":[],
                       "DESIGNATION":[],
                       "COMPANY_NAME":[],
                       "CONTACT":[],
                       "EMAIL":[],
                       "WEBSITE":[],
                       "ADDRESS":[],
                       "PINCODE":[]}
    
    extrd_text_dict["NAME"].append(text[0])
    extrd_text_dict["DESIGNATION"].append(text[1])
    
    for i in range(2,len(text),1):
        if text[i].startswith("+") or (text[i].replace("-","").isdigit() and "-" in text[i]):
            extrd_text_dict["CONTACT"].append(text[i])
        
        elif "@" in text[i] and ".com" in text[i]:
            extrd_text_dict["EMAIL"].append(text[i])
        
        elif "WWW" in text[i] or "www" in text[i] or "Www" in text[i] or "wWw" in text[i] or "wwW" in text[i]:
            small = text[i].lower()
            extrd_text_dict["WEBSITE"].append(small)

        elif "TamilNadu" in text[i] or "Tamil Nadu" in text[i] or text[i].isdigit():
            extrd_text_dict["PINCODE"].append(text[i])

        elif re.match(r'^[A-Za-z]', text[i]):
            extrd_text_dict["COMPANY_NAME"].append(text[i])
        
        else:
            remove_colon = re.sub(r'[,;]',"" ,text[i])
            extrd_text_dict["ADDRESS"].append(remove_colon)

    for key,value in extrd_text_dict.items():
         
        if len(value) > 0:
            concadenate = " ".join(value)
            extrd_text_dict[key]= [concadenate]
        else:
            value = "NA"
            extrd_text_dict[key]= [value]


    return extrd_text_dict


# Streamlit part

st.set_page_config(layout= "wide")
st.title("Extraction Bizcard Data with OCR")

with st.sidebar:
    select = option_menu("Menu",["Home","Upload and Modify","Delete"])

if select == "Home":
    pass

if select == "Upload and Modify":
    img = st.file_uploader("Upload the image",type= ["png","jpg","jpeg"]) 

    if img is not None:
        st.image(img,width= 300)

        text_img, input_img = image_to_text(img)

        text_dict = extracted_text(text_img)

        if text_dict:
            st.success("Text Data Is Extracted Successfully")

    df = pd.DataFrame(text_dict)
    
    # Converting image to bytes

    Image_bytes = io.BytesIO()
    input_img.save(Image_bytes, format= "PNG")

    image_data = Image_bytes.getvalue()

    # Creating Dictionary

    data = {"IMAGE":[image_data]}
    df_1 = pd.DataFrame(data)

    concat_df = pd.concat([df,df_1],axis= 1)
    
    st.dataframe(concat_df)

if select == "Delete":
    pass