from customtkinter import *
import sqlite3
import threading
import webbrowser
from component import scrapper_loop, cookie_save


url_db = 'https://www.linkedin.com/sales/search/people?query='
start_page_db = '1'
end_page_db = '100'
Output_Folder_db = 'Output'

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                url CHAR(500),
                start_page CHAR(10),
                end_page CHAR(10),
                Output_Folder CHAR(10)
            )   
            ''')
data_check = cur.execute('''SELECT url FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check == None:
    cur.execute(f'''
                    INSERT INTO Postdata(
                        url,
                        start_page,
                        end_page,
                        Output_Folder
                        )
                    VALUES(
                        '{url_db}',
                        '{start_page_db}',
                        '{end_page_db}',
                        '{Output_Folder_db}' 
                                               
                    )
                    ''')
# TK part
window = CTk()
set_default_color_theme("green")
set_appearance_mode("light")
window.title("Linkedin Scrapper")
window.geometry("620x600")
window.wm_iconbitmap()

# Create a Frame + Content Frame with scrollbar
frame = CTkFrame(window)
frame.pack(fill=BOTH, expand=True)
canvas = CTkCanvas(frame)
canvas.pack(side=LEFT, fill=BOTH, expand=True)
canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event))  # Labda have to use when function is below
scrollbar = CTkScrollbar(frame, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
content_frame = CTkFrame(canvas)
canvas.create_window((0, 0), window=content_frame, anchor=NW)


# website info widgets
cookie_frame = CTkFrame(content_frame, fg_color=('#DBDBDB'))
cookie_frame.grid(pady=10, padx=20)
# label section
open = CTkButton(cookie_frame, text="Open Browser", width=150, fg_color=('#006262'),corner_radius=20, command=lambda: browser_open())
open.grid(row=1, column=0, padx=10, pady=10)

close = CTkButton(cookie_frame, text="Close Browser", width=150, fg_color=('#006262'), corner_radius=20,command=lambda: browser_close())
close.grid(row=1, column=1, padx=10, pady=10)

login_status = CTkLabel(cookie_frame,width=200, text="Login Status : False",corner_radius=20, fg_color=('#9457EB'), text_color=('#E1E8FF'))
login_status.grid(row=1, column=2, padx=10, pady=10)
if os.path.exists('storage_state.json'):
        if os.path.getsize('storage_state.json') > 0:
            login_status.configure(text='Login Status : True')

# URL Frame
url_frame = CTkFrame(content_frame, fg_color=('#DBDBDB'))
url_frame.grid(pady=10, padx=20)

url_input_labe = CTkLabel(url_frame, text="URL Input")
url_input_labe.grid(row=2, column=0, padx=10, pady=3)
url_input = CTkTextbox(url_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=550, height=80)
url_input.insert('1.0',str(cur.execute('''SELECT url FROM Postdata WHERE ID=1''').fetchone()[0]))
url_input.grid(row=3, column=0, padx=5, pady=(5, 10))

# Page
page_frame = CTkFrame(content_frame, fg_color=('#DBDBDB'))
page_frame.grid(pady=10, padx=20)
start_page_labe = CTkLabel(page_frame, text="Start Page ")
start_page_labe.grid(row=4, column=0, padx=10, pady=3)
start_page = CTkEntry(page_frame, width=110, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
start_page.insert(0, str(cur.execute('''SELECT start_page FROM Postdata WHERE ID=1''').fetchone()[0]))
start_page.grid(row=5, column=0, padx=10, pady=10)

end_page_labe = CTkLabel(page_frame, text="End Page ")
end_page_labe.grid(row=4, column=1, padx=10, pady=3)
end_page = CTkEntry(page_frame, width=123, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
end_page.insert(0, str(cur.execute('''SELECT end_page FROM Postdata WHERE ID=1''').fetchone()[0]))
end_page.grid(row=5, column=1, padx=10, pady=10)

Output_Folder_labe = CTkLabel(page_frame, text="Output Folder")
Output_Folder_labe.grid(row=4, column=2, padx=10, pady=3)
Output_Folder = CTkEntry(page_frame, width=110, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
Output_Folder.insert(0, str(cur.execute('''SELECT Output_Folder FROM Postdata WHERE ID=1''').fetchone()[0]))
Output_Folder.grid(row=5, column=2, padx=10, pady=10)

Browser_Status_labe = CTkLabel(page_frame, text="Browser Status")
Browser_Status_labe.grid(row=4, column=3, padx=10, pady=3)
Browser_Status = CTkComboBox(page_frame, width=140, values=["browser hide", "browser show"])
Browser_Status.grid(row=5, column=3, padx=10, pady=10)
Browser_Status.set("browser show")

# Command
command_label = CTkFrame(content_frame, fg_color=('#DBDBDB'))
command_label.grid(row=14, column=0, padx=5, pady=(30, 30))
start = CTkButton(command_label, text="▶️ Run", width=120, fg_color=('#006262'), corner_radius=20,command=lambda: operation_start())
start.grid(row=15, column=0, padx=5, pady=10, ipadx=5)
stop = CTkButton(command_label, text="⏹️ Stop", width=120, fg_color=('#9457EB'), corner_radius=20,command=lambda: operation_close())
stop.grid(row=15, column=1, padx=5, pady=10, ipadx=5)
Update = CTkButton(command_label, text='✔ Save Data', width=120, fg_color=("#006262"), corner_radius=20,command=lambda: db_save())
Update.grid(row=15, column=2, padx=5, pady=10, ipadx=5)
Reset = CTkButton(command_label, text='↻ Reset Data', width=120, fg_color=("#9457EB"), corner_radius=20,command=lambda: reset_data())
Reset.grid(row=15, column=3, padx=5, pady=10, ipadx=5)


# Log
log_label = CTkLabel(content_frame, text="Logs", font=('', 20), fg_color=("#9457EB"), text_color=('white', 'black'), corner_radius=20,)
log_label.grid(row=16, column=0, pady=0, ipadx=20)
log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=550, height=200)
log.grid(row=17, column=0, padx=5, pady=(5, 10))
copyright = CTkLabel(content_frame, text="Need any help ?")
copyright.grid(row=18, column=0, padx=5, pady=(5, 0))
copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'),command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
copy_button.grid(row=19, column=0, padx=5, pady=(5, 300))


def db_save():
    get_url = str(url_input.get('1.0',END))
    get_start_page = str(start_page.get())
    get_end_page = str(end_page.get())
    get_Output_Folder = str(Output_Folder.get())


    cur.execute('''
        UPDATE Postdata
        SET
            url = ?,
            start_page = ?,
            end_page = ?,
            Output_Folder = ?
            
        WHERE ID = 1
    ''', (
        get_url,
        get_start_page,
        get_end_page,
        get_Output_Folder
    ))


def reset_data():
    # Clear and update fields data
    url_input.delete('1.0',END)
    url_input.insert('1.0', url_db)

    start_page.delete(0,END)
    start_page.insert(0,start_page_db)

    end_page.delete(0,END)
    end_page.insert(0,end_page_db)

    Output_Folder.delete(0,END)
    Output_Folder.insert(0,Output_Folder_db)


    # Update database
    cur.execute(f'''
                    UPDATE Postdata
                    SET
                        url = '{url_db}',
                        start_page = '{start_page_db}',  
                        end_page = '{end_page_db}',
                        Output_Folder = '{Output_Folder_db}'
                          
                    WHERE ID = 1

                    ''')
    # window.destroy()



browser_close_event = threading.Event()
def browser_open():
    thread = threading.Thread(target=browser_open_thread)
    thread.start()

def browser_open_thread():
    # Clear the event if the browser is being opened
    browser_close_event.clear()
    cookie_save(login_status, log, close_event=browser_close_event)
def browser_close():
    # Set the event to signal the browser should close
    browser_close_event.set()

operation_close_event = threading.Event()
def operation_start():
    start.configure(text="⌛️ Running...")
    thread = threading.Thread(target=operation_start_thread)
    thread.start()
def operation_close():
    start.configure(text="▶️ Run")
    operation_close_event.set()

def operation_start_thread():
    get_url = url_input.get('1.0',END)
    get_start_page = start_page.get()
    get_end_page = end_page.get()
    get_Output_Folder = Output_Folder.get()
    browser_status = Browser_Status.get()
    print(browser_status)
    operation_close_event.clear()
    scrapper_loop(get_url, get_start_page, get_end_page, get_Output_Folder,browser_status,log,close_event=operation_close_event)
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    window.mainloop()

con.commit()
cur.close()