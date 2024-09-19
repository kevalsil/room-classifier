# Room Classifier


## 개요

Room Classifier는 이미지를 분석하여 방의 유형을 식별하는 웹 애플리케이션입니다. YOLOv5 모델을 사용하여 이미지를 분석하고, 이를 가공한 뒤 클러스터링과 PCA, 유사도 측정법 등의 방법을 통해 방의 유형을 예측합니다.


## 기능

- 웹 형식으로 편리한 첨부
- 이미지 분석 및 결과 도출
- 분석 결과 다운로드


## 구조

### 기술 스택

- **백엔드**: Python, Flask
- **프론트엔드**: HTML, JavaScript
- **머신러닝**: PyTorch (YOLOv5), Scikit-learn
- **데이터 처리**: Pandas, NumPy
- **시각화**: Matplotlib

### 작동 구조

1. **이미지 업로드**: 사용자가 웹 인터페이스를 통해 방 이미지를 업로드합니다.

2. **객체 감지**: YOLOv5 모델을 사용하여 업로드된 이미지에서 객체를 감지합니다.

3. **벡터 생성**: 감지된 객체와 그 신뢰도 점수를 바탕으로 고정 길이의 벡터를 생성합니다.

4. **클러스터링 및 PCA**: 미리 준비된 방 데이터에 DBSCAN 클러스터링을 적용하고, PCA를 사용하여 3차원으로 차원을 축소합니다.

5. **유사도 계산**: 새로운 이미지 벡터와 기존 클러스터 간의 유사도를 계산합니다.

6. **결과 시각화**: 계산된 유사도와 3D PCA 플롯을 웹 인터페이스에 표시합니다.

7. **결과 다운로드**: 사용자는 분석 결과와 3D 플롯을 다운로드할 수 있습니다.

### 작동 구조 다이어그램

```mermaid
graph TD
    A[사용자] -->|이미지 업로드| B[웹 인터페이스]
    B -->|이미지 전송| C[Flask 서버]
    C -->|객체 감지| D[YOLOv5 모델]
    D -->|객체 정보| E[벡터 생성]
    E -->|새 벡터| F[유사도 계산]
    G[기존 방 데이터] -->|클러스터링| H[DBSCAN]
    H -->|클러스터| I[PCA]
    I -->|3D 데이터| F
    F -->|결과| J[결과 시각화]
    J -->|표시| B
    B -->|결과 및 플롯 다운로드| A
```


## 설치

1. **리포지토리 클론**

   ```bash
   git clone https://github.com/your-repo/room-classifier.git
   cd room-classifier
   ```

2. **Python 의존성 설치**

   ```bash
   pip install -r requirements.txt
   ```

3. **서버 실행**

   ```bash
   python app.py
   ```

서버가 `http://127.0.0.1:5000`에서 실행됩니다.


## 사용

직관적인 웹 형식에 사진을 첨부하기만 하면 끝입니다!


## 기타

<details open>
  <summary>Recognition Rate</summary>
  <table border="1" table-layout="fixed">
  	<th align="center">Livingroom</th>
  	<th align="center">Kitchen</th>
    <th align="center">Library</th>
  	<th align="center">Bedroom</th>
    <th align="center">Bathroom</th>
  	<th align="center">Average</th>
  	<tr align="center"><!-- 첫번째 줄 시작 -->
      <td>96.77%</td>
      <td>93.10%</td>
      <td>67.86%</td>
      <td>70.00%</td>
      <td>92.86%</td>
      <td>
        <span style="color:red">84.12%</span>
      </td>
  	</tr><!-- 첫번째 줄 끝 -->
  </table>
</details>

<details close>
  <summary>Heatmap</summary>
  분석에 사용된 자료를 볼 수 있습니다. heatmap 문서를 확인하세요.
</details>
