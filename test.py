import ctypes
import datetime
import json
import os
import re
import sys
import time
import urllib.request as urllib2
import webbrowser
from time import strftime
import playsound
import pyttsx3
import requests
import speech_recognition as sr
import wikipedia
from gtts import gTTS
from webdriver_manager.chrome import ChromeDriverManager
from youtube_search import YoutubeSearch

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

#chuyển văn bản thành giọng nói
def speak(text):
    print("Trí tuệ AI: ",text)
    
    tts = gTTS(text = text , lang = language , slow = False)
    tts.save("noi.mp3")  #lưu giọng nói
    playsound.playsound("noi.mp3" , True)
    os.remove("noi.mp3")  #xóa file sau mỗi lần nói
    
    robot_mouth = pyttsx3.init()
    '''
    voices = robot_mouth.getProperty('voices')
    rate = robot_mouth.getProperty('rate')
    volume = robot_mouth.getProperty('volume')
    robot_mouth.setProperty('volume', volume - 0.0)  # tu 0.0 -> 1.0
    robot_mouth.setProperty('rate', rate - 50)
    robot_mouth.setProperty('voice', voices[1].id)
    robot_mouth.say(text)
    robot_mouth.runAndWait()
    '''

#chuyển giọng nói (âm thanh) thành văn bản

def get_audio():
    robot_aer = sr.Recognizer()
    with sr.Microphone() as mic:  #dùng mic của máy để nghe người dùng nói
        print("Trí tuệ AI: đang nghe.....!")
        audio = robot_aer.listen(mic , phrase_time_limit=5) #truyền vào âm thanh thu dc từ mic vào biến audio, để bot nghe trong 8s
        try: #nhận dạng giọng nói
            text = robot_aer.recognize_google(audio, language = "vi-VN") # nhận dạng âm thanh ở biến audio chuyển thành văn bản
            print("Người nói: ", text)
            return text
        except: #nếu lỗi
            print("Trí tuệ AI: Mình không nghe rõ ạ...")
            return 0
'''
def get_audio_2():
    ear_robot = sr.Recognizer()
    with sr.Microphone() as source:
        ear_robot.pause_threshold = 2
        print("Trí tuệ AI: đang nghe.....!")
        audio = ear_robot.listen(source)
    try:
        text = ear_robot.recognize_google(audio, language="vi-VN")
    except:
        speak("Nhận dạng giọng nói thất bại. Vui lòng nhập lệnh ở dưới")
        text = input("Mời nhập: ")
    return text.lower()
'''

def stop():
    speak("Tạm biệt bạn, hẹn gặp lại lần sau!")


#máy tính sẽ cố gắng nhận dạng âm thanh của người đọc tối đa 3 lần cho đến khi máy tính nghe rõ
def get_text():
    for i in range(3): #vòng lặp sẽ chạy 3 lần
        text = get_audio()  #nghe những gì nghe được sẽ chuyển thành văn bản
        if text : #nếu true or !=0 thì if sẽ được thực hiện
            return text.lower()
        elif i < 2:
            speak("Mình không nghe rõ, bạn có thể nói lại được không?")
    time.sleep(4) #chương trình sẽ tạm dừng trong 4s
    stop()
    return 0


def hello(name):
    day_time = int(strftime('%H'))
    if 0 <= day_time < 11:
        speak(f'Xin chào {name}. Chúc bạn một buổi sáng tràn đầy năng lượng')
        speak("Bạn cần mình giúp gì không?: ")
    elif 11 <= day_time < 13 :
        speak(f'Xin chào {name}. Buổi trưa làm việc tốt nha')
        speak("Bạn cần mình giúp gì không?: ")
    elif 13<= day_time < 18 :
        speak(f'Xin chào {name}. Buổi chiều hãy giữ vững năng lượng cho ngày dài nha')
        speak("Bạn cần mình giúp gì không?: ")
    elif 18<= day_time < 22 :
        speak(f'Xin chào {name}. Chào buổi tối, hãy nhớ ngủ đúng giờ để mai thoải mái nha')
        speak("Bạn cần mình giúp gì không?: ")
    elif 22<= day_time < 23 :
        speak(f'Xin chào {name}. Khuya rồi sao chưa đi ngủ vậy bạn')
        speak("Bạn cần mình giúp gì không?: ")
    else:
        speak(f'Xin chào {name}. Một ngày vui vẻ.')


def get_time(text):
    now = datetime.datetime.now()
    if "giờ" in text:
        speak(f" Bây giờ là {now.hour} giờ {now.minute} phút {now.second} giây")
    elif "ngày" in text:
        speak(f" Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}")
    else:
        speak("Mình chưa biết bạn đang nói gì (:3_\)_")


