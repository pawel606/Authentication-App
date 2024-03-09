import os.path
import subprocess
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import requests
import mysql.connector
from twilio.rest import Client

import util


class App:
    def __init__(self):

        self.main_window = tk.Tk()
        self.main_window.geometry("1200x500+350+100")
        self.main_window.title("STAH App")

        self.login_button_main_window = util.get_button(self.main_window, 'Zaloguj sie', 'green', self.login)
        self.login_button_main_window.place(x=750, y=300)

        #self.register_button_main_window = util.get_button(self.main_window, 'Zarejestruj użytkownika', 'grey',
        #                                                   self.register_new_user, fg='black')
        #self.register_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        
        self.entry_text_ID = util.get_entry_text(self.main_window)
        self.entry_text_ID.place(x=750, y=150)
        
        self.text_label_ID = util.get_text_label(self.main_window,'ID:')
        self.text_label_ID.place(x=750, y=70)

        self.add_webcam(self.webcam_label)


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label

        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame #CV2 format

        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        self.most_recent_capture_pil = Image.fromarray(img_) #Pillow format

        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        unknown_img_path = r'.\tmp.jpg'
        id = self.entry_text_ID.get(1.0, "end-1c")
        
        db = mysql.connector.connect(
        	host="localhost",
        	user="root",
        	password="kali",
        	database="employees"
        )
        
        mycursor = db.cursor()
        
        sql = "SELECT photo_link FROM doctors WHERE id = {}".format(id)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        result = []
        for x in myresult:
        	result.extend(x)
        
        photo_link = requests.get(result[0])
        self.dataBaseImage = r'dbImage'
        if not os.path.exists(self.dataBaseImage):
        	os.makedirs(self.dataBaseImage)
        open(r'dbImage/personImage.jpg', "wb").write(photo_link.content)

        cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
        output = str(subprocess.check_output(['face_recognition', self.dataBaseImage, unknown_img_path ]))
        name = output.split(',')[1][:-3]
        
        os.remove(unknown_img_path)
        os.remove(r'dbImage/personImage.jpg')
        os.removedirs(self.dataBaseImage)

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box("Autoryzacja zakończona fiaskiem", 'Nieznany użytkownik. Proszę spróbuj ponownie albo skontaktuj sie z przełozonym')
        else:
            sql2 = "SELECT name FROM doctors WHERE id = {}".format(id)
            sql3 = "SELECT phone_number FROM doctors WHERE id = {}".format(id)
            mycursor.execute(sql2)
            myresult2 = mycursor.fetchall()
            mycursor.execute(sql3)
            myresult3 = mycursor.fetchall()
            result2 = []
            for x in myresult2:
            	result2.extend(x)
            for x in myresult3:
            	result2.extend(x)
            	
            	
            person_name = result2[0]
            self.person_phone = result2[1]
            util.msg_box("Autoryzacja zakończona sukcesem", 'Witaj, {}'.format(person_name))
            self.sms_authentication()
        
    
    def sms_authentication(self):
    	self.main_window.withdraw()
    	self.sms_window = tk.Toplevel(self.main_window)
    	self.sms_window.geometry("500x500")
    	
    	self.text_label_sms = util.get_text_label(self.sms_window, 'Podaj kod SMS:')
    	self.text_label_sms.place(x=100, y=50)
    	
    	self.entry_text_sms = util.get_entry_text(self.sms_window)
    	self.entry_text_sms.place(x=100, y=150)
    	account_sid = "AC457c8dde89fe46ed30dcaebff0440c4e"
    	auth_token = "b9556259b8758935934cb34908cf297f"
    	self.verify_sid = "VA58b2545dd860f29b65896dae409180ca"
    	self.verified_number = "+48{}".format(self.person_phone)
    	
    	self.client = Client(account_sid, auth_token)
    	
    	verification = self.client.verify.v2.services(self.verify_sid) \
    		.verifications \
    		.create(to=self.verified_number, channel="sms") #call
    	#print(verification.status)
    	
    	
    	self.accept_button = util.get_button(self.sms_window, "Akceptuj", "green", self.verifyCode)
    	self.accept_button.place(x=100, y=250)
    	
    
    
    def verifyCode(self):
    	otp_code = self.entry_text_sms.get(1.0, "end-1c")
    	
    	verification_check = self.client.verify.v2.services(self.verify_sid) \
    	.verification_checks \
    	.create(to=self.verified_number, code=otp_code)
    	print(verification_check.status)
    	if verification_check.status == 'pending':
    		util.msg_box("Sukces", 'Kod SMS niepoprawny')
    		#print("Niepoprawny kod")
    		self.sms_window.destroy()
    		self.main_window.deiconify()
    	else:
    		#print("Dostęp uzyskany")
    		util.msg_box("Sukces", 'Uzyskano dostep')
    		self.sms_window.destroy()
    		self.main_window.destroy()
    
    def register_new_user(self):
        self.main_window.withdraw()
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_user_window = util.get_button(self.register_new_user_window, "Akceptuj", "green", self.accept_new_user)
        self.accept_button_register_user_window.place(x=750, y=300)

        self.try_again_button_register_user_window = util.get_button(self.register_new_user_window, "Spróbuj ponownie", "red", self.try_again_new_user)
        self.try_again_button_register_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, 'Podaj proszę swoje\nimię i nazwisko:')
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_new_user(self):
        self.register_new_user_window.destroy()
        self.main_window.deiconify()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c")

        cv2.imwrite(os.path.join(self.db_dir, '{}.jpg'.format(name)), self.register_new_user_capture)

        util.msg_box('Sukces', 'Użytkownik został zarejestrowany')

        self.main_window.deiconify()
        self.register_new_user_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
