#크롤링팀원 문정빈입니다!
# 어느정도 돌아가는 코드를 만들어서... 완성은 전혀 아니구 다듬고 살필 게 많지만 일단 깃헙에 공유해요!ㅠㅠ 

from bs4 import BeautifulSoup       #cmd의 pip명령을 통해 따로 깔아주어야 해요
from selenium import webdriver      #이것두! webdriver은 따로 설치해야 합니다
import time
import requests

url = "https://eureka.ewha.ac.kr/eureka/my/public.do?pgId=P531005519"   #강의계획안 사이트입니다.

# 크롬 브라우저로 웹 실행
path = "D:\python\chromedriver_win32 (1)\chromedriver.exe"
"""
여기서 오류가 나서 많이 헤맸는데ㅠ chrome driver 버전을 자기 컴퓨터 chrome 버전과 맞게 설정해야 잘 돌아가는 것 같아요
참고한 사이트는 https://blog.naver.com/kiddwannabe/221539689821의 게시글이고,
저같은 경우에는 chrome 버전이 95라서 https://sites.google.com/chromium.org/driver/여기서 받았습니다! 95와 96은 여기 있어요
"""

#미리 조건 설정 (일단 대충했어요 테스트용!! 입력이나 체크 안할거면 그냥 엔터치심 되어요)
print("맞으면 1")
qEng = input("영어강의인가요? : ")
qRem = input("원격강의인가요? : ")
print("\n 단답형")
classNum = input("학수번호? : ")
classN = input("강의명? : ")

# 드라이버 실행
driver = webdriver.Chrome(path)
driver.get(url)
time.sleep(2)


# 조회를 위한 조건문을 채워야 함
"""
강의계획안 사이트의 조건문...

html의 input 형식 참고 : https://coding-factory.tistory.com/24

1. select option
- 년도/학기 => 필수!  - 교과목 구분    - 교양영역
- 대학          - 개설학과/전공    - 학년
- 원어강의      -역량     -수업     -교시
2. text
- 학수번호  => 중요
- 교과목명  => 중요
- 담당교수      - 주제어 
3. check box
- 영어강의      -원격강의       -인문학관련소양        -sw교과목
    
"""

# 영어강의 체크박스 체크.
if qEng == "1":
    englishCheck = driver.find_element_by_id(
        "mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_ckbEngChk_chkimg")
    englishCheck.click()
else:
    print()

#원격강의 체크박스 체크.
if qRem == "1":
    remoteCheck = driver.find_element_by_id(
        "mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_ckbOnChk_chkimg")
    remoteCheck.click()
else :
    print()

#학수번호 text box
className = driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_ipbSubjectCd_input')
className.click()           #클릭을 하지 않고 send keys를 사용하면 오류가 납니다...  ㅠㅠ 한참 헤맸네요 click 필수!!
className.send_keys(classNum)
time.sleep(3)  #sleep을 쓰지 않으면 selenium이 개복치처럼 종료되기 때문에 시간을 줍니다
#그래서 좀 시간이 걸릴 수 있어요! 기다리면 결과가 나올거에요
#만약 갑자기 꺼지는 오류가 계속 난다면 sleep의 값을 좀 더 늘려주면 됩니다! 

#교과목명 text box
className = driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_ipbSubjectNm_input')
className.click()
className.send_keys(classN)
time.sleep(3)

# 검색버튼 누르기
btn = driver.find_element_by_xpath("//*[@id='mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_btnSearchTextBoxElement']/div")
btn.click()
time.sleep(3)

soup = BeautifulSoup(driver.page_source,"html.parser")
#print(soup.text)    #줄줄줄 출력됨
#print(soup.prettify())  #html이 이쁘게 출력됨
driver.find_element_by_id("mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_0_cell_0_16").click()    #이부분 아직 범용 구현x
time.sleep(10)

#헐 다운로드가 되네요!! ㅠㅠ 일단 영어강의 원격강의 체크했을 때 가장 먼저 보이는 글로벌어쩌구 강의계획서를 저장할 수 있는 상태에요!
#곧장 저희 컴퓨터의 download 파일에 저장되는데... 이걸 어떻게 어디에 저장히게 해줘야 자연어처리 코드 소스로 사용할 수 있을까요?.?

"""
남은 과제 :
1. 파일 다운로드 경로 및 방법
2. 조건을 완벽히 설정할 수 있도록 구현하기 : select option은 text, check box와 달리 오류가 떠서 고치고 있어요ㅠㅠ!
3. 강의계획안에 국문/영문/FILE/URL이 있는데, 전부 클릭하게 구현하기
4. 일괄적으로 다운로드 할 수 있게 구현하기
11. 위의 문제를 모두 해결하고 나면 실시간 변경사항 반영해서 긁어오기, 기타 다른 기능 구현 등등...
"""
