# Signature Extractor

This Streamlit app provides a user-friendly interface for extracting and colorizing signatures from images.

## Features

* **Image Upload:** Upload images containing signatures in JPG, JPEG, or PNG format.
* **Signature Selection:** Draw a rectangle on the canvas to precisely select the signature region.
* **Color Customization:** Choose the desired color for your signature using a color picker.
* **Threshold Adjustment:** Fine-tune the extraction process by adjusting the threshold value.
* **Processed Signature Output:** View and download the extracted signature as an image file (PNG).
* **New Image Upload:** Easily upload a new image to extract a different signature.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/pranaysuyash/img-ext.git
   cd img-ext
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   **Note:** Make sure you have a `requirements.txt` file in the root of your project with the following:
   ```
   streamlit
   opencv-python
   numpy
   pillow
   streamlit_drawable_canvas
   ```

3. **Run the App:**
   ```bash
   streamlit run app.py
   ```

## Deployment

### Streamlit Sharing (Limited Functionality)
* Streamlit Cloud may have limitations with OpenCV's graphics dependencies. You might need to simplify image processing or use cloud image processing services.
* To deploy to Streamlit Sharing, follow the instructions [here](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app).

### Alternatives (Recommended)
* **Heroku:** Deploy to Heroku for more control over the environment. Visit [Heroku](https://www.heroku.com/) for more information.
* **Vultr:** Deploy to a Vultr server for full customization. Visit [Vultr](https://www.vultr.com/) for more information.

### Deployment Guidance
* **Vultr:** Follow the detailed instructions for setting up a Vultr server, installing dependencies, and configuring Nginx.
* **Heroku:** Refer to the [Heroku documentation](https://devcenter.heroku.com/articles/streamlit) for Streamlit deployment.

## Contributing
Contributions are welcome! If you have any improvements or new features you'd like to add, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
