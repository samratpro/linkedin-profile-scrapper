from customtkinter import *
import sqlite3
import threading
import webbrowser
from component import scrapper_loop
import asyncio

api_key_db = 'api_key_xxxxxxxxxxxxxxx'
profile_id_db = 'profile_id_xxxxxxxxxxxxxxx'
url_db = 'https://www.linkedin.com/sales/search/people?query='
start_page_db = '1'
end_page_db = '100'
Output_Folder_db = 'Output'



con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Postdata (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key CHAR(200),
                profile_id CHAR(200),
                url CHAR(500),
                start_page CHAR(10),
                end_page CHAR(10),
                Output_Folder CHAR(10)
            )   
            ''')

data_check = cur.execute('''SELECT api_key FROM Postdata WHERE ID=1''').fetchone()
print(data_check)

if data_check == None:
    cur.execute(f'''
                    INSERT INTO Postdata(
                        api_key,
                        profile_id,
                        url,
                        start_page,
                        end_page,
                        Output_Folder
                        )
                    VALUES(
                        '{api_key_db}',                          
                        '{profile_id_db}', 
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
window.geometry("600x600")
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
info_frame = CTkFrame(content_frame)
info_frame.grid(pady=10, padx=20)

# label section
api_key_labe = CTkLabel(info_frame, text="API Key")
api_key_labe.grid(row=0, column=0, padx=10, pady=3)
api_key = CTkEntry(info_frame, width=300, border_width=1)
api_key.insert(0,str(cur.execute('''SELECT api_key FROM Postdata WHERE ID=1''').fetchone()[0]))
api_key.grid(row=1, column=0, padx=10, pady=10)

profile_id_labe = CTkLabel(info_frame, text="Profile ID")
profile_id_labe.grid(row=0, column=1, padx=10, pady=3)
profile_id = CTkEntry(info_frame, width=220, border_width=1)
profile_id.insert(0, str(cur.execute('''SELECT profile_id FROM Postdata WHERE ID=1''').fetchone()[0]))
profile_id.grid(row=1, column=1, padx=10, pady=10)

# URL Frame
url_frame = CTkFrame(content_frame)
url_frame.grid(pady=10, padx=20)

url_input_labe = CTkLabel(url_frame, text="URL Input")
url_input_labe.grid(row=2, column=0, padx=10, pady=3)
url_input = CTkTextbox(url_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=550, height=80)
url_input.insert('1.0',str(cur.execute('''SELECT url FROM Postdata WHERE ID=1''').fetchone()[0]))
url_input.grid(row=3, column=0, padx=5, pady=(5, 10))

# Page
page_frame = CTkFrame(content_frame)
page_frame.grid(pady=10, padx=20)
start_page_labe = CTkLabel(page_frame, text="Start Page ")
start_page_labe.grid(row=4, column=0, padx=10, pady=3)
start_page = CTkEntry(page_frame, width=160, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
start_page.insert(0, str(cur.execute('''SELECT start_page FROM Postdata WHERE ID=1''').fetchone()[0]))
start_page.grid(row=5, column=0, padx=10, pady=10)

end_page_labe = CTkLabel(page_frame, text="End Page ")
end_page_labe.grid(row=4, column=1, padx=10, pady=3)
end_page = CTkEntry(page_frame, width=160, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
end_page.insert(0, str(cur.execute('''SELECT end_page FROM Postdata WHERE ID=1''').fetchone()[0]))
end_page.grid(row=5, column=1, padx=10, pady=10)

Output_Folder_labe = CTkLabel(page_frame, text="Output Folder")
Output_Folder_labe.grid(row=4, column=2, padx=10, pady=3)
Output_Folder = CTkEntry(page_frame, width=175, border_width=1, fg_color=('black', 'white'), text_color=('white', 'black'))
Output_Folder.insert(0, str(cur.execute('''SELECT Output_Folder FROM Postdata WHERE ID=1''').fetchone()[0]))
Output_Folder.grid(row=5, column=2, padx=10, pady=10)


# Command
command_label = CTkFrame(content_frame)
command_label.grid(row=14, column=0, padx=10, pady=(30, 30))
start = CTkButton(command_label, text=" ▶ Run", fg_color=('#2AA26F'), command=lambda: operation_start())
start.grid(row=15, column=0, padx=12, pady=10, ipadx=10)
Update = CTkButton(command_label, text='✔ Save Data', fg_color=("#2AA26F"), command=lambda: db_save())
Update.grid(row=15, column=1, padx=12, pady=10, ipadx=10)
Reset = CTkButton(command_label, text='↻ Reset Data', fg_color=("#EB4C42"), command=lambda: reset_data())
Reset.grid(row=15, column=2, padx=12, pady=10, ipadx=10)


# Log
log_label = CTkLabel(content_frame, text="Logs", font=('', 20), fg_color=("red"))
log_label.grid(row=16, column=0, pady=0, ipadx=20)
log = CTkTextbox(content_frame, fg_color=('black', 'white'), text_color=('white', 'black'), width=550, height=200)
log.grid(row=17, column=0, padx=5, pady=(5, 10))
copyright = CTkLabel(content_frame, text="Need any help ?")
copyright.grid(row=18, column=0, padx=5, pady=(5, 0))
copy_button = CTkButton(content_frame, text="Contact With Developer", fg_color=('#2374E1'),command=lambda: webbrowser.open_new('https://www.facebook.com/samratprodev/'))
copy_button.grid(row=19, column=0, padx=5, pady=(5, 300))


def db_save():
    get_api_key = str(api_key.get())
    get_profile_id = str(profile_id.get())
    get_url = str(url_input.get('1.0',END))
    get_start_page = str(start_page.get())
    get_end_page = str(end_page.get())
    get_Output_Folder = str(Output_Folder.get())


    cur.execute('''
        UPDATE Postdata
        SET
            api_key = ?,
            profile_id = ?,
            url = ?,
            start_page = ?,
            end_page = ?,
            Output_Folder = ?
            
        WHERE ID = 1
    ''', (
        get_api_key,
        get_profile_id,
        get_url,
        get_start_page,
        get_end_page,
        get_Output_Folder
    ))


def reset_data():
    # Clear and update fields data
    api_key.delete(0,END)
    api_key.insert(0,api_key_db)

    profile_id.delete(0,END)
    profile_id.insert(0,profile_id_db)

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
                        api_key = '{api_key_db}',
                        profile_id = '{profile_id_db}',
                        url = '{url_db}',
                        start_page = '{start_page_db}',  
                        end_page = '{end_page_db}',
                        Output_Folder = '{Output_Folder_db}'
                          
                    WHERE ID = 1

                    ''')
    # window.destroy()


def operation_start():
    thread = threading.Thread(target=operation_start_thread)
    thread.start()


def operation_start_thread():
    get_api_key = api_key.get()
    get_profile_id = profile_id.get()
    get_url = url_input.get('1.0',END)
    get_start_page = start_page.get()
    get_end_page = end_page.get()
    get_Output_Folder = Output_Folder.get()
    scrapper_loop(get_api_key, get_profile_id,get_url, get_start_page, get_end_page, get_Output_Folder, log)
def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    window.mainloop()

con.commit()
cur.close()