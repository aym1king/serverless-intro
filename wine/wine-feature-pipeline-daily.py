import os
import modal

LOCAL=True

if LOCAL == False:
   stub = modal.Stub("wine_daily")
   image = modal.Image.debian_slim().pip_install(["hopsworks"]) 

   @stub.function(image=image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("id2223"))
   def f():
       g()


def generate_wine(name, fixed_acidity_max, fixed_acidity_min, volatile_acidity_max, volatile_acidity_min,
                    citric_acid_max, citric_acid_min, residual_sugar_max, residual_sugar_min,
                    chlorides_max, chlorides_min, free_sulfur_dioxide_max, free_sulfur_dioxide_min,
                    total_sulfur_dioxide_max, total_sulfur_dioxide_min, density_max, density_min,
                    pH_max, pH_min, sulphates_max, sulphates_min, alcohol_max, alcohol_min):
    """
    Returns a single wine as a single row in a DataFrame
    """
    import pandas as pd
    import random

    df = pd.DataFrame({
        "type": [round(random.uniform(0, 1))],
        "fixed_acidity": [random.uniform(fixed_acidity_max, fixed_acidity_min)],
        "volatile_acidity": [random.uniform(volatile_acidity_max, volatile_acidity_min)],
        "citric_acid": [random.uniform(citric_acid_max, citric_acid_min)],
        "residual_sugar": [random.uniform(residual_sugar_max, residual_sugar_min)],
        "chlorides": [random.uniform(chlorides_max, chlorides_min)],
        "free_sulfur_dioxide": [random.uniform(free_sulfur_dioxide_max, free_sulfur_dioxide_min)],
        "total_sulfur_dioxide": [random.uniform(total_sulfur_dioxide_max, total_sulfur_dioxide_min)],
        "density": [random.uniform(density_max, density_min)],
        "pH": [random.uniform(pH_max, pH_min)],
        "sulphates": [random.uniform(sulphates_max, sulphates_min)],
        "alcohol": [random.uniform(alcohol_max, alcohol_min)]
    })
    df['quality'] = name
    return df

def get_random_wine():
    """
    Returns a DataFrame containing one random wine
    """
    import pandas as pd
    import random

    quality3_df = generate_wine("3", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality4_df = generate_wine("4", 12.5, 4.6, 1.13, 0.11, 1.0, 0.0, 17.55, 0.7, 0.61, 0.013, 138.5, 3.0, 272.0, 7.0, 1.0, 0.99, 3.90, 2.74, 2.0, 0.25, 13.5, 8.4)
    quality5_df =  generate_wine("5", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality6_df = generate_wine("6", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality7_df = generate_wine("7", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality8_df =  generate_wine("8", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality9_df = generate_wine("9", 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)

    wines = [quality3, quality4, quality5, quality6, quality7, quality8, quaility9]
    # randomly pick one of these 7 and write it to the featurestore
    pick_random = round(random.uniform(0,7))
    wine_df = wines[pick_random]
    print(f'Wine with Quality wine_df["quality"] added')
    
   return wine_df


def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()

    wine_df = get_random_iris_flower()

    wine_fg = fs.get_feature_group(name="wine",version=1)
    wine_fg.insert(wine_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_daily")
        with stub.run():
            f()
