import tensorflow as tf

model = tf.keras.applications.InceptionV3(include_top=True, weights='imagenet')
# InceptionV3 model trained on ImageNet dataset
from tensorflow.keras.preprocessing.image import load_img, img_to_array

img = load_img('static/uploads/Emma Watson_parth_49.jpg', target_size=(299, 299))
img_array = img_to_array(img)
img_array = tf.keras.applications.inception_v3.preprocess_input(img_array)

predictions = model.predict(img_array.reshape(1, 299, 299, 3))

from tensorflow.keras.applications.inception_v3 import decode_predictions

decoded_predictions = decode_predictions(predictions, top=10)[0]
tags = [tag[1] for tag in decoded_predictions]
print(tags)
