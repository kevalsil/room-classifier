from flask import Flask, request, jsonify, render_template
import os
import torch
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import pairwise_distances
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import io
import base64
import pickle

app = Flask(__name__)

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

def detect_and_process_image(image_path, num_classes=80):
    results = model(image_path)
    
    # 벡터 초기화
    vector = [0 for _ in range(num_classes)]
    
    # 탐지 결과 처리
    for det in results.xyxy[0]:  # 첫 번째 (그리고 유일한) 이미지의 탐지 결과
        class_index = int(det[5])  # 클래스 인덱스
        confidence = float(det[4]) * 10  # 정확도 * 10
        vector[class_index] += confidence
    
    return vector

def save_cluster_data(cluster_data, filename="cluster_data.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(cluster_data, file)

def load_cluster_data(filename="cluster_data.pkl"):
    with open(filename, "rb") as file:
        return pickle.load(file)

def perform_clustering(csv_files, eps, min_samples):
    cluster_data = []
    all_data = []

    for file in csv_files:
        data = pd.read_csv(file)
        vectors = data.values
        all_data.append(vectors)
        scaler = StandardScaler()
        vectors_scaled = scaler.fit_transform(vectors)

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        dbscan.fit(vectors_scaled)

        core_samples = vectors_scaled[dbscan.core_sample_indices_] if len(dbscan.core_sample_indices_) > 0 else []
        cluster_data.append((core_samples, scaler, dbscan))

    all_data_combined = np.vstack(all_data)
    pca = PCA(n_components=3)
    pca.fit(all_data_combined)

    save_cluster_data((cluster_data, pca), "cluster_data.pkl")

def process_new_vector(new_vector):
    csv_files = ["csvdata/Living_room_data.csv", "csvdata/Kitchen_data.csv", "csvdata/Library_data.csv", "csvdata/Bedroom_data.csv", "csvdata/Bathroom_data.csv"]

    if not os.path.exists("cluster_data.pkl"):
        perform_clustering(csv_files, eps=0.5, min_samples=5)

    cluster_data, pca = load_cluster_data("cluster_data.pkl")

    new_vector_pca = pca.transform([new_vector])[0]

    all_data_pca = []
    for core_samples, scaler, _ in cluster_data:
        if len(core_samples) > 0:
            all_data_pca.append(pca.transform(scaler.inverse_transform(core_samples)))
        else:
            all_data_pca.append([])

    min_distance = np.inf
    closest_csv = None
    distance_table = []

    for i, (core_samples, scaler, model) in enumerate(cluster_data):
        if len(core_samples) == 0:
            distance_table.append((csv_files[i], None))
            continue

        new_vector_scaled = scaler.transform([new_vector])
        distances = pairwise_distances(new_vector_scaled, core_samples, metric="manhattan")
        distance = np.min(distances)

        distance_table.append((csv_files[i], distance))

        if distance < min_distance:
            min_distance = distance
            closest_csv = csv_files[i]

    # 3D PCA 플롯 생성
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['b', 'g', 'r', 'c', 'm']
    for i, data_pca in enumerate(all_data_pca):
        if len(data_pca) > 0:
            ax.scatter(data_pca[:, 0], data_pca[:, 1], data_pca[:, 2], c=colors[i], label=csv_files[i].split('/')[-1].split('_')[0])

    ax.scatter(new_vector_pca[0], new_vector_pca[1], new_vector_pca[2], c='black', marker='x', s=100, label='New Vector')

    ax.set_title('3D PCA of Clusters')
    ax.legend()

    # 플롯을 이미지로 변환
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.getvalue()).decode()
    plt.close()

    room_type = closest_csv.split('/')[-1].split('_')[0]

    return {
        'closest_room': room_type,
        'distance_table': distance_table,
        'plot': img_data
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file:
        # 임시로 파일 저장
        temp_path = 'temp_image.jpg'
        file.save(temp_path)
        
        # 이미지 분석
        vector = detect_and_process_image(temp_path)
        
        # 결과 처리
        result = process_new_vector(vector)
        
        # 임시 파일 삭제
        os.remove(temp_path)
        
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)