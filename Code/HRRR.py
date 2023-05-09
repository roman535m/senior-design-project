from GUI import GUI
from tkinter import *
from PIL import Image, ImageTk
import cv2
from Video import Video
from HR_RR_Calculator import HR_RR_Calculator
from matplotlib.figure import Figure

def main():
    v = Video()
    process = HR_RR_Calculator()
    plot_clear = 125

    window = Tk()
    gui = GUI(window)
    window.protocol("WM_DELETE_WINDOW", window.destroy)
    gui.center_window()
    gui.set_title('Heart Rate Through Video Measurement System')
    gui.set_background('#DEDDDD')

    face_label_frame = gui.create_label_frame(parent=window, label_text='Captured Frame')
    gui.set_object_grid_parameter(object=face_label_frame, grid_row=0, grid_column=0)

    label = gui.create_label(parent=face_label_frame, width=700, height=500)
    label.pack(padx=10, pady=10)

    buttons_label_frame = gui.create_label_frame(parent=window, label_text='Operation Buttons')
    gui.set_object_grid_parameter(object=buttons_label_frame, grid_row=5, grid_column=0, column_span=11)

    hr_label_frame = gui.create_label_frame(parent=window, label_text='Heart Rate Graph')
    gui.set_object_grid_parameter(object=hr_label_frame, grid_row=0, grid_column=1, row_span=1, column_span=10)

    results_hr_frame = gui.create_label_frame(parent=window, label_text='Heart Rate')
    gui.set_object_grid_parameter(object=results_hr_frame, grid_row=1, grid_column=0, column_span=1, row_span=4)

    hr_label = gui.create_text_label(parent=results_hr_frame, width=18, height=1)
    hr_label.pack(padx=10, pady=10)

    results_rr_frame = gui.create_label_frame(parent=window, label_text='Respiration Rate')
    gui.set_object_grid_parameter(object=results_rr_frame, grid_row=1, grid_column=1, column_span=10, row_span=4)

    rr_label = gui.create_text_label(parent=results_rr_frame, width=18, height=1)
    rr_label.pack(padx=10, pady=10)

    """
    results_fps_frame = gui.create_label_frame(parent=window, label_text='Frames Per Second')
    gui.set_object_grid_parameter(object=results_fps_frame, grid_row=1, grid_column=7, column_span=3)

    fps_label = gui.create_text_label(parent=results_fps_frame, width=18, height=1)
    fps_label.pack(padx=10, pady=10)
    """

    gui.set_figure(figure=Figure(figsize=(9, 6), dpi=100))
    gui.set_plot(plot=gui.figure.add_subplot())
    gui.set_canvas(canvas=gui.create_figure_canvas(gui.figure, parent=hr_label_frame))
    gui.canvas.draw()
    gui.canvas.get_tk_widget().pack()

    def clear_plot():
        gui.plot.remove()
        gui.set_plot(plot=gui.figure.add_subplot())

    def update_hr_label():
        hr_label.configure(text=round(process.bpm), font=('Helvetica bold', 50))
        hr_label.after(100, update_hr_label)

    def update_rr_label():
        rr_label.configure(text=round(process.rrpm), font=('Helvetica bold', 5m 0))
        rr_label.after(100, update_rr_label)

    def update_fps_label():
        fps_label.configure(text=round(process.fps))
        fps_label.after(100, update_fps_label)

    def plot_results():
        if len(process.hr_list) <= plot_clear:
            gui.canvas.draw()
            gui.plot.plot(process.hr_list[-plot_clear:])
            gui.toolbar.update()
        else:
            process.hr_list.clear()
            clear_plot()
            plot_results()

    def video_stop():
        v.status = False
        v.stop()
        gui.set_blank_image()

    def video_capture():
        if v.status:
            frame = v.get_frame()
            try:
                process.run(frame)
                cv2image = cv2.cvtColor(process.frame_out, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)
                plot_results()
            except Exception:
                pass
            label.after(10, video_capture)

    def video_start():
        v.status = True
        update_hr_label()
        update_rr_label()
        #update_fps_label()
        clear_plot()
        process.reset()
        gui.remove_blank_image()
        v.start()
        video_capture()

    start_btn = gui.create_button(parent=buttons_label_frame, label_text='Start', button_width=60, function=video_start)
    start_btn['font'] = gui.create_font()
    gui.set_object_grid_parameter(object=start_btn, grid_row=0, grid_column=0)

    end_btn = gui.create_button(parent=buttons_label_frame, label_text='End', button_width=56, function=video_stop)
    end_btn['font'] = gui.create_font()
    gui.set_object_grid_parameter(object=end_btn, grid_row=0, grid_column=6)

    window.mainloop()


if __name__ == '__main__':
    main()
