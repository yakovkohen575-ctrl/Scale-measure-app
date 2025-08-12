import streamlit as st
from PIL import Image
from pdf2image import convert_from_bytes
from streamlit_drawable_canvas import st_canvas
import math

st.set_page_config(page_title="מדידת קווים לפי קנה מידה", layout="wide")
st.title("📐 אפליקציה למדידת קווים לפי קנה מידה")

uploaded_file = st.file_uploader("העלה תמונה או PDF", type=["jpg", "png", "pdf"])
if uploaded_file:
    if uploaded_file.type == "application/pdf":
        pages = convert_from_bytes(uploaded_file.read())
        image = pages[0]
    else:
        image = Image.open(uploaded_file)

    st.image(image, caption="בחר קו קנה מידה", use_column_width=True)

    st.subheader("שלב 1: צייר קו קנה מידה")
    canvas_scale = st_canvas(
        background_image=image,
        height=image.height,
        width=image.width,
        drawing_mode="line",
        stroke_color="#FF0000",
        stroke_width=3,
        key="scale_canvas"
    )

    real_length = st.number_input("הזן את האורך האמיתי של הקו (במטרים)", min_value=0.0, step=0.1)
    scale = None
    if canvas_scale.json_data and real_length:
        objects = canvas_scale.json_data["objects"]
        if objects:
            line = objects[0]
            x1, y1 = line["left"], line["top"]
            x2, y2 = x1 + line["width"], y1 + line["height"]
            pixel_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            scale = real_length / pixel_length
            st.success(f"קנה המידה: {scale:.3f} מטר לפיקסל")

    st.subheader("שלב 2: צייר קווים שברצונך למדוד")
    canvas_measure = st_canvas(
        background_image=image,
        height=image.height,
        width=image.width,
        drawing_mode="line",
        stroke_color="#0000FF",
        stroke_width=3,
        key="measure_canvas"
    )

    if canvas_measure.json_data and scale:
        st.subheader("📏 תוצאות המדידה")
        for i, obj in enumerate(canvas_measure.json_data["objects"]):
            x1, y1 = obj["left"], obj["top"]
            x2, y2 = x1 + obj["width"], y1 + obj["height"]
            pixel_len = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            real_len = pixel_len * scale
            st.write(f"🔹 קו {i+1}: {real_len:.2f} מטר")
