import gradio as gr
from PIL import Image
import requests
import hopsworks
import joblib
import pandas as pd
import numpy as np

project = hopsworks.login()
fs = project.get_feature_store()


mr = project.get_model_registry()
model = mr.get_model("wine_model", version=1)
model_dir = model.download()
model = joblib.load(model_dir + "/wine_model.pkl")
print("Model downloaded")

def wine(type, fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol):
    print("Calling function")
#     df = pd.DataFrame([[sepal_length],[sepal_width],[petal_length],[petal_width]], 
    if type == "red" or type == "RED" or type == "Red":
        type = 1
    elif type == "white" or type=="WHITE" or type == "White":
        type = 0
        
    df = pd.DataFrame([[type, fixed acidity, volatile acidity, citric acid, residual sugar, chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, alcohol]], 
                      columns=['type', 'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates', 'alcohol'])
    print("Predicting")
    print(df)
    # 'res' is a list of predictions returned as the label.
    res = np.round(model.predict(df)) 
    # We add '[0]' to the result of the transformed 'res', because 'res' is a list, and we only want 
    # the first element.
#     print("Res: {0}").format(res)
    print(res)
    wine_url = "https://raw.githubusercontent.com/aym1king/serverless-intro/master/wine/wine_imgs/" + res[0] + ".png"
    img = Image.open(requests.get(wine_url, stream=True).raw)            
    return img
        
demo = gr.Interface(
    fn=wine,
    title="Wine Quality Predictive Analytics",
    description="Experiment with wine features to predict which quality it has.",
    allow_flagging="never",
    inputs=[
        gr.inputs.Number(default="white", label="type (white or red)"),
        gr.inputs.Number(default=7.3, label="fixed acidity"),
        gr.inputs.Number(default=0.4, label="volatile acidity"),
        gr.inputs.Number(default=0.3, label="citric acid"),
        gr.inputs.Number(default=5.8, label="residual sugar"),
        gr.inputs.Number(default=0.1, label="chlorides"),
        gr.inputs.Number(default=30, label="free sulfur dioxide"),
        gr.inputs.Number(default=120, label="total sulfur dioxide"),
        gr.inputs.Number(default=1.0, label="density"),
        gr.inputs.Number(default=3.2, label="pH"),
        gr.inputs.Number(default=0.5, label="sulphates"),
        gr.inputs.Number(default=9.8, label="alcohol"),
        ],
    outputs=gr.Image(type="pil"))

demo.launch(debug=True)

