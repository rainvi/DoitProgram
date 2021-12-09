'''
이 코드는 강의계획안 사이트에서 파일을 자동으로 다운로드하는 코드입니다.
설치해야하는 것 :
beautifulsoup, selenium, pillow, selenium_screenshot
자신의 chrome 버전과 맞는 chrome driver
'''
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from PIL import Image #pip install pillow
from Screenshot import Screenshot_Clipping #pip install selenium_screenshot
import time
import os
import shutil


url = "https://eureka.ewha.ac.kr/eureka/my/public.do?pgId=P531005519"  # 강의계획안 사이트입니다.

'''
필요한 정보를 설정합니다.
path는 chrome driver의 설치 위치로 바꾸어주세요.
downloadPath는 파일을 저장받을 위치로 바꾸어주세요.
'''
print("2021 - 겨울계절1차 : 1, 2021 - 2학기 : 2, ... , 2015 - 1학기 : 28 \n 반드시 숫자로만 입력해야 합니다! \n")
semesterNum = input("학기를 설정해주세요. (1~28) : ")
path = "D:\python\chromedriver_win32 (1)\chromedriver.exe"  #chrome driver 저장 위치를 알려줍니다.
downloadPath = r'D:\학교\3학년 2학기\캡스톤디자인프로젝트\구현\다운로드 폴더'   #로컬 컴퓨터 저장위치를 설정합니다.


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


#학기를 자동으로 변경
# 학기 선택은 상하키로 조종됩니다. 위에서부터 아래에 있는 학기를 선택할수록 반복 횟수를 늘립니다.
for i in range(1, int(semesterNum)):
    driver.find_element_by_xpath('//*[@id="mainframe_VFrameSet_WorkFrame_Child__form_div_Work_div_search_cbbYearTermCd_comboedit_input"]'
                             ).send_keys(Keys.ARROW_DOWN)

'''
드롭다운에 대한 추가 설명
select option(drop down)을 선택할 때 그냥 xpath가 아니라 full xpath를 복사해야 합니다.
---> 스크롤이 생기는 dropdown의 경우 스크롤 코드를 추가해야하기 때문에 down key로 변경해서 구현하였습니다.
나중에 쓰일 일이 있을까봐 주석으로 남깁니다.
'''