def open_app(text):
    if "google" in text:
        speak("Mở Chrome nào")
        os.system("C:\\Program Files\\CocCoc\\Browser\\Application\\browser.exe")
        #mở ứng dụng dẽ ko tắt chương trình, tắt ứng dụng thì mới tắt chương trình
    elif "zalo" in text:
        speak(" Zalo hạn chế nên bạn ít dùng nhỉ")
        os.system("C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Zalo\\Zalo.exe")
    elif "studio code" in text:
        speak(" Nào chúng ta cùng code thôi")
        os.system("C:\\Users\\ADMIN\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
    else:
        speak("Ứng dụng chưa cài đặt rồi. Bạn quên rồi sao?")


def open_web(text):
    reg_ex = re.search('mở (web+)' , text)
    if reg_ex:
        domain = reg_ex.group(1)
        url = "https://www." + domain
        webbrowser.open(url)
        speak("Trang web bạn yêu cầu đã được mở ạ. ")
        if input("hãy nhập a để tiếp tục: ") == "a": #sau khi mở web thì chương trình sẽ dừng lại đến khi bạn nhập "a"
            pass
        return True
    else:
        return False


def open_google_search():
    speak("Bạn cần tìm  trên Google vậy?:..")
    search = str(get_text()).lower()
    url = f"https://www.google.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Đây là thông tin về {search} bạn tìm được trên Google đó')


def open_youtube_search():
    speak("Bạn muốn xem gì trên Youtube vậy?:..")
    search = str(get_text()).lower()
    url = f"https://www.youtube.com/search?q={search}"
    webbrowser.get().open(url)
    speak(f'Đây là trang video {search} bạn tìm trên Youtube')


def open_youtube_2():
    speak("Bạn muốn xem video gì trên Youtube vậy?:..")
    search = get_text()
    while True:
        result = YoutubeSearch(search, max_results=10).to_dict()
        if result:
            break
    url = f"https://www.youtube.com" + result[0]['url_suffix']
    webbrowser.get().open(url)
    speak(f'Đây là video {search} bạn tìm trên Youtube')
    print(result)

def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu vậy ạ?")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?" # Đường dẫn trang web để lấy dữ liệu về thời tiết
    city = get_text()   # lưu tên thành phố vào biến city
    if not city:    # nếu biến city != 0 và = False thì để đấy ko xử lí gì cả
        pass
    api_key = "321736900281f24ef0a888c9112b0758"    # api_key lấy trên open weather map
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"    # tìm kiếm thông tin thời thời tiết của thành phố
    # truy cập đường dẫn lấy dữ liệu thời tiết
    response = requests.get(call_url) #gửi yêu cầu lấy dữ liệu
    data = response.json()    # lưu dữ liệu thời tiết dưới dạng json và cho vào biến data
    if data["cod"] != "404":     # kiểm tra nếu không gặp lỗi 404 thì xem xét và lấy dữ liệu
        # lấy dữ liệu của key main
        city_res = data["main"]
        # nhiệt độ hiện tại
        current_temperature = city_res["temp"]
        # áp suất hiện tại
        current_pressure = city_res["pressure"]
        # độ ẩm hiện tại
        current_humidity = city_res["humidity"]
        # thời gian mặt trời
        suntime = data["sys"]
        # 	lúc mặt trời mọc, mặt trời mọc
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        # lúc mặt trời lặn
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        # thông tin thêm
        wthr = data["weather"]
        # mô tả thời tiết
        weather_description = wthr[0]["description"]
        # Lấy thời gian hệ thống cho vào biến now
        now = datetime.datetime.now()
        # hiển thị thông tin với người dùng
        content = f"""
        Hôm nay là ngày {now.day} tháng {now.month} năm {now.year}
        Bình minh vào {sunrise.hour} giờ {sunrise.minute} phút
        Hoàng hôn vào {sunset.hour} giờ {sunset.minute} phút
        Nhiệt độ trung bình là {current_temperature} độ C
        Độ ẩm là {current_humidity}%
        Áp suất không khí là {current_pressure} héc tơ Pascal
        """
        speak(content)
    else:
        # nếu tên thành phố không đúng thì nó máy tính nói
        speak("Không tìm thấy địa chỉ bạn muốn.")


# url = 'https://api.unsplash.com/photos/random?client_id=' + \
#       api_key
def change_wallpaper():
    api_key = "RF3LyUUIyogjCpQwlf-zjzCf1JdvRwb--SLV6iCzOxw"
    url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
    f = urllib2.urlopen(url) #lấy kết quả trả về của trang web
    json_string = f.read() #đọc dữ liệu ở trang web
    f.close() #đóng lại trình duyệt ẩn
    parsed_json = json.loads(json_string)  #xử lý dữ liệu
    photo = parsed_json['urls']['full'] #lấy ảnh ở link urls với chất lượng full
    urllib2.urlretrieve(photo, "G:\Ảnh\a.png") #tải về máy
    image = os.path.join("G:\Ảnh\a.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
    speak("Hình nền máy tính bạn đã được thay đổi. Bạn ra home xem có đẹp không ?")


def read_news():
    speak("Bạn muốn đọc báo về gì ạ")
    
    queue = get_text()
    params = {'apiKey': '6f82b36a92b9436290e981158e34c3fd',"q": queue, }

    api_result = requests.get('https://newsapi.org/v2/everything?', params)
    api_response = api_result.json()
    print("Tin tức")

    for number, result in enumerate(api_response['articles'], start=1):
        print(f"Tin {number}:\nTiêu đề: {result['title']}\nTrích dẫn: {result['description']}\nLink: {result['url']}")
        if number <= 3:
            webbrowser.open(result['url'])


def tell_me_about():
    try:
        speak("Bạn muốn tìm hiểu về gì ạ")
        text = get_text()
        contents = wikipedia.summary(text).split('\n')
        speak(contents[0])
        time.sleep(5)
        for content in contents[1:]:
            speak("Bạn muốn nghe thêm không?")
            ans = get_text()
            if "có" not in ans:
                break    
            speak(content)
            time.sleep(5)

        speak('Cảm ơn bạn đã lắng nghe!!!')
    except:
        speak("Mình không nghe được bạn nói gì. Bạn có thể nhắc lại được không?")

def help_me():
    speak("""Trí tuệ AI có thể giúp bạn thực hiện các việc sau đây:
    1. chào hỏi
    2. Hiển thị giờ
    3. Mở website, ứng dụng desktop
    4. Tìm kiếm với google
    5. Tìm kiếm video với youtube
    6. Dự báo thời tiết
    7. Đọc báo
    8. Thay đổi hình nền máy tính
    9. Tìm kiếm trong từ điển bách khoa toàn thư ( Wikipedia )
    10. Mở nhạc với youtube
    """)


def main_brain():
    speak("Xin chào bạn mình là Trí Tuệ AI. Rất vui khi gặp bạn! Hãy cho mình biết mật khẩu.")
    passs = get_text()
    name = "Ngô Sách Tiến"
    if(passs == "mở"):
        speak(f'xin chào bạn {name}.')
    else:
        speak("Sao mật khẩu không đúng nhỉ? Thôi Bye nha!")
        stop()
        sys.exit()
    if name :
        speak("Bạn cần mình giúp gì không")
        while True:
            text = get_text()

            if not text:
                break
            elif "tạm biệt" in text or "gặp lại" in text or "tắt điện" in text or "ngủ" in text or "nghỉ" in text:
                    stop()
                    break
            elif "xin chào" in text or "hello" in text or "rất vui" in text:
                hello(name)
            elif "bây giờ" in text:
                get_time(text)
            elif "mở " in text:
                if "web" in text:
                    open_web(text)
                else:
                    open_app(text)
            elif "google" in text:
                open_google_search()
                if input("Để tiếp tục y/n: ") == "y" :
                        pass
            elif 'youtube' in text:
                speak("Bạn muốn tìm trong trang ti kiếm hay xem video?")
                yeu_cau = get_text()
                if "kênh" in yeu_cau:
                    open_youtube_search()
                    if input("Để tiếp tục y/n: ") == "y" :
                        pass
                elif "video" in yeu_cau:
                    open_youtube_2()
                    if input("Để tiếp tục y/n: ") == "y":
                        pass
            elif "thời tiết" in text:
                current_weather()
            elif "hình nền" in text:
                change_wallpaper()
            elif "đọc báo" in text:
                read_news()
                if input("Bạn có muốn tiếp tục y/n: ") == "y" :
                        pass
            elif "định nghĩa" in text or "wiki" in text:
                tell_me_about()
            elif "chức năng" in text or "công việc" in text:
                help_me()
            elif "quẩy lên" in text or "nhảy" in text:
                meme = r"G:\Video Meme\rickroll.mp4"
                os.startfile(meme)
            else:
                speak(f'Chức năng này chưa có trong hệ thống nên bạn xem thêm những thứ khác nha.')

main_brain()