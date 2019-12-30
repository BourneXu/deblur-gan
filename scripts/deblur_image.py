import numpy as np
from PIL import Image
import click
import os
import io


from deblurgan.model import generator_model
from deblurgan.utils import load_image, deprocess_image, preprocess_image
from keras import backend as K
import tensorflow as tf


def deblur(weight_path, input_dir, output_dir):
    g = generator_model()
    g.load_weights(weight_path)
    for image_name in os.listdir(input_dir):
        image = np.array([preprocess_image(load_image(os.path.join(input_dir, image_name)))])
        x_test = image
        generated_images = g.predict(x=x_test)
        generated = np.array([deprocess_image(img) for img in generated_images])
        x_test = deprocess_image(x_test)
        for i in range(generated_images.shape[0]):
            x = x_test[i, :, :, :]
            img = generated[i, :, :, :]
            output = np.concatenate((x, img), axis=1)
            im = Image.fromarray(output.astype(np.uint8))
            im.save(os.path.join(output_dir, image_name))


class Deblur:
    def __init__(self, weight_path):
        self.weight_path = weight_path
        self.load_model()

    def load_model(self):
        self.g = generator_model()
        self.g.load_weights(self.weight_path)
        self.g._make_predict_function()
        self.graph = tf.get_default_graph()

    def deblurOne(self, imageByte: bytes):
        image = np.array([preprocess_image(Image.open(io.BytesIO(imageByte)))])
        try:
            image = np.delete(image, 3, 3)
        except:
            pass
        x_test = image
        with self.graph.as_default():
            generated_images = self.g.predict(x=x_test)
        generated = np.array([deprocess_image(img) for img in generated_images])
        x_test = deprocess_image(x_test)
        for i in range(generated_images.shape[0]):
            img = generated[i, :, :, :]
            im = Image.fromarray(img.astype(np.uint8))
            output = io.BytesIO()
            im.save(output, format="png")
            output.seek(0)
            return output


@click.command()
@click.option("--weight_path", help="Model weight")
@click.option("--input_dir", help="Image to deblur")
@click.option("--output_dir", help="Deblurred image")
def deblur_command(weight_path, input_dir, output_dir):
    return deblur(weight_path, input_dir, output_dir)


if __name__ == "__main__":
    # deblur_command()
    test = Deblur("../generator.h5")
    test_out = test.deblurOne(open("../sample/test.png", "rb").read())
