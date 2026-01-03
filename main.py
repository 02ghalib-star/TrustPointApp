import json, os
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.core.window import Window

# কিবোর্ড এবং স্ক্রিন অ্যাডজাস্টমেন্ট
Window.softinput_mode = "below_target"

DATA_FILE = "trustpoint_final.json"
ADMIN_PHONE = "01234567890" # আপনার নম্বর দিন

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f: return json.load(f)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

KV = '''
ScreenManager:
    LoginScreen:
    RegisterScreen:
    DashboardScreen:

<LoginScreen>:
    name: "login"
    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": .5}
            MDLabel:
                text: "TrustPoint Login"
                font_style: "H4"
                halign: "center"
            MDTextField:
                id: phone
                hint_text: "Mobile Number"
                mode: "rectangle"
            MDRaisedButton:
                text: "LOGIN"
                pos_hint: {"center_x": .5}
                size_hint_x: 0.9
                on_release: root.do_login()
            MDFlatButton:
                text: "Don't have an account? Register"
                pos_hint: {"center_x": .5}
                on_release: app.root.current = "register"

<RegisterScreen>:
    name: "register"
    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: "20dp"
            spacing: "15dp"
            adaptive_height: True
            pos_hint: {"center_x": .5, "center_y": .5}
            MDLabel:
                text: "Create Account"
                font_style: "H4"
                halign: "center"
            MDTextField:
                id: new_phone
                hint_text: "Enter Mobile Number"
                mode: "rectangle"
            MDRaisedButton:
                text: "REGISTER NOW"
                pos_hint: {"center_x": .5}
                size_hint_x: 0.9
                on_release: root.do_register()

<DashboardScreen>:
    name: "dashboard"
    MDBoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            title: "TrustPoint Dashboard"
        ScrollView:
            MDGridLayout:
                cols: 1
                adaptive_height: True
                padding: "15dp"
                spacing: "15dp"
                MDCard:
                    size_hint_y: None
                    height: "100dp"
                    padding: "15dp"
                    MDLabel:
                        id: balance_label
                        text: "Balance: 0.00 TK"
                        halign: "center"
                        font_style: "H5"
                
                MDGridLayout:
                    cols: 2
                    spacing: "10dp"
                    size_hint_y: None
                    height: self.minimum_height
                    
                    MDFillRoundFlatIconButton:
                        icon: "play-circle"
                        text: "Daily Ads"
                        on_release: app.add_money()
                    MDFillRoundFlatIconButton:
                        icon: "wallet"
                        text: "Withdraw"
                        on_release: app.show_msg("Withdraw", "Withdraw system will be available soon!")
                    MDFillRoundFlatIconButton:
                        icon: "account"
                        text: "Profile"
                        on_release: app.show_msg("Profile", f"User: {app.current_user}")
                    MDFillRoundFlatIconButton:
                        icon: "history"
                        text: "History"
                        on_release: app.show_msg("History", "No payment history found.")
                    MDFillRoundFlatIconButton:
                        icon: "account-multiple"
                        text: "Refer"
                        on_release: app.show_msg("Refer", "Your referral code is your phone number.")
                    MDFillRoundFlatIconButton:
                        icon: "help-circle"
                        text: "Support"
                        on_release: app.show_msg("Support", "Contact us at support@trustpoint.com")
                    MDFillRoundFlatIconButton:
                        icon: "shield-check"
                        id: admin_btn
                        text: "Admin"
                        on_release: app.show_msg("Admin", "Welcome to Admin Panel")
                
                MDRaisedButton:
                    text: "LOGOUT"
                    md_bg_color: "red"
                    pos_hint: {"center_x": .5}
                    on_release: app.root.current = "login"
'''

class LoginScreen(Screen):
    def do_login(self):
        phone = self.ids.phone.text
        data = load_data()
        if phone in data["users"]:
            app = MDApp.get_running_app()
            app.current_user = phone
            app.root.get_screen('dashboard').ids.balance_label.text = f"Balance: {data['users'][phone]['balance']} TK"
            app.root.get_screen('dashboard').ids.admin_btn.opacity = 1 if phone == ADMIN_PHONE else 0
            app.root.current = "dashboard"

class RegisterScreen(Screen):
    def do_register(self):
        phone = self.ids.new_phone.text
        if phone:
            data = load_data()
            if phone not in data["users"]:
                data["users"][phone] = {"balance": 0.0}
                save_data(data)
                MDApp.get_running_app().show_msg("Success", "Registration Successful!")
                self.manager.current = "login"

class DashboardScreen(Screen):
    pass

class TrustPointApp(MDApp):
    current_user = ""
    dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def show_msg(self, title, text):
        self.dialog = MDDialog(
            title=title, text=text, 
            buttons=[MDRaisedButton(text="OK", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()

    def add_money(self):
        data = load_data()
        data["users"][self.current_user]["balance"] += 2.0
        save_data(data)
        self.root.get_screen('dashboard').ids.balance_label.text = f"Balance: {data['users'][self.current_user]['balance']} TK"
        self.show_msg("Earned", "You earned 2.0 TK from Daily Ads!")

if __name__ == "__main__":
    TrustPointApp().run()