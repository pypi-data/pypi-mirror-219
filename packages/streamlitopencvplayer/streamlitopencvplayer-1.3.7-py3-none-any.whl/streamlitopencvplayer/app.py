import json
import time
import urllib.request

import cv2
import streamlit as st

# Function to display video in the Streamlit app


def display_video(video_path, json_file):
    # Open the video file
    # Check if video_url variables exists in session state
    if "name_vid_old" not in st.session_state and "name_vid_sel" not in st.session_state :
        if "capture" not in st.session_state:
            st.session_state['capture'] = cv2.VideoCapture(video_path)
            # or st.session_state['name_vid_old'] != st.session_state['name_vid_sel']
    else :
        if st.session_state['name_vid_old'] != st.session_state['name_vid_sel'] :
            st.session_state['capture'] = cv2.VideoCapture(video_path)
            st.session_state['name_vid_old'] = st.session_state['name_vid_sel']

    if "fps" not in st.session_state:
        st.session_state['fps'] = st.session_state['capture'].get(
            cv2.CAP_PROP_FPS)
    if not st.session_state["capture"].isOpened():
        st.write("No much video to open")
        exit()
    if "resume" not in st.session_state:
        st.session_state["resume"] = False
    if "frame" not in st.session_state:
        ret, frame = st.session_state["capture"].read()
        st.session_state["frame"] = frame

    # Opening JSON file and returns JSON object as a dictionnary
    if json_file is not None:
        response = urllib.request.urlopen(json_file)
        fileReader = json.loads(response.read())
        list_ts = []
        list_data = []

        for alert in fileReader["alerts"]:
            list_ts.append(alert["timestamp"])
            list_data.append(alert["data"])

        st.session_state['alerts_list'] = list_ts
        alerts = []
        data = []

        for x in range(len(list_ts)):
            time_alert = float(list_ts[x])-float(
                st.session_state['name_vid_sel'].partition('_')[0])
            alerts.append(int((time_alert)*st.session_state['fps']))
            data.append(list_data[x])
    # checkbox to enable detections
    draw_detections = st.checkbox("Draw detections", value=True)
    column1, column2, column3 = st.columns([1, 2, 1])
    with column1:
        # zone to display images
        stframe = st.empty()
    with column3:
        # Create buttons for alerts
        st.subheader('Alerts :')
        num_buttons = len(alerts)

        button_values = {f'{i}': 0 for i in range(num_buttons)}

        for button_label, button_value in button_values.items():
            if st.button(str('Alert ')+button_label):
                button_values = {label: 1 if label ==
                                 button_label else 0 for label in button_values}

        for button_label, button_value in button_values.items():
            if button_value == 1:
                st.session_state["capture"].set(
                    cv2.CAP_PROP_POS_FRAMES, alerts[int(button_label)])
                st.session_state["resume"] = True

    # Buttons and zone of display
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="small")
    with col1:
        container_2 = st.empty()
        pause = container_2.button('⏸')
    with col2:
        plus = st.button("➕")
    with col4:
        replay = st.button("↻")
    with col3:
        minus = st.button("➖")
    with col5:
        st.write('')

    if replay:
        st.session_state["capture"].set(cv2.CAP_PROP_POS_FRAMES, 0)
        st.session_state["resume"] = False

    while st.session_state["resume"] is False:
        for x in range(int(st.session_state['fps'])):
            ret, frame = st.session_state["capture"].read()
            st.session_state["frame"] = frame
            for i in range(len(data)):
                if draw_detections:
                    if int(st.session_state["capture"].get(cv2.CAP_PROP_POS_FRAMES)) == int(alerts[i]):
                        # draw all detections on the frame
                        for j in range(len(data[i])):
                            output = cv2.rectangle(st.session_state["frame"], (data[i][j][0][0], data[i][j][0][1]), (
                                data[i][j][0][2], data[i][j][0][3]), color=(128, 0, 0), thickness=2)
                            output = cv2.putText(
                                st.session_state["frame"], data[i][j][3], (data[i][j][0][0], data[i][j][0][1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                        # update image zone with detections
                        stframe.image(output, caption='', width=500)
                        time.sleep(0.05)
            stframe.image(
                st.session_state["frame"], caption='', width=500)
            time.sleep(0.05)

            if pause:
                st.session_state["resume"] = True
                break
            if plus:
                st.session_state["capture"].set(cv2.CAP_PROP_POS_FRAMES, int(
                    st.session_state["capture"].get(cv2.CAP_PROP_POS_FRAMES))-1)
                st.session_state["resume"] = True
                break
            if minus:
                st.session_state["capture"].set(cv2.CAP_PROP_POS_FRAMES, int(
                    st.session_state["capture"].get(cv2.CAP_PROP_POS_FRAMES))-3)
                st.session_state["resume"] = True
                break

            # back to the first frame if the video is finished
            if int(st.session_state["capture"].get(cv2.CAP_PROP_POS_FRAMES)) == int(st.session_state['capture'].get(cv2.CAP_PROP_FRAME_COUNT)):
                st.session_state["capture"].set(cv2.CAP_PROP_POS_FRAMES, 0)
                st.session_state["resume"] = True
                break

    if st.session_state["resume"]:
        container_2.empty()
        pause = container_2.button('▶')
        st.session_state["resume"] = False


def main():

    video_path = "https://cvlogger.blob.core.windows.net/json-concat-files/1689004947.7068138_1689004953.7068138.webm?sv=2021-10-04&st=2023-07-11T15%3A21%3A27Z&se=2023-07-26T15%3A21%3A00Z&sr=b&sp=r&sig=u6uuOUo9wvn5KJFNUnUR3axYtC815SUQBuDqNIC4L%2Bw%3D"
    down_json = "https://cvlogger.blob.core.windows.net/json-concat-files/1689004947.7068138_1689004953.7068138_global.json?sv=2021-10-04&st=2023-07-11T15%3A22%3A03Z&se=2023-07-26T15%3A22%3A00Z&sr=b&sp=r&sig=qSHWvDUIOOT%2F%2Bff270JVX7ucSRn5Lylgw5%2Fh9iTa4BY%3D"
    if video_path is not None:
        display_video(video_path, down_json)


if __name__ == "__main__":
    main()
