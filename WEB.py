import streamlit as st
import requests
import streamlit_lottie
import webbrowser
from helmet_detection import predict
import os


def main():
    st.set_page_config(layout='wide', page_title="Sign_detector")
    custom = '''
    <style>
    body {
        background-color: #FFFFFF;
    }
    </style>
    '''

    # st.markdown(custom,unsafe_allow_html=True)
    def lottie_loder(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    l2 = lottie_loder('https://lottie.host/21920c70-d7d9-4dd4-b5a4-04de562eb120/IRBDqhEhDi.json')
    git_logo = lottie_loder('https://lottie.host/69dbf8fc-3893-40ad-8cc2-07c40d298f56/AzzxAzqYBC.json')

    def open_website(website_url):
        webbrowser.open_new_tab(website_url)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(
            f'<div style="font-size: 30px; font-weight: bold; color: #415056;text-align: center;">Quick-Links</div>',
            unsafe_allow_html=True
        )
    with c2:
        st.button("Model", on_click=open_website, args=['https://github.com/ajaykumar703/WebApp-for-Helmet-detection'])

    with c3:

        st.button("SK-learn", on_click=open_website, args=['https://scikit-learn.org/stable/'])
    with c4:

        st.button("Tensorflow", on_click=open_website, args=["https://www.tensorflow.org"])
    with c5:

        st.button("Neural-Networks", on_click=open_website,
                  args=['https://www.geeksforgeeks.org/neural-networks-a-beginners-guide/'], key="custom-button")
    with c6:
        st.button("OpenCV", on_click=open_website, args=['https://opencv.org/'])

    st.write('---')

    title = 'Traffic Sign Detector'
    st.markdown(
        f'<div style="font-size: 80px; font-weight: bold; color: #1D5C96;text-align: center;">{title}</div>',
        unsafe_allow_html=True
    )

    st.write(' ')
    st.write(' ')

    left, right2 = st.columns(2)
    content = '''
               Our project is a Traffic Sign Detector designed to enhance road safety by automating
               the recognition and interpretation of traffic signs. This system uses deep learning techniques
               to detect and classify various types of traffic signs from images or video streams in real-time.
               It can be integrated into vehicles, traffic monitoring systems, or even used by pedestrians to
               increase awareness of road signage.
             '''

    with left:
        st.write('')
        st.write('')
        st.write('')
        st.markdown(
            f'<div style="font-size: 28px;padding-top:70px;color: #687F8D;font-family: Pacifico, cursive;">{content}</div>',
            unsafe_allow_html=True
        )

    with right2:
        streamlit_lottie.st_lottie(l2)

    st.markdown(
        f'<div style="font-size: 35px; font-weight: bold; color: #1D5C96;">Upload Your Image</div>',
        unsafe_allow_html=True
    )

    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    left_img, right_img = st.columns([3, 1])
    st.write("---")

    st.markdown(
        f'<div style="font-size: 60px; font-weight: bold; color: #1D5C96;text-align: center;">Git-Hub</div>',
        unsafe_allow_html=True
    )

    bottum_left, bottum_right = st.columns(2)
    with bottum_left:
        streamlit_lottie.st_lottie(git_logo, height=600, width=600)

    with bottum_right:
        st.markdown(
            f'<div style="font-size: 28px;padding-top:140px;padding-left:100px"> </div>',
            unsafe_allow_html=True
        )
        button_style = (
            "font-size: 24px;"
            "padding: 10px 20px;"
            "border: 2px solid #000;"
            "border-radius: 10px;"
            "text-decoration: none;"

        )

        # st.button("Sagar.E", on_click=open_website, args=['https://github.com/sagareddum'])
        st.write(f'<a href="https://github.com/ajaykumar703" style="{button_style}" class="stButton">Ajay.k</a>',
                 unsafe_allow_html=True)
        st.markdown(f'<div style="padding-top:50px;"> </div>', unsafe_allow_html=True)
        st.write(f'<a href="https://github.com/sagareddum" style="{button_style}" class="stButton">Sagar.E</a>',
                 unsafe_allow_html=True)
        st.markdown(f'<div style="padding-top:50px;"> </div>', unsafe_allow_html=True)
        st.write(f'<a href="https://github.com/sagareddum" style="{button_style}" class="stButton">Pramode.M.S</a>',
                 unsafe_allow_html=True)

    if uploaded_image is not None:
        image_data = uploaded_image.read()

        output_directory = 'Input_images'

        output_filename = "uploaded_image.jpg"

        output_path = output_directory + output_filename

        with open(output_path, "wb") as f:
            f.write(image_data)
        output_img, status = predict(output_path)

        with left_img:
            st.image(output_img, caption='Uploaded Image', use_column_width=True)

        with right_img:
            st.markdown(
                f'<div style="font-size: 50px;padding-top:70px;padding-left:50px;color: #687F8D;font-family: Pacifico, cursive;">{status}</div>',
                unsafe_allow_html=True
            )

        os.remove(output_path)


if __name__ == "__main__":
    main()




