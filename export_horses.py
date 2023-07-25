# Script for exporting coordinates of animals relative to the background which were tracked in a video scene in Blender
# All animal tracks should have standard names (like "H1 or H001") and should be in the object "allhorses"
# All background markers should have standard names (like "bgd01")

import bpy

#SETUP START

filepath = '/Applications/Blender/output/'      #output destination
clip = bpy.data.movieclips[0]
clipname = clip.name
#clipname = "V180817_12fps_4k.mp4"
obname = "allhorses"
horse_ob = clip.tracking.objects[obname]
no_of_horses = len(horse_ob.tracks)	#max is 1000
#no_of_horses = 1
no_of_bgdpoints = len(clip.tracking.objects["Camera"].tracks)	#max is 100
init_frame = bpy.context.scene.frame_start
end_frame = bpy.context.scene.frame_end

outputx_name = filepath + 'alltracks_x.txt'
outputy_name = filepath + 'alltracks_y.txt'
outputx = open(outputx_name, 'w')
outputy = open(outputy_name, 'w')

#SETUP END


def print_one_horse (frame, frame_end, current_horse, counter):
    output_name = filepath + counter + '.txt'
    output = open(output_name, 'w')
    horse =  bpy.data.objects[str(current_horse.name)]
    track = clip.tracking.objects[obname].tracks[current_horse.name]
    while frame < frame_end+1:

        #set current frame to frame that we need
        bpy.context.scene.frame_set(frame)

        #print (horse.matrix_world*horse.location)
		#export logs
        coords = (horse.matrix_world*horse.location)[0:3]
        x = coords[0]
        y = coords[1]
        z = coords[2]

        #it exports one more frame after and before getting disabled
        markerisactive = track.markers.find_frame(frame, exact=True)
        nextmarkerisactive = track.markers.find_frame(frame+1, exact=True)
        prevmarkerisactive = track.markers.find_frame(frame-1, exact=True)
        #none of them is inactive
        isactive = markerisactive and prevmarkerisactive and nextmarkerisactive
        if isactive:
        #if bpy.data.movieclips["full180913_1_10x.mp4"].tracking.tracks[current_horse.name].is_enabled
            output.write(str(frame) + '\t' + str(x) + '\t' + str(y) + '\t' + str(z) + '\n')
            outputx.write(str(x) + '\t')
            outputy.write(str(y) + '\t')
        else:
            output.write(str(frame) + '\t' + 'NaN' + '\t' + 'NaN' + '\t' + 'NaN' + '\n')
            outputx.write('NaN' + '\t')
            outputy.write('NaN' + '\t')

        frame = frame + 1

    output.close()
    outputx.write('\n')
    outputy.write('\n')
    #print (str(current_horse.name))


def set_horse(i):

    if i > 0 and i < 10:
        horse_name = 'H' + '00' + str(i)
    elif i >= 10 and i < 100:
        horse_name = 'H' + '0' + str(i)
    elif i >= 100:
        horse_name = 'H' + str(i)
    #horse_name = 'H' + str(i)
    bpy.data.objects[horse_name].constraints["Follow Track"].depth_object = bpy.data.objects["Ground"]
    bpy.data.objects[horse_name].constraints["Follow Track"].use_undistorted_position = True
    current_horse = bpy.data.objects[horse_name]
    return current_horse


def link_bgd_empty(no_of_bgdpoints):
    bpy.context.scene.frame_set(init_frame)
    j = 1

    while j <= no_of_bgdpoints:
    	if j < 10:
    		trackname = 'BG' + '0' + str(j)
    	elif j >= 10:
    		trackname = 'BG' + str(j)
    	bpy.ops.object.empty_add(type='SPHERE', radius=0.1, view_align=False, location=(0, 0, 0), layers=(False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False))
    	bpy.ops.object.constraint_add(type='FOLLOW_TRACK')
    	bpy.context.object.constraints["Follow Track"].object = "Camera"
    	bpy.context.object.constraints["Follow Track"].camera = bpy.data.objects["Camera"]
        #bpy.context.object.constraints["Follow Track"].depth_object = bpy.data.objects["Ground"]
    	bpy.context.object.constraints["Follow Track"].use_3d_position = True
    	bpy.context.object.constraints["Follow Track"].track = trackname
        #bpy.data.objects[horse_name].constraints["Follow Track"].use_undistorted_position = True
        #empty_name = 'Empty'
        #if j > 0 and j < 10:
        #	empty_name = empty_name + '.00' + str(j)
        #elif j>= 10 and j < 100:
        #	empty_name = empty_name + '.0' + str(j)
        #elif j > 100:
        #	empty_name = empty_name + '.' + str(j)
    	#print (empty_name)
    	j = j + 1
		

def print_empty(no_of_bgdpoints):
	bpy.context.scene.frame_set(init_frame)
	output_name = filepath + 'bgd_points' + '.txt'
	output = open(output_name, 'w')
	k = 0
	while k < no_of_bgdpoints:
		empty_name = 'Empty'
		if k > 0 and k < 10:
			empty_name = empty_name + '.00' + str(k)
		elif k>= 10 and k < 100:
			empty_name = empty_name + '.0' + str(k)
		elif k > 100:
			empty_name = empty_name + '.' + str(j)              
		point = bpy.data.objects[empty_name]
		coords = (point.matrix_world*point.location)[0:3]
		x = coords[0]
		y = coords[1]
		z = coords[2]
		
		output.write(str(k+1) + '\t' + str(x) + '\t' + str(y) + '\t' + str(z) + '\n')
		k = k + 1
	output.close()


def delete_empty(no_of_bgdpoints):
    n = 0
    while n < no_of_bgdpoints:
        empty_name = 'Empty'
        if n > 0 and n < 10:
            empty_name = empty_name + '.00' + str(n)
        elif n>= 10 and n < 100:
            empty_name = empty_name + '.0' + str(n) 
        elif n > 100:
        	 empty_name = empty_name + '.' + str(j)        
        try:
            bpy.data.objects[empty_name].select = True
        except:
            print('testing')
        bpy.ops.object.delete() 

          
        n = n + 1


clip = bpy.data.movieclips[clipname]
i = 1
bpy.context.scene.frame_set(1)
while i <= no_of_horses:
    
    if i > 0 and i < 10:
        counter = 'H' + '00' + str(i)
    elif i >= 10 and i < 100:
        counter = 'H' + '0' + str(i)
    elif i >= 100:
        counter = 'H' + str(i)
    current_horse = set_horse(i)
    print_one_horse(init_frame, end_frame, current_horse, counter)
    i = i + 1

link_bgd_empty(no_of_bgdpoints) 

print_empty(no_of_bgdpoints)

#delete_empty(no_of_bgdpoints)

outputx.close()
outputy.close()


