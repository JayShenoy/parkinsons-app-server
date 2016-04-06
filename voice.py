from flask import Flask, make_response
app = Flask(__name__)

from subprocess import CalledProcessError, check_call
from tempfile import NamedTemporaryFile
import numpy as np
from StringIO import StringIO
import pickle

class ANN:
    def __init__(self, theta1, theta2):
        self.theta1 = theta1
        self.theta2 = theta2

    # Function that receives feature vector X as input and returns diagnosis
    def predict(self, x):
        a1 = x
        z2 = theta1.dot(a1)
        a2 = g(z2)
        a2 = np.concatenate((np.ones((1, num_fold)), a2))
        z3 = theta2.dot(a2)
        a3 = g(z3)
        diagnosis = a3.T.round()
        return diagnosis

# Load theta matrices and construct ANN
theta1_file = open('theta1.txt')
theta2_file = open('theta2.txt')
theta1 = pickle.load(theta1_file)
theta2 = pickle.load(theta2_file)
theta1_file.close()
theta2_file.close()

neural_network = ANN(theta1, theta2)

@app.route('/upload-voice', methods=['GET', 'POST'])
def upload_voice():
    # voice_file = request.files['voice.wav']

    audio_file_name = 'recording.wav'

    # Create temporary output file
    output_file = NamedTemporaryFile(mode='w+b', suffix='.txt')

    if audio_file_name:
        # Extract dysphonia measures
        try:
            check_call('matlab -nodisplay -nojvm -nosplash -r "extract(\'%s\', \'%s\')"' % (audio_file_name, output_file.name), shell=True)

            # Retrieve feature values from output file
            output_file.seek(0)
            extracted_features = output_file.read()
            output_file.close()
            # Create feature vector
            features = np.genfromtxt(StringIO(extracted_features))
            features = features.reshape((features.size, 1))
            # Append bias unit to feature vector
            features = np.vstack((np.ones((1, 1)), features))

            '''
            diagnosis = neural_network.predict(features)

            response = make_response(json.dumps(diagnosis), 200)
            response.headers['Content-Type'] = 'application/json'
            return response
            '''

            return extracted_features

        except CalledProcessError as cpe:
            output_file.close();
            return cpe.output

if __name__ == '__main__':
    app.run()