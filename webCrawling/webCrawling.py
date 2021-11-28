
# 크롤링팀원 문정빈입니다!
# 일괄 파일 다운 구현했습니다. 파일이 업로드되지 않은 칸은 건너뛸 수 있도록 했어요.
# 강의 수가 많은 학기는 부가조건이 필수라, 여러가지를 따져본 결과 교과목 구분을 기준으로 조건을 나누기로 했어요. (다른 조건은 강의가 중복이 많거나 누락되는 강의가 발생했습니다!)
# 다운받을 때 파일명을 변경해서 저장하도록 했어요. 교수님들께서 파일명 정말 다양하게 올려주셔서 일괄 형식으로 저장하면 편할 것 같아서요!
# 미구현 및 오류 : 돋보기 아이콘으로 된 파일은 아직 저장하지 못해요.
# count가 1인 파일만 저장을 안하는데, 뭐가 문제인지 살펴볼 예정이에요.
# 한 페이지를 다 저장하고 다음 조건(교과목구분)으로 넘어갈 때, 강의 수 차이로 인해 스크롤이 사라지는 것 때문에 오류가 발생하고 있어요. 조만간 해결할 예정이에요.

from bs4 import BeautifulSoup  # cmd의 pip명령을 통해 따로 깔아주어야 해요
from selenium import webdriver  # 이것두! webdriver은 따로 설치해야 합니다
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import os
import shutil


url = "https://eureka.ewha.ac.kr/eureka/my/public.do?pgId=P531005519"  # 강의계획안 사이트입니다.
url2 = "http://localhost:8000/"

print("2021 - 겨울계절1차 : 1, 2021 - 2학기 : 2, ... , 2015 - 1학기 : 28 \n 반드시 숫자로만 입력해야 합니다! \n")
semesterNum = input("학기를 설정해주세요. (1~28) : ")
#시간상 테스트는 1만 돌렸습니다

# 크롬 브라우저로 웹 실행
path = "D:\python\chromedriver_win32 (1)\chromedriver.exe"
downloadPath = r'D:\학교\3학년 2학기\캡스톤디자인프로젝트\구현\다운로드 폴더'
# 경로는 ''안에 넣어주면 되어요


#파일 다운로드 경로 변경
op = Options()
op.add_experimental_option('prefs',{
    'download.default_directory': downloadPath
})
#최대화면 변경
op.add_argument('--start-fullscreen')
# 드라이버 실행
driver = webdriver.Chrome(path, chrome_options= op)
driver.get(url)
time.sleep(2)

# 조회를 위한 조건문을 채워야 함


#학기 선택하기
# 학기 선택은 상하키로 조종할 수 있습니다. 위에서부터 내려갈수록 반복 횟수를 늘려요
# 키입력 참고 주소 : https://coding-kindergarten.tistory.com/151

for i in range(1, int(semesterNum)):

    driver.find_element_by_xpath('//*[@id="mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_cbbYearTermCd_comboedit_input"]'
                             ).send_keys(Keys.ARROW_DOWN)

'''
select option(drop down)을 선택할 때 그냥 xpath가 아니라 full xpath를 복사해야 기능합니다.
통상적이지 않은 input based dropdown이라 많이 헤멨네요...ㅠ
element 찾는 법은 ctrl+F로 검색하면 빠릅니다.
'''
#교과목 구분 설정하기
# 귀찮게 설정하는 이유 : 교과목이 너무 많아서 사이트 자체에서 조건을 하나 이상 설정하게끔 막아놨습니다. 스크롤이 터지는 걸 방지하기 위한 것 같아요
# 교과목 구분에 따라 교양/비사대교직/전공선택(교직)/대학기초/전공기초/전공/학점교환 검색 후 합치기
# 계절학기는 그냥 조회해도 보이지만 구별하는 게 더 귀찮다

