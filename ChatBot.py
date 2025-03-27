import nltk
import numpy as np
import random
import string 
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from fuzzywuzzy import process
import re 

class ChatBot():
    API_KEY = "3e95ca7740038bb5e66cf609dfaaf482"  

    def __init__(self):
        self.qa_dict = {}
        self.last_request = None  # 🔥 Nhớ trạng thái câu hỏi gần nhất
        self.last_city = None  # 🔥 Nhớ tên thành phố gần nhất
        file_path = 'chatbot.txt'
        if not os.path.exists(file_path):
            print(f"Lỗi: Không tìm thấy file {file_path}")
            exit()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().strip().split("\n")

        current_question = None
        for line in lines:
            if line.startswith("Câu hỏi:"):
                current_question = line.replace("Câu hỏi:", "").strip().lower()
            elif line.startswith("Trả lời:") and current_question:
                self.qa_dict[current_question] = line.replace("Trả lời:", "").strip()
                
    def get_faq_response(self, user_input):
        """Tìm câu hỏi phù hợp với ưu tiên từ khóa và fuzzy matching"""
        user_input = user_input.lower().strip()

        # Danh sách từ khóa quan trọng liên kết với câu hỏi chuẩn
        keyword_mapping = {
            "hủy đơn": "Tôi có thể hủy đơn hàng sau khi đã đặt không?",
            "đổi trả": "Tôi muốn đổi trả hàng, phải làm sao?",
            "vận chuyển": "Phí vận chuyển được tính như thế nào?",
            "kiểm tra đơn": "Tôi có thể kiểm tra trạng thái đơn hàng của mình ở đâu?",
            "bảo hành": "Chính sách bảo hành sản phẩm như thế nào?",
            "thanh toán": "Tôi có thể thanh toán bằng phương thức nào?",
        }

        # Kiểm tra xem có từ khóa quan trọng trong câu hỏi không
        for keyword, correct_question in keyword_mapping.items():
            if keyword in user_input:
                return self.qa_dict.get(correct_question, "Xin lỗi, tôi chưa hiểu câu hỏi của bạn.")

        # Nếu không có từ khóa, sử dụng fuzzy matching
        best_match, score = process.extractOne(user_input.lower(), self.qa_dict.keys())

        if score > 80:  # Giảm ngưỡng xuống 70% để nhận diện câu hỏi thiếu từ
            return self.qa_dict[best_match]

        return "Xin lỗi, tôi chưa hiểu câu hỏi của bạn. Bạn có thể hỏi lại theo cách khác không?"

    @staticmethod
    def LemTokens(tokens):
        lemmer = nltk.stem.WordNetLemmatizer()
        return [lemmer.lemmatize(token) for token in tokens]

    @staticmethod
    def LemNormalize(text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        return ChatBot.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    @staticmethod
    def greeting(sentence):
        GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey", "chào")
        GREETING_RESPONSES = ["Hi!", "Hey!", "Hello!", "Chào bạn!", "Xin chào!"]
        sentence = sentence.lower()
        best_match, score = process.extractOne(sentence, GREETING_INPUTS)
        for word in sentence.split():
            if score > 80:
                return random.choice(GREETING_RESPONSES)
        return None

    @staticmethod
    def get_weather(city):
        """Lấy dữ liệu thời tiết từ OpenWeatherMap API"""
        if not city or len(city.split()) > 3:  # 🔥 Chặn trường hợp nhập cả câu dài
            return "Tên thành phố không hợp lệ. Hãy nhập lại tên thành phố ngắn gọn."

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={ChatBot.API_KEY}&units=metric&lang=vi"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if "main" in data:
                temp = data['main']['temp']
                weather = data['weather'][0]['description']
                return f"🌤️ Thời tiết tại **{city.capitalize()}**: {weather}, {temp}°C."
            else:
                return f"Không tìm thấy thông tin thời tiết cho thành phố **{city}**. Hãy kiểm tra lại tên!"
        
        except requests.exceptions.HTTPError as e:
            return f"Lỗi: Thành phố **{city}** không tồn tại. Hãy kiểm tra lại tên!"
        except requests.exceptions.RequestException as e:
            return f"Lỗi khi lấy dữ liệu thời tiết: {str(e)}"

    def extract_city(self, user_response):
        """Tìm tên thành phố từ câu hỏi của người dùng"""
        blacklist = ["thời tiết", "ở", "tại", "hôm nay", "hiện tại", "như thế nào", "?"]
        words = user_response.lower().split()

        city = " ".join([word for word in words if word not in blacklist])

        if not city:
            match = re.search(r"thời tiết.*?ở (.+)", user_response)
            if match:
                city = match.group(1)

        return city.strip() if len(city.split()) <= 3 else ""  # 🔥 Chỉ nhận tối đa 3 từ

    def response(self, user_response):
        """Xử lý câu hỏi bằng mô hình TF-IDF"""
        self.sent_tokens.append(user_response)
        TfidfVec = TfidfVectorizer(tokenizer=lambda text: ChatBot.LemNormalize(text), stop_words='english')
        tfidf = TfidfVec.fit_transform(self.sent_tokens)

        vals = cosine_similarity(tfidf[-1], tfidf[:-1])
        idx = vals.argsort()[0][-1]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-1]

        self.sent_tokens.pop()

        if req_tfidf == 0:
            return "Xin lỗi, tôi không hiểu bạn nói gì."
        else:
            return self.sent_tokens[idx]

    def Chat_with_Bot(self, user_response):
        user_response = user_response.lower().strip()

        # 🔥 Nếu trước đó hỏi thời tiết nhưng chưa nhập thành phố, chatbot sẽ hỏi lại
        if self.last_request == "weather_request":
            self.last_request = None  
            self.last_city = user_response  # Nhớ lại thành phố
            return self.get_weather(user_response)

        # 🔥 Nếu chỉ hỏi "thời tiết", lấy thành phố trước đó
        if user_response == "thời tiết" and self.last_city:
            return self.get_weather(self.last_city)

        # Nếu câu chứa "thời tiết", thử tìm thành phố
        if self.last_request == "weather_request":
            self.last_request = None  
            self.last_city = user_response  
            return self.get_weather(user_response)

        if user_response == "thời tiết" and self.last_city:
            return self.get_weather(self.last_city)

        if "thời tiết" in user_response:
            city = self.extract_city(user_response)
            if city:
                self.last_city = city  
                return self.get_weather(city)
            else:
                self.last_request = "weather_request"  
                return "Bạn muốn xem thời tiết ở đâu? Hãy nhập tên thành phố."

        # Reset trạng thái nếu câu không liên quan đến thời tiết
        self.last_request = None

        # Chào hỏi
        greeting_res = ChatBot.greeting(user_response)
        if greeting_res:
            return greeting_res

        # Xử lý câu hỏi trong chatbot.txt
        return self.get_faq_response(user_response)
