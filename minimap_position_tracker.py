from riotwatcher import RiotWatcher, ApiError
import cv2
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


watcher = RiotWatcher('RGAPI-a2563a60-31e5-4189-b78c-1ea7d035bdbe')

# ---------- DINAMIC DATA ---------- 
matchId = 4545560961
side = 100
file_name = "kills_PSH_vs_QLS_Blue.jpg"
# -----

game = watcher.match.by_id('euw1',matchId)
timeline = watcher.match.timeline_by_match('euw1',matchId)


participants = []
kills = []
position = []

print(game.keys())
for participant in game['participants']:
    if participant['teamId'] == side:
        #print(participant['participantId'])
        participants.append(participant['participantId'])
    

for x in timeline['frames']:
    # print(x.keys())
    for events in x['events']:
        if events['type'] == "CHAMPION_KILL":
            for y in participants:
                if events['killerId'] == y:
                    kills.append(events['killerId'])
                    position.append(events['position'])
            
            
print(kills)


# --- OpenCV ---
img = cv2.imread('imagenes/map11.png')

# creates the overlay
overlay = img.copy()

# configures the overlay size and color
cv2.rectangle(overlay,(0,0),(512,512),(0,0,0),-1)

# lower the opacity of the overlay
final_img = cv2.addWeighted(img,0.4,overlay,0.6,0,overlay)

for x in position:
    # reescales the coordinates
    new_x = int(x['x']*(512/14990))
    new_y = int(512-(x['y']*(512/15100)))
    # draws the markers
    cv2.drawMarker(final_img,(new_x,new_y),(0,255,0),cv2.MARKER_DIAMOND,20,5,8)

# shows the image
cv2.imshow("compuesta",final_img)
cv2.waitKey(0)

# saves the image in a new file

cv2.imwrite(file_name,final_img)

# ---


