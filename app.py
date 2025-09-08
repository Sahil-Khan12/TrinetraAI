from flask import Flask, jsonify, render_template
import multiprocessing
from detect import run, parse_opt
from flask_cors import CORS
import time  # Added for timestamp in logs

app = Flask(__name__)
CORS(app)
current_person_count = multiprocessing.Value('i', 0)
current_area = multiprocessing.Value('d', 0.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/person_count')
def get_person_count():
    person_count = current_person_count.value
    area = current_area.value
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Serving person_count: {person_count}, area: {area}")  # Enhanced log
    return jsonify({
        'person_count': person_count,
        'area': area
    })

def start_detection(shared_person_count, shared_area):
    opt = parse_opt()
    run(
        weights='yolov5s.pt',
        source='http://192.168.80.221:4747/video',
        classes=[0],
        conf_thres=0.3,
        save_txt=False,
        save_csv=False,
        nosave=True,
        view_img=True,
        shared_person_count=shared_person_count,
        shared_area=shared_area,
    )

if __name__ == '__main__':
    detection_process = multiprocessing.Process(
        target=start_detection,
        args=(current_person_count, current_area)
    )
    detection_process.daemon = True
    detection_process.start()

    # Run Flask server in the main thread
    print("Starting Flask server at http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

    # Ensure process cleanup on exit
    import atexit
    @atexit.register
    def cleanup():
        if detection_process.is_alive():
            detection_process.terminate()
            print("Detection process terminated.")