#교과목 구분 설정하기
'''
교과목 구분을 설정하는 이유에 대한 설명
이유 : 강의 수가 많은 학기, 예를 들어 계절학기가 아닌 학기일 경우, 하나 이상의 조건을 설정하도록 사이트 자체에 조건이 걸려 있었습니다.
해결 방안 : 교과목 구분에 따라 교양/비사대교직/전공선택(교직)/대학기초/전공기초/전공 조건 설정 후, 각각 결과로 나온 파일을 다운받습니다.
교과목 구분인 이유 : 중복이 없고 빠진 강의도 없기에 가장 적합한 조건입니다.
학점 교환 강의의 경우 : 폼이 다르기도 하고 강의계획서도 없어서, 나중에 사이트 자체의 정보만 가져오는 방식으로 데이터베이스에 추가할 계획입니다.
'''
for i in range(1, 7):
    #드롭다운 박스 클릭
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
    #print(soup.text)    #텍스트가 출력됨
    #print(soup.prettify())  #html이 깔끔히 출력됨

    # 해당 검색결과가 없을 경우 패스할 수 있는 코드
    if soup.find("div", id = 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_0_cell_0_0') == None:
        pass
    else:
        '''
          만약 조회 결과가 존재할 경우, 마지막까지 다운로드 버튼을 누름
          
          column 값 >
         0 : 순번 | 1 : 학수번호 | 2 : 분반 | 3 : 교과목명
         4 : 교과목구분 | 5 : 교과영역 | 6 : 개설 학과 | 7 : 학년 | 8 : 교수명
         9 : 학점 | 10 : 시간 | 11 : 요일 | 12 : 교시 | 13 : 교실
         14 : 국문 | 15 : 영문 | 16 : FILE | 17 : URL
         18 : 영어강의 | 19 : 원어강의 | 20 : 원격강의 | 21 : 인문학관련교양과목 | 22 : SW과목
         23 : 정원 | 24 : 수업방식 | 25 : 비고
         
         파일명을 통일해서 저장합니다.
         통일할 파일명은 다음과 같습니다: 교과목명_분반_교수_강의계획안번호.파일형식
        '''

        #파일 처음부터 끝까지 받기
        Temp = 1    #반복문용 변수
        count = 0   # element 이름의 row 숫자를 갱신해주는 변수 (0~17)
        Total = 0   #현재까지 저장한 강의의 row 수

        # 총 건수가 오른쪽 화면에 뜨므로, 그 숫자를 가져와 숫자만금 반복하여 파일을 저장합니다.
        tempText = driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_stcTextTextBoxElement').text
        if "총건수" in tempText:
             tempList = tempText.split(':')
             tempText = tempList[1].replace(' ','')
             tempText = tempText.replace(']','')
             tempText = int(tempText)
             print("Total : " + str(tempText))  #총 건수를 tempText에 int 형태로 저장합니다.

        while(Temp == 1):
             Total += 1     #현재 반복한 횟수. tempText와 계속 비교하여 더 반복할지를 결정합니다.

             # 다 돌았을 경우
             if (Total > tempText):
                 print("다 돌았다\n")
                 break

            # ROW를 발견하지 못했을 경우
             if soup.find("div",id ='mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_'+str(count)+'_cell_'+str(count)+'_0') == None:
                 print("이 행이 없는 것 같다\n")
                 break

            # 아직 다 돌지 않았고, ROW도 발견했을 경우
             else:

                 # 저장할 파일명을 지정합니다.
                 # className은 강의명입니다.
                 className = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_3').text
                 # classNum은 학수번호입니다.
                 classNum = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_2').text
                 # professor은 교수명입니다.
                 professor = driver.find_element_by_id(
                     'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                         count) + '_cell_' + str(count) + '_8').text

                 # 간혹 파일명에 들어가서는 안 되는 값이 있기에, 해당 문자를 다른 문자로 치환해줍니다.
                 # 예외 > \, /, :, *, <, >, |, \n(엔터)
                 # 치환 > +, +, -, +, [, ], +, (없음)
                 className = className.replace("/","+")
                 className = className.replace("\\", "+")
                 className = className.replace(":", "-")
                 className = className.replace("*", "+")
                 className = className.replace("<", "[")
                 className = className.replace(">", "]")
                 className = className.replace("|", "+")
                 className = className.replace("\n", "")
                 professor = professor.replace("/","+")
                 professor = professor.replace("\\", "+")
                 professor = professor.replace(":", "-")
                 professor = professor.replace("*", "+")
                 professor = professor.replace("<", "[")
                 professor = professor.replace(">", "]")
                 professor = professor.replace("|", "+")
                 professor = professor.replace("\n","")

                 new_filename = className + "_" + classNum + "_" + professor + "_"
                 # 이후 뒤에 강의계획안번호와 파일형식을 붙일 예정

                 print("count: "+str(count))

                 # 하나의 강의에 올라온 모든 파일 받기 (최대 4개)
                 for number in range(14, 18):

                     # html 갱신
                     soup = BeautifulSoup(driver.page_source, "html.parser")

                    #시간 절약을 위해 칸이 비어있으면 패스합니다.
                     if soup.find('div', id = 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_'
                                              +str(count)+'_cell_'+str(count)+'_'+str(number)+'_controlexpand') == None:
                         print(str(number)+" 칸이 비었다 \n")
                         pass

                    #비어있지 않을 경우
                     else:
                         number = str(number)   # number을 str으로 변환하여 element를 찾는다.

                         # 14와 15는 각각 국문과 영어로, 새탭으로 열리는 강의계획안입니다.
                         if number == "14" or number =="15":
                             print("돋보기 칸 찾았다\n")

                             target = driver.find_element_by_id(
                                'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                                    count) + '_cell_' + str(count) + '_' + number)
                             #강의계획안을 새탭으로 열리게 합니다.
                             ActionChains(driver).key_down(Keys.CONTROL).click(target).key_up(Keys.CONTROL).perform()
                             time.sleep(2)
                             # 새로 열린 탭으로 화면을 이동합니다.
                             driver.switch_to.window(driver.window_handles[1])

                            #전체화면 스크린샷을 찍어, png로 저장합니다.
                             ss = Screenshot_Clipping.Screenshot()
                             ss.full_Screenshot(driver, save_path= downloadPath, image_name= r"\temp.png")
                             # 하단이 살짝 잘려서 저장되는 문제가 있습니다. 해결할 계획입니다.

                            # 현재 화면을 닫습니다.
                             driver.close()
                             # 원래의 페이지로 돌아갑니다.
                             driver.switch_to.window(driver.window_handles[0])

                        # 16은 이미지를 누르면 파일을 다운받는 방식입니다.
                         if number == "16":
                             print("파일 칸 찾았다\n")
                             driver.find_element_by_id(
                                'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_body_gridrow_' + str(
                                    count) + '_cell_' + str(count) + '_' + number).click()

                        # URL을 올리신 교수님은 없었기에, 특별한 코드를 작성하지 않았습니다. 확인된다면 추가하겠습니다.
                         if number == "17" :
                            print("URL 찾았다 \n")

                        #꼭 time sleep이 필요함.
                         time.sleep(2)

                         # 파일명 변경은 selenium에서 할 수 없기에 따로 코드를 짜야 합니다.
                         # 나중에 다른 python 파일로 분류하면 좋을 것 같습니다.

                         # 가장 최근에 다운받아진 파일을 대상으로 이름을 변경합니다. 따라서 파일 다운 순서가 꼬이지 않도록 주의해야 합니다.
                         filename = max([downloadPath + '\\' + f for f in os.listdir(downloadPath)],
                                        key=os.path.getctime)
                         # 다운이 덜 되었을 때, 즉 다운 도중일 때 crdownload라는 형식의 파일이 생기는데,
                         # 이 때 그냥 다음으로 넘어가면 앞서 말했듯이 파일 순서가 꼬일 우려가 있으므로 while문을 이용하여 멈춰줍니다.
                         temp = 1
                         while (temp == 1):
                             if "crdownload" in filename:  # 아직 저장이 덜 되었을 때 생김
                                 temp = 1
                             else:
                                 temp = 0

                         print(filename)    # 변경 전 파일명을 출력해봅니다.

                         # 파일 형식을 얻어 변경하게 될 파일명 뒤에 붙여야 합니다.
                         list_filename = filename.split(".")
                         lenmax = len(list_filename)
                         fileEx = list_filename[lenmax-1]   # fileEx가 파일 형식입니다.

                         print(new_filename + number + "." + fileEx)        #변경 이후 파일명을 출력해봅니다.

                         #파일명을 변경합니다.
                         shutil.move(os.path.join(downloadPath, filename),
                                     os.path.join(downloadPath, new_filename + number + "." + fileEx))
                         time.sleep(1)


                # 현재 화면에 없는 element과 상호작용할 수 없습니다.
                 # 따라서 전체 화면의 브라우저 스크롤 가장 밑으로 내립니다. *강의계획안 사이트에는 전체 스크롤과 그리드 스크롤이 있습니다.
                 attr = {'id': 'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_incbuttonAlignImageElement',
                         'style': 'user-select: none; position: absolute; left: 0px; top: 0px; width: 15px; height: 15px; background-repeat: no-repeat; background-position: center center; background-image: url("/eureka/my/nxc/_theme_/theme/base/scr_WF_VerincN.png");'}
                 if soup.find('div', attrs=attr) != None:
                    for i in range(0, 4):
                        driver.find_element_by_id('mainframe_VFrameSet_WorkFrame_Child__form_div_Work_vscrollbar_incbuttonAlignImageElement').click()


                 # 그리드 스크롤을 1칸 내립니다.
                 attr = {'id':'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_vscrollbar_incbutton', 'style' : 'user-select: none; position: absolute; overflow: hidden; left: 0px; top: 478px; width: 15px; height: 15px; border-radius: 0px; background-color: transparent; cursor: pointer;'}
                 if soup.find('div', attrs = attr) != None:
                     driver.find_element_by_id(
                         'mainframe_VFrameSet_WorkFrame_Child__form_div_Work_grxMain_vscrollbar_incbuttonAlignImageElement').click()

                # 파일 row는 0~17마다 element명이 갱신됩니다.
                # 따라서 count를 이용하여 해당 번호를 붙여줍니다.
                 count = (count+1)%18

         # 다운로드가 끝났으면 다시 최상단으로 스크롤을 돌려야 합니다.
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

# 해당 학기의 파일을 모두 다운받았습니다.
print("완료")

#이후 일정 주기로 해당 학기의 파일을 다시 일괄적으로 다운받아 갱신합니다.
# 학기 초일수록 자주, 학기가 시작된 이후에는 드물게 갱신하도록 구현하게 될 예정입니다.
time.sleep(100)



"""
앞으로의 과제
** 파일 다운로드 경로 및 방법
django 서버에 업로드할 수 있어야 함. > element를 찾을 수 없는 오류가 발생. window와 linux의 차이?
1) 가상환경에 저장 후 업로드하는 방법 
2) download link를 얻는 방법을 알아내기
=> 1)의 경우 mysql에 저장하는 내용은 가상환경의 파일경로가 될 것이고, 2)의 경우 mysql에 저장하는 내용은 download link가 될 것입니다.

* 구동시간에 대하여 *
이 코드는 오류를 방지하기 위해 sleep을 많이 사용하고, selenium 자체가 느리기 때문에 구동 시간이 깁니다. 
한 과목 저장에 대략 4초 정도 걸리는 것 같고,
강의 수가 2000개라고 가정했을 때 한 번 한 학기를 갱신하는 데 2~3시간 쯤 걸릴 것 같습니다.
속도가 중요한 시스템이 아니므로 괜찮을 것 같지만, 이후 개선을 고려하고 있습니다.
"""
