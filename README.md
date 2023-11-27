# ID2223 Serverless-Intro Lab 1

In this lab assignment, I built two scalable serverless machine learning system, consisting of a feature pipeline, a training pipeline, a batch inference pipeline, and a user interface (one for interactive querying, one as a dashboard) for iris flower and wine quality predictions. The tools used were Hopsworks, Github Actions, and Hugging Face Spaces. 

Hopsworks is a data platform for ML with a Python-centric Feature Store and MLOps capabilities. It is used to manage and sharing ML assets - features, models, training data, batch scoring data, logs, and more. Github Actions is a CI/CD tool that automates workflows. In this case we use it to automate generation of sample and inference. Finally, Hugging Face Spaces is our platform where we deploy our gradio application, which implements the interactive querying and dashboard.

The two serverless systems are extremely similar, and the only place they differ is at the feature pipeline and the training pipeline. For the former, in the wine dataset we have the added preprocessing steps where we impute missing data using mean and label encode categorical variables. And for the latter, we use KNearestNeighbor to train the iris flower prediction model and use a RandomForestRegressor to train the wine quality prediction model (with rounded outputs).  

## Public URL for the 2 Gradio Applications
- Iris
    - https://huggingface.co/spaces/aym1king/iris (Interactive Querying)
    - https://huggingface.co/spaces/aym1king/iris-monitor (Dashboard)
- Wine
    - https://huggingface.co/spaces/aym1king/wine (Interactive Querying)
    - https://huggingface.co/spaces/aym1king/wine-monitor (Dashboard)
