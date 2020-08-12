from tkinter import *
from pydub import AudioSegment
from pydub.playback import play
import os

# base states
counter_timer = 1500
counter_break = 300
rdy = 0
paused = 0
stopped = 0
alreadyplayed = 0


def update_break():
    global counter_break
    global counter_timer
    global stopped
    global paused

    if paused == 0:
        if stopped == 0:
            if counter_break >= 0:
                minutes = counter_break // 60
                if minutes < 10:
                    minutes = "0" + str(minutes)
                seconds = counter_break % 60
                if seconds < 10:
                    seconds = "0" + str(seconds)
                output = str(minutes) + ":" + str(seconds)

                break_count.configure(text=output, padx=5, pady=5)
                break_count.after(1000, update_break)
                counter_break -= 1
            else:
                play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'endbrake.mp3')) - 20)
                counter_timer = 1500
                counter_break = 300
                timer_count.configure(text='25:00')
                break_count.configure(text='5:00')
                stop.grid_forget()
                pause.grid_forget()
                start.grid(column=0, row=5)

        else:
            counter_timer = 1500
            counter_break = 300
            timer_count.configure(text='25:00')
            break_count.configure(text='5:00')
    else:
        pass


def update_timer():
    global counter_timer
    global counter_break
    global stopped
    global paused
    global alreadyplayed
    global rdy

    if paused == 0:
        if stopped == 0:
            if counter_timer >= 0:
                minutes = counter_timer // 60
                if minutes < 10:
                    minutes = "0" + str(minutes)
                seconds = counter_timer % 60
                if seconds < 10:
                    seconds = "0" + str(seconds)
                output2 = str(minutes) + ":" + str(seconds)

                timer_count.configure(text=output2)
                timer_count.after(1000, update_timer)
                counter_timer -= 1
            else:
                if alreadyplayed == 0:
                    play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'victory.mp3')) - 20)
                    alreadyplayed = 1
                    rdy += 1
                    rdy_count.configure(text=rdy)
                update_break()
        else:
            counter_timer = 1500
            counter_break = 300
            timer_count.configure(text='25:00')
            break_count.configure(text='5:00')
    else:
        pass


def click_start():
    global stopped
    global alreadyplayed

    stopped = 0
    alreadyplayed = 0

    pause.grid(column=1, row=5)
    stop.grid(column=2, row=5)
    start.grid_forget()
    update_timer()
    play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'start.mp3')) - 20)


def click_pause():
    global paused

    if paused == 0:
        pause.configure(text='Resume')
        paused = 1
        update_timer()
        play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'pause.mp3')) - 20)
    else:
        pause.configure(text='Pause')
        paused = 0
        update_timer()
        play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'resume.mp3')))


def click_stop():
    global stopped
    global paused
    global counter_break
    global counter_timer

    counter_timer = 1500
    counter_break = 300
    timer_count.configure(text='25:00')
    break_count.configure(text='5:00')
    stopped = 1
    pause.configure(text='Pause')
    paused = 0
    stop.grid_forget()
    pause.grid_forget()
    start.grid(column=0, row=5)
    play(AudioSegment.from_file(os.path.join(os.path.dirname(__file__), 'sounds', 'stop.mp3')) - 20)


# window properties
window = Tk()
window.title("Timer")
window.geometry('390x150')

# main timer
timer_text = Label(window, text="timer", font=("Times", "20", "bold"))
timer_text.grid(column=0, row=0, padx=10, pady=10)
timer_count = Label(window, text="25:00", font=("Times", "20", "bold"))
timer_count.grid(column=1, row=0, padx=10, pady=10)

# break timer
break_text = Label(window, text="break", font=("Times", "20", "bold"))
break_text.grid(column=0, row=1, padx=10, pady=10)
break_count = Label(window, text="5:00", font=("Times", "20", "bold"))
break_count.grid(column=1, row=1, padx=10, pady=10)

# count of ready
rdy_text = Label(window, text='Num of Ready', font=("Times", "20", "bold"))
rdy_text.grid(column=2, row=0)
rdy_count = Label(window, text='0', background='orange', font=("Times", "20", "bold"))
rdy_count.grid(column=2, row=1)

start = Button(window, text="Start", command=click_start, background='orange', font=("Times", "20", "bold"))
pause = Button(window, text="Pause", command=click_pause, font=("Times", "20", "bold"))
stop = Button(window, text="Stop", command=click_stop, font=("Times", "20", "bold"))
start.grid(column=0, row=5)

window.mainloop()
