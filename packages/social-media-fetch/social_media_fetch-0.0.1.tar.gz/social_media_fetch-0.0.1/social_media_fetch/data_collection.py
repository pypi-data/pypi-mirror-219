import mastodon.utility
from mastodon.utility import *
from mastodon import Mastodon
import tkinter as gui_dc
from tkinter import messagebox,Scrollbar
import csv
import os


class cls_data_collection:

    global mastodon


    # Mastodon Authentication
    clnt_id = 'RO9_LFCNfSEG0vLXtmOkyACer96bRWndA6Cd8LFEu0k'
    clnt_scrt = 'o59V2Kod3Q49mL7c0L10_InsAyEVbszPesXPx-mHcM8'
    acs_tkn = 'r9UZM6ccbqbMccT6uPY6O_981PRcZSamUMosSlcPxwE'
    url_lnk = 'https://mastodon.social'


    mastodon = Mastodon(
        client_id=clnt_id,
        client_secret=clnt_scrt,
        access_token=acs_tkn,
        api_base_url=url_lnk,
        version_check_mode='none'
    )


    # fetch data
    def fn_ftch_data():

        timln_data = Mastodon.timeline_public(self=mastodon,limit=100)
        #fchd_data =[]
        if timln_data != None:
            """post_datetime = pst_data["created_at"]
            post_id = pst_data["id"]
            post_text = pst_data["content"]
            user_name = pst_data["account"]["display_name"]

            post_info = f"Datetime: {post_datetime}\nPost ID: {post_id}\nContent: {post_text}\nUser: {user_name}\n"
            """
            return timln_data
        else:
            messagebox.showinfo('Data Collection', 'Error while fetching data')


    # display data
    def fn_dsply_data(lst_bx_posts_data):

        post_dsplay = cls_data_collection.fn_ftch_data()
        for pst_data in post_dsplay:

            if pst_data["media_attachments"]:
                continue
                


            post_datetime = pst_data["created_at"]
            post_id = pst_data["id"]
            post_text = pst_data["content"]
            user_name = pst_data["account"]["display_name"]
            
            post_info = f"Datetime: {post_datetime}\nPost ID: {post_id}\nContent: {post_text}\nUser: {user_name}\n"

            lst_bx_posts_data.insert(gui_dc.END, post_info + "\n\n\n"+'_____________________'+"\n\n\n")




    # create new folder to store csv file
    def crt_fldr(fldr_name):
        prjct_path = os.getcwd()
        new_fldr_path = os.path.join(prjct_path,fldr_name)

        #print('step 1')

        fetched_data = cls_data_collection.fn_ftch_data()

        if not os.path.exists(new_fldr_path):
            os.mkdir(new_fldr_path)

            #print('step 2')

            # save data to csv

            fldr_path = os.path.join(os.getcwd(), fldr_name)
            file_path = os.path.join(fldr_path, 'md_dataset.csv')

            with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
                wrte_data = csv.writer(csv_file)
                wrte_data.writerow(['Date Time', 'Post Id', 'Post Text', 'User Name'])
                print('saving headers to csv file')
                for csv_data in fetched_data:
                    #wrte_data.writerows(csv_data)
                    wrte_data.writerow([csv_data['created_at'],csv_data['id'],csv_data['content'],csv_data["account"]["display_name"]])

                    #print(csv_data)
                messagebox.showinfo('Data Collection','Data set genrated successfully! Please check below path of your system'+'\n'+new_fldr_path)
        else:

            fldr_path = os.path.join(os.getcwd(), fldr_name)
            file_path = os.path.join(fldr_path, 'md_dataset.csv')

            with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
                wrte_data = csv.writer(csv_file)
                #wrte_data.writerow(['Date Time', 'Post Id', 'Post Text', 'User Name'])
                #print('saving headers to csv file')
                for csv_data in fetched_data:
                    #wrte_data.writerows(csv_data)
                    wrte_data.writerow([csv_data['created_at'],csv_data['id'],csv_data['content'],csv_data["account"]["display_name"]])

                    #print(csv_data)
                messagebox.showinfo('Data Collection','Data set genrated successfully! Please check below path of your system'+'\n'+new_fldr_path)




    def fn_gui_data_collection():

        # Canvas
        canvas_gui_dc = gui_dc.Tk()
        canvas_gui_dc.geometry('700x700')
        canvas_gui_dc.title('Step 1: Data Collection')

        #Labels
        lbl_title = gui_dc.Label(canvas_gui_dc, text='Data Collection')
        lbl_title.place(x=300, y=50)

        lst_bx_posts_data = gui_dc.Text(canvas_gui_dc)
        lst_bx_posts_data.place(x=100, y=180)
        lst_bx_posts_data.configure(height=10, width=50)


        # Buttons
        btn_ftch = gui_dc.Button(canvas_gui_dc, text='Fetch and Display Data',command=lambda: cls_data_collection.fn_dsply_data(lst_bx_posts_data))
        btn_ftch.place(x=90, y=120)
        btn_ftch.configure(height=1, width=25)


        btn_gnrte_ds = gui_dc.Button(canvas_gui_dc,text='Genrate Data Set',command=lambda:cls_data_collection.crt_fldr('Mastodon dataset'))
        btn_gnrte_ds.place(x=310,y=120)
        btn_gnrte_ds.configure(height=1,width=20)


        canvas_gui_dc.mainloop()



if __name__ == '__cls_data_collection__':

    #fldr_name = 'Mastodon dataset'
    cls_data_collection()






