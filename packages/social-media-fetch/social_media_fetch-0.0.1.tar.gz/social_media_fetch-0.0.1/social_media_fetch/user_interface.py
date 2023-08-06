import tkinter as tk_gui

import front_end.Data_access_layer
from front_end.Data_access_layer import cls_function_logic



class cls_gui_frame:

    def fn_gui():
        # Canvas
        canvas_gui = tk_gui.Tk()
        canvas_gui.geometry('700x700')
        canvas_gui.title('Sentiment Analysis')

        # Labels
        lbl_title = tk_gui.Label(canvas_gui, text='Sentiment Analysis')
        lbl_title.place(x=300, y=50)



        # # STEP 1 : Data collection
        lbl_title = tk_gui.Label(canvas_gui, text='Step 1:')
        lbl_title.place(x=170, y=100)

        # Button
        btn_data_collection = tk_gui.Button(canvas_gui, text='Data collection', command=cls_function_logic.fn_data_ftch)
        btn_data_collection.place(x=300, y=98)
        btn_data_collection.configure(height=1, width=25)



        canvas_gui.mainloop()




















