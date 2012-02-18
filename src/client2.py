import swapi
import time
from math import sqrt
import mathlib

server = swapi.swconn("192.168.178.43", 1337, swapi.PLAYERTYPE_PLAYER, "joe")
server.connect()

field_size = 1000

target_id = None
target_pos = None

def distance(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def get_closest(playerlist):
    target = None    
    mindist = 99999.0

    pos = None
    
    mypos = server.get_pos()
    for plr in playerlist:
        dist = distance(mypos, (plr[1], plr[2]))
        if dist < mindist:
            target = plr[0]
            offset = (0.0, 0.0)
            if plr[9]:
                offset = mathlib.rot(plr[5] / 5.0, 0.0, plr[3]) 
            pos = (plr[1] + offset[0], plr[2] + offset[1])
            mindist = dist
    
    return target, pos, mindist        

def get_target_pos(playerlist):
    for plr in playerlist:
        if target_id == plr[0]:
            return (plr[1], plr[2])

def multiply_players(playerlist):
    new_list = []
    for p in playerlist:
        new_list.append(p)
        new_list.append((p[0] + 100000000,p[1]+field_size,p[2],           p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 200000000,p[1]-field_size,p[2],           p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 300000000,p[1],           p[2]+field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 400000000,p[1],           p[2]-field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 100000000,p[1]+field_size,p[2]+field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 200000000,p[1]-field_size,p[2]+field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 300000000,p[1]+field_size,p[2]-field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
        new_list.append((p[0] + 400000000,p[1]-field_size,p[2]-field_size,p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10]))
    return new_list

old_target = None
while True:    
    time.sleep(0.01)
    
    playerlist = multiply_players(server.get_players())
    
    mypos = server.get_pos()
    target_id, pos, dist = get_closest(playerlist)
    if old_target != target_id:
        #print target_id, mypos, pos, dist
        old_pos = pos
    if target_id == None:
        server.do(True, 0, True, 0)
    else:
        if pos != None and mypos != None:
            dist = distance(pos, mypos) 
                    
            thrust = False
            fire = False
            turn_left = False
            turn_right = False
            
            if dist > 75:
                thrust = True
                
            dirvec = mathlib.rot(1.0, 0.0, server.get_dir())
            adiff = mathlib.anglediff(mypos[0], mypos[1], pos[0], pos[1], dirvec[0], dirvec[1])
            if abs(adiff) > 0.1:
                if adiff < 0:
                    turn_right = True
                else:
                    turn_left = True
                    
            if server.get_has_shot() and dist < 500 and abs(adiff) < 0.2 - ((0.15 / 400) * dist):
                fire = True
            
            server.do(turn_left, turn_right, thrust, fire)
        
        