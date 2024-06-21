import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import os
import uuid
from pathlib import Path

# --- Page Configuration ---
st.set_page_config(layout="wide",
                   page_title="Signature Extractor",
                   page_icon=":pencil:")

# Adding Microsoft Clarity Tracker Code
clarity_id = os.environ.get('CLARITY_ID')
if clarity_id:
    tracker_code = f"""
    <script type="text/javascript">
        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", "{clarity_id}");
    </script>
    """
    components.html(tracker_code)

# Adding Google Analytics Code
ga_id = os.environ.get('GA_ID')
if ga_id:
    google_analytics_code = f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """
    components.html(google_analytics_code)

st.title("Signature Extractor")
st.markdown("Easily extract and color your signatures from images!")

# --- Initialize Session State ---
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = None
if 'color' not in st.session_state:
    st.session_state.color = "#0000ff"  # Default signature color
if 'final_image' not in st.session_state:
    st.session_state.final_image = None
if 'payment_confirmed' not in st.session_state:
    st.session_state.payment_confirmed = False
if 'threshold' not in st.session_state:
    st.session_state.threshold = 150  # Default threshold value
if 'adjustment_count' not in st.session_state:
    st.session_state.adjustment_count = 0
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'selection_confirmed' not in st.session_state:
    st.session_state.selection_confirmed = False

# --- Temporary Files Directory ---
temp_dir = Path(f"temp_{st.session_state.session_id}")
temp_dir.mkdir(parents=True, exist_ok=True)
output_path = temp_dir / "output.png"

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an image containing a signature...",
                                 type=["jpg", "jpeg", "png"])

# --- Check if file is valid ---
if uploaded_file is not None:
    try:
        st.session_state.uploaded_image = Image.open(uploaded_file)
        if st.session_state.uploaded_image.mode == 'RGBA':
            # Convert transparent areas to white
            background = Image.new("RGB", st.session_state.uploaded_image.size,
                                   (255, 255, 255))
            background.paste(st.session_state.uploaded_image,
                             mask=st.session_state.uploaded_image.split()
                             [3])  # 3 is the alpha channel
            st.session_state.uploaded_image = background
        st.session_state.adjustment_count = 0
        # Clear previous temporary files
        if temp_dir.exists():
            for f in temp_dir.iterdir():
                f.unlink()
    except Exception as e:
        st.error(f"Error: {e}")
        st.session_state.uploaded_image = None

# --- Layout ---
col1, col2 = st.columns([1, 2])  # Adjust if needed

# --- Image Preview (Always in col1) ---
with col1:
    if st.session_state.uploaded_image is not None:
        preview_width = 300
        preview_height = int(preview_width *
                             (st.session_state.uploaded_image.height /
                              st.session_state.uploaded_image.width))
        st.image(st.session_state.uploaded_image,
                 caption='Uploaded Image Preview',
                 width=preview_width,
                 use_column_width=False)

# --- Selection Canvas (Initially in col2, moves to col1 after confirmation) ---
if st.session_state.uploaded_image is not None:
    image = np.array(st.session_state.uploaded_image)

    # --- Calculate Resized Image ONCE ---
    if not st.session_state.selection_confirmed:
        canvas_width = 600  # Fixed canvas width
    else:
        canvas_width = preview_width

    canvas_height = int(canvas_width * (image.shape[0] / image.shape[1]))
    scale_factor = canvas_width / image.shape[1]
    resized_image = cv2.resize(image, (canvas_width, canvas_height))

    if not st.session_state.selection_confirmed:
        with col2:
            st.write("1. Select the signature region:")

            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#ff0000",
                background_image=Image.fromarray(
                    resized_image),  # Use resized_image
                update_streamlit=True,
                height=canvas_height,
                width=canvas_width,
                drawing_mode="rect",
                key="canvas",
            )

            if canvas_result.json_data is not None:
                objects = canvas_result.json_data["objects"]
                if objects:
                    left = int(objects[0]["left"] / scale_factor)
                    top = int(objects[0]["top"] / scale_factor)
                    width = int(objects[0]["width"] / scale_factor)
                    height = int(objects[0]["height"] / scale_factor)

                    st.session_state.selected_region = (left, top, width,
                                                        height)

            st.write("2. Choose Signature Color:")
            st.session_state.color = st.color_picker(
                "Pick a color for the signature", st.session_state.color)

            st.write("3. Adjust Threshold (Optional):")
            st.session_state.threshold = st.slider(
                "Fine-tune the extraction by adjusting the threshold value.",
                0, 255, st.session_state.threshold)

            if st.button('Confirm Selection'):
                if st.session_state.selected_region is None:
                    st.warning("Please select a region first.")
                else:
                    st.session_state.selection_confirmed = True
                    st.rerun()

    else:  # Selection Confirmed
        with col1:
            st.write("Selected Region:")

            # --- Get Selection Coordinates ---
            if st.session_state.selected_region is not None:
                left, top, width, height = st.session_state.selected_region
                left = int(left * scale_factor)
                top = int(top * scale_factor)
                width = int(width * scale_factor)
                height = int(height * scale_factor)
            else:
                left, top, width, height = 0, 0, 0, 0

            # --- Display Canvas with Selection in col1 ---
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#ff0000",
                background_image=Image.fromarray(
                    resized_image),  # Use resized_image
                update_streamlit=True,
                height=canvas_height,
                width=canvas_width,
                drawing_mode="rect",
                key="canvas_confirmed",
                initial_drawing={
                    "objects": [{
                        "type": "rect",
                        "left": left,
                        "top": top,
                        "width": width,
                        "height": height,
                        "fill": "rgba(255, 165, 0, 0.3)",
                        "stroke": "#ff0000"
                    }]
                })

        with col2:
            st.write("2. Choose Signature Color:")
            st.session_state.color = st.color_picker(
                "Pick a color for the signature", st.session_state.color)

            st.write("3. Adjust Threshold (Optional):")
            st.session_state.threshold = st.slider(
                "Fine-tune the extraction by adjusting the threshold value.",
                0, 255, st.session_state.threshold)

            if st.session_state.adjustment_count < 5:
                if st.button('Process Image'):
                    x, y, w, h = st.session_state.selected_region
                    sig = image[y:y + h, x:x + w]

                    sig_gray = cv2.cvtColor(sig, cv2.COLOR_BGR2GRAY)
                    ret, alpha_mask = cv2.threshold(sig_gray,
                                                    st.session_state.threshold,
                                                    255, cv2.THRESH_BINARY_INV)
                    color_bgr = tuple(
                        int(st.session_state.color[i:i + 2], 16)
                        for i in (1, 3, 5))
                    color_mask = np.zeros_like(sig, dtype=np.uint8)
                    for i in range(3):
                        color_mask[:, :, i] = color_bgr[i]

                    sig_color = cv2.addWeighted(sig, 1, color_mask, 0.5, 0)
                    b, g, r = cv2.split(sig_color[..., :3])
                    new = [b, g, r, alpha_mask]

                    png = cv2.merge(new)
                    final_image = Image.fromarray(png)
                    st.session_state.final_image = final_image
                    if not output_path.parent.exists():
                        output_path.parent.mkdir(parents=True)
                    final_image.save(output_path)
                    st.session_state.adjustment_count += 1
            else:
                st.warning(
                    "You have reached the maximum number of adjustments. Please make a new payment to continue."
                )

            if st.session_state.final_image is not None:
                # Display final image with a maximum width to prevent overflow
                final_image_width = min(st.session_state.final_image.width,
                                        600)
                final_image_height = int(final_image_width *
                                         (st.session_state.final_image.height /
                                          st.session_state.final_image.width))
                st.image(st.session_state.final_image,
                         caption='Final Processed Signature',
                         width=final_image_width,
                         use_column_width=False)
                if output_path.exists():
                    with open(output_path, "rb") as file:
                        st.download_button(label="Download Signature",
                                           data=file,
                                           file_name="extracted_signature.png",
                                           mime="image/png")


# --- Function to Reset Session and Delete Temp Files ---
def reset_session():
    # Reset session state
    st.session_state.uploaded_image = None
    st.session_state.payment_confirmed = False
    st.session_state.selection_confirmed = False
    st.session_state.selected_region = None
    st.session_state.adjustment_count = 0
    st.session_state.final_image = None
    st.session_state.session_id = str(uuid.uuid4())
    # Clear previous temporary files
    temp_dir = Path(f"temp_{st.session_state.session_id}")
    if temp_dir.exists():
        for f in temp_dir.iterdir():
            f.unlink()
        temp_dir.rmdir()  #Remove the directory itself after content deletion


# --- Upload New Image Button ---
if st.session_state.uploaded_image is not None and st.button(
        "Upload a New Image"):
    reset_session()
    st.rerun()

# --- Gumroad Payment Button ---
st.markdown("---")
st.markdown(
    "###### If you find this tool useful, consider supporting us by making a payment."
)

gumroad_button = f"""
<a href="https://pranaysuyash.gumroad.com/l/sig-ext?wanted=true" target="_blank" rel="noopener noreferrer">
    <button style="background-color: #FFB74D; color: white; border: none; padding: 12px 24px; font-size: 18px; font-weight: bold; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.25); background-image: linear-gradient(to bottom, #FFD54F, #FFC107); transition: all 0.3s ease;">
    Support on Gumroad
</button>
</a>
"""

st.markdown(gumroad_button, unsafe_allow_html=True)
