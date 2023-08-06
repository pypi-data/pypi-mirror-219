from datetime import datetime
import tensorflow as tf
import numpy as np
import cv2

import comun_sqlsrv


class AILog:
    def __init__(self, endpoint_name: str, endpoint_data_received: str):
        self.date_time = datetime.now()
        self.endpoint_name = endpoint_name
        self.endpoint_data_received = endpoint_data_received
        self.result = "KO_199"
        self.prediction = None
        self.img_path = None
        self.img_name = None
        self.img_frame = None
        self.error = None
        self.bar_code = None

    def __str__(self):
        return f"""
                LOG:
                Date: {self.date_time},
                Endpoint name: {self.endpoint_name},
                Endpoint received data: {self.endpoint_data_received},
                Result: {self.result},
                Prediction: {self.prediction}         
                """

    def save_log(self, mssql_srv: str, database: str, user: str, passwd: str):
        # SAVE IMAGE:
        if self.img_frame is not None:
            if self.img_frame is None:
                self.img_name = f'{self.date_time.strftime("%Y_%m_%d_%H_%M_%S")}.jpg'
            if self.img_path is None:
                self.img_path = f'img_save/{self.img_name}'
            cv2.imwrite(self.img_path, self.img_frame)

        # SAVE LOG IN DB:
        mssql = comun_sqlsrv.Sql(mssql_srv, database, user, passwd)
        query = f"""
                INSERT INTO T_VA_API_LOG
                (FECHA_HORA, ENDPOINT, RESULTADO, DATO_RECIBIDO, PREDICCION_VA, NOMBRE_IMAGEN, ERROR, COD_BAR)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """
        query_values = (self.date_time,
                        self.endpoint_name,
                        self.result,
                        self.endpoint_data_received,
                        self.prediction,
                        self.img_name,
                        self.error)
        mssql.ejecutar(query, query_values)
        mssql.cerrar_conexion()


def get_image_from_ip_camera(camera_url):
    """
    Function that connect to an IP camera and return a frame
    :param camera_url: need to be the RTSP URL
    :return: given frame from OpenCV when you read a video capture
    """
    try:
        cap = cv2.VideoCapture(camera_url)  # IP Camera
        success, frame = cap.read()
        cap.release()
        if success:
            return frame
        else:
            raise Exception

    except Exception:
        raise Exception(f"No se ha podido conectar a la camara IP")


def run_model_with_frame(img_frame, class_names: dict, model_path: str, output=False, rescaled_size=(224, 224)) -> str:
    """
    Function that execute an IA model
    :param img_frame: given frame from OpenCV when you read a video capture
    :param class_names: the posibles results of the IA
    :param model_path: path from the saved model
    :param output: set to True if you want to see all predictions
    :param rescaled_size: the size of the images which the model has been trained (img_height, img_width)
    :return: the maximum value predicted by the model from class_names dictionary
    """
    try:
        # Limit the GPU memory usage only to what is needed, without this TensorFlow would use all the GPU memory.
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)

        # Disable scientific notation for clarity
        np.set_printoptions(suppress=True)

        # Load the model. Compile is not needed while prediction, only while training.
        model = tf.keras.models.load_model(model_path, compile=False)

        image_resized = cv2.resize(img_frame, rescaled_size)
        image = np.expand_dims(image_resized, axis=0)
        predictions = model.predict(image)
        index = np.argmax(predictions)
        class_name = class_names[index]

        if output:
            print("\nPREDICTION:", flush=True)
            print(f"Class name: {class_name}  Match Score: {predictions[0][index]}", flush=True)
            print(f"All predictions: {predictions}", flush=True)

        return class_name

    except Exception:
        raise Exception(f"No se ha podido ejecutar la red neuronal")
