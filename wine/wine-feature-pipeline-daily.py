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

    quality3_df = generate_wine(3, 11.8, 4.2, 1.58, 0.17, 0.66, 0.0, 16.2, 0.7, 0.267, 0.022, 289.0, 3.0, 440.0, 9.0, 1.0, 0.99, 3.63, 2.87, 0.86, 0.28, 12.6, 8.0)
    quality4_df = generate_wine(4, 12.5, 4.6, 1.1, 0.1, 1.0, 0.0, 17.6, 0.7, 0.6, 0.0, 138.5, 3.0, 272.0, 7.0, 1.0, 1.0, 3.9, 2.7, 2.0, 0.2, 13.5, 8.4)
    quality5_df =  generate_wine(5, 15.9, 4.5, 1.3, 0.1, 1.0, 0.0, 23.5, 0.6, 0.6, 0.0, 131.0, 2.0, 344.0, 6.0, 1.0, 1.0, 3.8, 2.8, 2.0, 0.3, 14.9, 8.0)
    quality6_df = generate_wine(6, 14.3, 3.8, 1.0, 0.1, 1.7, 0.0, 65.8, 0.7, 0.4, 0.0, 112.0, 1.0, 294.0, 6.0, 1.0, 1.0, 4.0, 2.7, 2.0, 0.2, 14.0, 8.4)
    quality7_df = generate_wine(7, 15.6, 4.2, 0.9, 0.1, 0.8, 0.0, 19.2, 0.9, 0.4, 0.0, 108.0, 3.0, 289.0, 7.0, 1.0, 1.0, 3.8, 2.8, 1.4, 0.2, 14.2, 8.6)
    quality8_df =  generate_wine(8, 12.6, 3.9, 0.8, 0.1, 0.7, 0.0, 14.8, 0.8, 0.1, 0.0, 105.0, 3.0, 212.5, 12.0, 1.0, 1.0, 3.7, 2.9, 1.1, 0.2, 14.0, 8.5)
    quality9_df = generate_wine(9, 9.1, 6.6, 0.4, 0.2, 0.5, 0.3, 10.6, 1.6, 0.0, 0.0, 57.0, 24.0, 139.0, 85.0, 1.0, 1.0, 3.4, 3.2, 0.6, 0.4, 12.9, 10.4)

    wines = [quality3_df, quality4_df, quality5_df, quality6_df, quality7_df, quality8_df, quality9_df]
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

    wine_df = get_random_wine()

    wine_fg = fs.get_feature_group(name="wine",version=1)
    wine_fg.insert(wine_df)

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_daily")
        with stub.run():
            f()
