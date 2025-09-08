from flask import Flask, jsonify, render_template
import multiprocessing
from detect import run, parse_opt
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
current_person_count = multiprocessing.Value('i', 0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/person_count')
def get_person_count():
    return jsonify({'person_count': current_person_count.value})

# Modify this function to accept one argument
def start_detection(shared_value):
    opt = parse_opt()
    run(
        weights='yolov5x.pt',
        source=0,
        classes=[0],
        conf_thres=0.3,
        save_txt=False,
        save_csv=False,
        nosave=True,
        view_img=True,
        # Pass the received argument to the run function
        shared_person_count=shared_value,
    )
    

if __name__ == '__main__':
    # Pass the argument to the target function using args
    detection_process = multiprocessing.Process(
        target=start_detection, 
        args=(current_person_count,)
    )
    detection_process.daemon = True
    detection_process.start()
    app.run(host='0.0.0.0', port=5000, debug=False)