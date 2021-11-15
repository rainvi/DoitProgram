    #추출할 필드
#표: 교과목 명
#표: 학수번호
#표: 학점/시간
#표: 개설 전공
#표: 수업시간/강의실 : 자연어처리 필요? 하여간 정제 필요
#표: 담당 교수 성명 / 소속 / 이메일 / 연락처 : 정제 필요
#표: 면담 장소 / 시간 : 정제 필요

#선수학습사항
#강의 방식 : 표 + 자연어처리
#학습 평가 방식 : 표 + 자연어처리
#교재

#표: 차시별 강의 계획 : 날짜 column만 date 형식으로 바꾸고 나머지는 그대로 내용 때려박으면 안되나? 그래서 해당 날짜에 그 알람 울리게 하고...

#OCR (테서렉트)를 이용해 이미지의 텍스트를 긁어오는 코드
import pytesseract
from PIL import Image

def img_extract_kor(file): #파라미터는 이미지파일 절대경로
    pytesseract.pytesseract.tesseract_cmd = r"테서렉트 위치 절대경로"
    text = pytesseract.image_to_string(Image.open(file), lang="kor")
    return text