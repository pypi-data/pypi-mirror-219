def main():
    import tkinter as tk
    from tkinter import messagebox
    import sys
    import datetime
    import psutil
    from PIL import Image, ImageTk
    import platform

    def login():
        username = entry_username.get()
        password = entry_password.get()

        if username == "" and password == "":
            messagebox.showinfo("Başarılı", "Giriş başarılı!")
            window.withdraw()
            open_main_page()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya parola!")

    def python():
        class RedirectedOutput:
            def __init__(self, output_text):
                self.output_text = output_text

            def write(self, message):
                self.output_text.configure(state="normal")
                self.output_text.insert(tk.END, message)
                self.output_text.configure(state="disabled")
                self.output_text.see(tk.END)

        def execute_command():
            command = input_text.get("1.0", tk.END).strip()
            try:
                result = eval(command)
                print(result)
            except Exception as e:
                print(str(e))
            input_text.delete("1.0", tk.END)

        def exit_console():
            sys.exit()

        root = tk.Tk()
        root.title("Python Konsolu")
        root.attributes("-topmost", True)
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)

        input_text = tk.Text(input_frame, width=60, height=5)  # Yükseklik ayarı burada yapılıyor
        input_text.pack(side=tk.LEFT)

    #    execute_button = tk.Button(input_frame, text="Çalıştır", command=execute_command)
    #    execute_button.pack(side=tk.LEFT, padx=10)
        output_text = tk.Text(root, width=60, height=20)
        output_text.pack()

        exit_button = tk.Button(root, text="Çalıştır", command=execute_command)
        exit_button.pack(pady=10)

        # Çıktıyı yönlendir
        sys.stdout = RedirectedOutput(output_text)

        root.mainloop()

    def system_infos():
        def get_system_info():
        # İşletim sistemi bilgilerini al
            os_name = platform.system()
            os_version = platform.release()

            # İşlemci bilgilerini al
            processor = platform.processor()

            # Bellek bilgilerini al
            memory = psutil.virtual_memory()

            # Ekran çözünürlüğünü al
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            screen_resolution = f"{screen_width}x{screen_height}"

            # Bilgileri canvas üzerinde yazdır
            canvas.delete("all")
            canvas.create_text(200, 25, text="Donanım Bilgileri", font=("Arial", 14, "bold"), anchor="n")
            canvas.create_text(200, 50, text=f"İşletim Sistemi: {os_name} {os_version}", anchor="n")
            canvas.create_text(200, 75, text=f"İşlemci: {processor}", anchor="n")
            canvas.create_text(200, 100, text=f"Bellek: {memory.total // (1024 ** 3)} GB", anchor="n")
            canvas.create_text(200, 125, text=f"Ekran Çözünürlüğü: {screen_resolution}", anchor="n")

        def get_other_info():
            # Diğer verileri al ve canvas üzerinde yazdır (örneğin, kullanıcı adı, IP adresi, vb.)
            # Bu kısmı kendi ihtiyaçlarınıza göre düzenleyebilirsiniz
            canvas.create_text(200, 175, text="Diğer Bilgiler", font=("Arial", 14, "bold"), anchor="n")
            canvas.create_text(200, 200, text="Kullanıcı Adı: John Doe", anchor="n")
            canvas.create_text(200, 225, text="IP Adresi: 192.168.1.1", anchor="n")

        root = tk.Tk()
        root.title("Bilgisayar Bilgileri")

        # Canvas
        canvas = tk.Canvas(root, width=400, height=250)
        canvas.pack()
        root.attributes("-topmost", True)
        # Donanım bilgilerini al butonu
        button_get_system_info = tk.Button(root, text="Donanım Bilgilerini Al", command=get_system_info)
        button_get_system_info.pack(pady=10)

        # Diğer bilgileri al butonu
        button_get_other_info = tk.Button(root, text="Diğer Bilgileri Al", command=get_other_info)
        button_get_other_info.pack(pady=10)

        root.mainloop()

    def browser():
        import tkinter as tk
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        import sys

        class WebBrowser(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Tarayıcı")
                self.setGeometry(100, 100, 800, 600)

                self.web_view = QWebEngineView()
                self.setCentralWidget(self.web_view)

            def load_url(self, url):
                self.web_view.load(QUrl(url))
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Pencerenin en üstte kalmasını sağlar
                self.show()
                self.activateWindow()  # Pencereyi etkinleştirir

        def open_browser():
            app = QApplication(sys.argv)
            browser = WebBrowser()
            browser.show()
            app.exec_()

        root = tk.Tk()
        root.title("Web Tarayıcısı")
        #root.attributes("-fullscreen", True) 

        label = tk.Label(root, text="URL:")
        label.pack()

        entry = tk.Entry(root, width=50)
        entry.pack()

        button = tk.Button(root, text="Aç", command=open_browser)
        button.pack()

        root.mainloop()


    def google():
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        import sys

        class WebBrowser(QMainWindow):
            def __init__(self):
                super().__init__()
                self.setWindowTitle("Tarayıcı")
                self.setGeometry(100, 100, 800, 600)

                self.web_view = QWebEngineView()
                self.setCentralWidget(self.web_view)

            def load_url(self, url):
                self.web_view.load(QUrl(url))
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Pencerenin en üstte kalmasını sağlar
                self.show()
                self.activateWindow()  # Pencereyi etkinleştirir

                # Web tarayıcısını açmak için
        app = QApplication(sys.argv)
        browser = WebBrowser()
        browser.load_url("https://www.google.com")  # Görüntülemek istediğiniz URL'yi buraya yazın
        browser.show()
        app.exec_()

    def open_main_page():
        window2 = tk.Tk()
        window2.title("WixOS Arayüzü")

        # Pencere boyutu ve konumu
        screen_width = window2.winfo_screenwidth()
        screen_height = window2.winfo_screenheight()
        window2.geometry(f"{screen_width}x{screen_height}+1+1")

        # Pencereyi tam ekran yapma
        #window2.attributes("-fullscreen", True)

        def exit_program():
            def confirm_exit():
                if messagebox.askyesno("Çıkış", "Programdan çıkmak istediğinize emin misiniz?", parent=exit_window):
                    window2.destroy()  # Ana pencereyi kapat
                    sys.exit()  # Programı sonlandır

            exit_window = tk.Toplevel(window2)
            exit_window.title("Çıkış")
            exit_window.geometry("300x100")
            exit_window.resizable(False, False)
            exit_window.attributes("-topmost", True)  # Pencereyi en üste getir

            label_exit = tk.Label(exit_window, text="Programdan çıkmak istediğinize emin misiniz?")
            label_exit.pack(pady=10)

            button_yes = tk.Button(exit_window, text="Evet", command=confirm_exit)
            button_yes.pack(side="left", padx=10)

            button_no = tk.Button(exit_window, text="Hayır", command=exit_window.destroy)
            button_no.pack(side="right", padx=10)

            exit_window.mainloop()

            window2.deiconify()

        menu_bar = tk.Menu(window2)

        status_frame = tk.Frame(window2, relief="sunken")
        status_frame.place(relx=1.0, rely=1.012, anchor="se", x=-10, y=-10)

        datetime_label = tk.Label(status_frame, font=("Arial", 12))
        datetime_label.pack(side="left", padx=10, pady=5)

        battery_label = tk.Label(status_frame, font=("Arial", 12))
        battery_label.pack(side="left", padx=10, pady=5)

        wifi_label = tk.Label(status_frame, font=("Arial", 12))#, fg="white", bg="black")
        wifi_label.pack(side="left", padx=10, pady=5)

        frame_orta = tk.Frame(window2, bg="#808080")
        frame_orta.place(relx=0.0001, rely= 0.951, relwidth=7, relheight=0.009)

        def update_date_time():
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            datetime_label.config(text=f"Tarih: {current_date}   Saat: {current_time}")
            datetime_label.after(1000, update_date_time)

        def update_battery():
            battery_percent = psutil.sensors_battery()
            battery_label.config(text=f"Pil Gücü: {battery_percent}%")
            battery_label.after(60000, update_battery)

        

        update_date_time()
        update_battery()

        #uygulamalar...
        first_index = tk.Frame(window2, relief="sunken")
        first_index.place(relx=0.087, rely=0.03, anchor="center")
        second_index = tk.Frame(window2, relief="sunken")
        second_index.place(relx=0.07, rely=0.08, anchor="center")

        button_system = tk.Button(first_index, text="System Infos", font=("Arial", 12), command=system_infos)
        button_system.pack(side="left", padx=10, pady=5)

        button_app1 = tk.Button(first_index, text="Python Console", font=("Arial", 12), command=python)
        button_app1.pack(side="left", padx=10, pady=10)

        wix_browser = tk.Button(second_index, text="Wix Browser", font=("Arial", 12), command=browser)
        wix_browser.pack(side="left", padx=10, pady=5)

        button_browser = tk.Button(second_index, text="Google", font=("Arial", 12), command=google)
        button_browser.pack(side="left", padx=10, pady=10)
        #...

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", font=("Arial", 12), command=exit_program)
        menu_bar.add_cascade(label="WixOS", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Yeni Dosya")
        help_menu.add_command(label="Dosya Aç")
        menu_bar.add_cascade(label="Dosya", menu=help_menu)

        app_menu = tk.Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Sistem Özellikleri", command=system_infos)
        app_menu.add_command(label="Python Console", command=python)
        app_menu.add_command(label="Wix Browser", command=browser)
        app_menu.add_command(label="Google", command=google)
        menu_bar.add_cascade(label="Uygulamalar", menu=app_menu)

        help_menu1 = tk.Menu(menu_bar, tearoff=0)
        help_menu1.add_command(label="Hakkında")
        menu_bar.add_cascade(label="Yardım", menu=help_menu1)

        window2.config(menu=menu_bar)

        window2["highlightbackground"] = "black"
        window2["highlightcolor"] = "black"

        window2.iconbitmap("cizgifikrim.icon")

        #window2.wm_attributes("-topmost", True)

        exit_button = tk.Button(window2, text="Çıkış", command=exit_program)
        exit_button.pack(side="left", padx=10, anchor="s")

        window2.mainloop()

    window = tk.Tk()
    window.title("Kullanıcı Girişi")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window.geometry(f"{screen_width}x{screen_height}")
    # Ana frame
    main_frame = tk.Frame(window)
    main_frame.pack(expand=True)

    # Kullanıcı girişi bölümü
    login_frame = tk.Frame(main_frame)
    login_frame.pack(side=tk.LEFT, padx=(screen_width//4, 0))

    label_username = tk.Label(login_frame, text="Kullanıcı Adı:")
    label_username.pack()
    entry_username = tk.Entry(login_frame)
    entry_username.pack()

    label_password = tk.Label(login_frame, text="Parola:")
    label_password.pack()
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.pack()

    login_button = tk.Button(login_frame, text="Giriş Yap", command=login)
    login_button.pack(pady=20)

    # Fotoğraf bölümü
    image_frame = tk.Frame(main_frame)
    image_frame.pack(side=tk.RIGHT, padx=(0, screen_width//4))

    window.mainloop()
main()