for i in range(1, 9):
    # 교과목 구분 combobox 클릭하기
    driver.find_element_by_xpath(
        '//*[@id="mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_cbbViewKindCd_comboedit_input"]'
                                 ).click()
    #아래키 클릭
    driver.find_element_by_xpath(
        '//*[@id="mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_cbbViewKindCd_comboedit_input"]'
        ).send_keys(Keys.ARROW_DOWN)
    # 엔터 치기
    driver.find_element_by_xpath(
        '//*[@id="mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_cbbViewKindCd_comboedit_input"]'
        ).send_keys(Keys.ENTER)

    # 검색버튼 누르기
    btn = driver.find_element_by_xpath(
        "//*[@id='mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_btnSearchTextBoxElement']/div")
    btn.click()
    time.sleep(3)

    #현재 html 가져오기
    soup = BeautifulSoup(driver.page_source, "html.parser")
    #print(soup.text)    #줄줄줄 출력됨
    #print(soup.prettify())  #html이 이쁘게 출력됨

    # 해당 id가 없을 경우 스루할 수 있는 코드가 필요
    if soup.find("div", id = 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_0_cell_0_0') == None:
        pass
    else:
         # 만약 조회 결과가 존재할 경우, 마지막까지 다운로드 버튼을 누름
         # 0 : 순번 | 1 : 학수번호 | 2 : 분반 | 3 : 교과목명
         # 4 : 교과목구분 | 5 : 교과영역 | 6 : 개설 학과 | 7 : 학년 | 8 : 교수명
         # 9 : 학점 | 10 : 시간 | 11 : 요일 | 12 : 교시 | 13 : 교실
         # 14 : 국문 | 15 : 영문 | 16 : FILE | 17 : URL
         # 18 : 영어강의 | 19 : 원어강의 | 20 : 원격강의 | 21 : 인문학관련교양과목 | 22 : SW과목
         # 23 : 정원 | 24 : 수업방식 | 25 : 비고
         '''
         파일명 : 교과목명_분반_교수_강의계획안번호
         '''

         #파일 처음부터 끝까지 받기
         Temp = 1
         count = 0
         Total = 0
         tempText = driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_stcTextTextBoxElement').text
         if "총건수" in tempText:
             tempList = tempText.split(':')
             tempText = tempList[1].replace(' ','')
             tempText = tempText.replace(']','')
             tempText = int(tempText)
             print("Total : " + str(tempText))

         while(Temp == 1):
             Total +=1
             if (Total >= tempText):
                 break
             if soup.find("div",id ='mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_'+str(count)+'_cell_'+str(count)+'_0') == None:
                 break
             else:
                 className = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_3').text
                 classNum = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_2').text
                 professor = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_8').text
                 #가끔 교수명에 \n가 들어가는 경우가 있어서... 치환
                 className = className.replace("/","+")
                 professor = professor.replace("/","+")
                 professor = professor.replace("\n","")
                 new_filename = className + "_" + classNum + "_" + professor + "_"

                 print("count: "+str(count))

                 # 하나의 강의에 모든 파일 받기?
                 # 오류 : 어째선지 count가 1일 때의 행은 다운이 안되어서... 이유를 찾고 있습니다!
                 for number in range(14, 18):

                     if soup.find('div', id = 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_'+str(count)+'_cell_'+str(count)+'_'+str(number)+'_controlexpandImageElement') == None:
                         pass

                     else:
                         # 파일 다운 버튼을 클릭
                         number = str(number)

                         driver.find_element_by_id(
                             'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                                 count) + '_cell_' + str(count) + '_' + number).click()

                         time.sleep(2)  # 없으면 오류남 (파일이 제대로 다운이 안되거나...)

                         # 파일명 변경은 selenium에서 할 수 없기에 따로 코드를 짜야 한다.

                         filename = max([downloadPath + '\\' + f for f in os.listdir(downloadPath)],
                                        key=os.path.getctime)
                         temp = 1

                         while (temp == 1):
                             if "crdownload" in filename:  # 아직 저장이 덜 되었을 때 생김
                                 temp = 1
                             else:
                                 temp = 0

                         print(filename)
                         list_filename = filename.split(".")
                         fileEx = list_filename[1]
                         print(new_filename + number + "." + fileEx)
                         shutil.move(os.path.join(downloadPath, filename),
                                     os.path.join(downloadPath, new_filename + number + "." + fileEx))
                         time.sleep(1)

                # 브라우저 스크롤 가장 밑으로
                 for i in range(0, 4):
                    driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_incbuttonAlignImageElement').click()


                 # 스크롤 1칸 내리기
                 # 스크롤이 없을 수도 있어서 if문 넣었는데... 작동을 안해서 이 부분 좀 더 다른 방법을 고민해보겠어요

                 if soup.find('div', id = 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_vscrollbar_incbuttonAlignImageElement') != None:
                     driver.find_element_by_id(
                         'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_vscrollbar_incbuttonAlignImageElement').click()


                 count = (count+1)%18

         # 다운로드가 끝났으면 다시 최상단으로 스크롤을 돌려야 함
         scrollStyle = driver.find_element_by_id(
            'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_trackbar').get_attribute('style')
         list_scrollStyle = scrollStyle.split()
         scrollStyleHeight = list_scrollStyle[16]

         while (scrollStyleHeight != '15px,'):
                 # 가장 상단에 있을 경우 값은 15px
            driver.find_element_by_id(
                'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_decbuttonAlignImageElement').click()
            scrollStyle = driver.find_element_by_id(
                'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_trackbar').get_attribute('style')
            list_scrollStyle = scrollStyle.split()
            scrollStyleHeight = list_scrollStyle[16]

         time.sleep(2)

print("완료")
time.sleep(100)



"""
남은 과제 :
1. 파일 다운로드 경로 및 방법 v

-> 파일 경로 변경은 성공했으나 어디까지나 컴퓨터 내에서만.
django 서버에 업로드할 수 있어야함.
1) 가상환경에 저장 후 업로드하는 방법 
2) download link를 얻는 방법을 알아내기
=> 1)의 경우 mysql에 저장하는 내용은 가상환경의 파일경로가 될 것이고, 2)의 경우 mysql에 저장하는 내용은 download link가 될 것입니다.

2. 강의계획안에 국문/영문/FILE/URL이 있는데, 전부 클릭하게 구현하기
3. Chrome 창으로 뜨는 파일(돋보기) 저장 구현하기 => 출력 눌러서 pdf 저장하는 기능 이용하면 될 것 같다.
4. 중복처리... 파일명 아니까 쉬울듯 pass로 처리하거나

* 구동시간에 대하여 *
이 코드는 오류를 방지하기 위해 sleep을 많이 사용하고 있기도 하지만,
사람이 클릭하듯이 돌아가기 때문에 구동 시간이 깁니다.
하지만 저희가 만드는 어플은 zoom 회의와 같이 실시간과 속도가 매우 중요한 서비스가 아니므로,
지금의 속도로도 충분할 것이라고 생각됩니다.
"""
