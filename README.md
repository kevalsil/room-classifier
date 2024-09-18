# Room Classifier

Room Classifier는 이미지를 분석하여 방의 유형을 식별하는 웹 애플리케이션입니다. YOLOv5 모델을 사용하여 이미지를 분석하고, 이를 가공한 뒤 클러스터링과 PCA, 유사도 측정법 등의 방법을 통해 방의 유형을 예측합니다.

## 기능

- 웹 형식으로 편리한 첨부
- 이미지 분석 및 결과 도출
- 분석 결과 다운로드

## 구조

- **Backend**: Flask (Python), PyTorch (YOLOv5)
- **Data Analysis**: Scikit-learn (DBSCAN, PCA), Pandas, NumPy
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Matplotlib

이미지 분석 -> 가공 -> 기존 클러스터링 자료와 비교 -> 유사도 측정 -> 예측 결과 도출

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
