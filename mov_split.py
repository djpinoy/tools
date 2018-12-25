#!/usr/local/bin/python2.7

#from __future__ import division
from datetime import datetime
import os
import shutil
import tempfile
import fnmatch
import sys

print "Starting mov_split...\n";
startTime = datetime.now()
print "START: " + str(startTime)


# Create an array which holds all file extensions to look for
video_file_types = []
video_file_types.append("*.MOV")
video_file_types.append("*.mov")
video_file_types.append("*.mp4")
video_file_types.append("*.MP4")
video_file_types.append("*.avi")
video_file_types.append("*.AVI")
video_file_types.append("*.mts")
video_file_types.append("*.MTS")

total_video_file_size = 0

# Create array for photo file types
photo_file_types = []
photo_file_types.append("*.CR2")
photo_file_types.append("*.cr2")
photo_file_types.append("*.JPG")
photo_file_types.append("*.jpg")
photo_file_types.append("*.ARW")
photo_file_types.append("*.arw")
photo_file_types.append("*.RW2")
photo_file_types.append("*.rw2")

total_photo_file_size = 0

# BOZO: Try with single dir first...
#os.chdir("2011")

# Iterate through all years in current dir (/all/pics/...)
for year_dir in sorted(os.listdir(".")):
    if fnmatch.fnmatch(year_dir, '20*'):
        os.chdir(year_dir)
        cwd = os.getcwd()
        print "Current directory is " + cwd


        # First, grab all the directories in the current year, and then sort them.
        # BOZO: Assumes that there aren't any files in the year dir itself (which should be the case)
        directory_list = []
        for directory in os.listdir("."):
            directory_list.append(directory)
        directory_list.sort()

        for directory in directory_list:
            print "Examining " + directory
            # Reset flag
            video_found_flag = 0
            # Iterate through all video_file_types and check if one exists
            for video_file_type in video_file_types:
                # Use os.walk to get a recursive list under this dir
                for year_root, dirnames, filenames in os.walk(directory):
                    for filename in fnmatch.filter(filenames, video_file_type):
                        print "    Found video file: " + filename
                        video_found_flag = 1
            # if video_func_flag = 1, do the copy
            if video_found_flag == 1:
                print "        Found video files in " + directory
                target_dir = "/mnt/scratch5tb/video/incoming/" + directory
                if os.path.isdir(target_dir):
                    # BOZO: SHOULD NOT GET HERE IF DIR IS ALREADY PROCESSED!!!
                    print "ERROR: TARGET DIR ALREADY EXISTS - DID SOMETHING GO WRONG?"
                    sys.exit()
                    #print "        Deleting existing target_dir: " + target_dir
                    #shutil.rmtree(target_dir)
                print "        Copying " + directory + " to " + target_dir
                shutil.copytree(directory, target_dir)
                print "        Completed copying " + directory

                # Once this copying is done:
                # - iterate through all video_file_types,
                dir_video_file_size = 0
                for video_file_type in video_file_types:
                    #   - delete video files from src_dir
                    for year_root, dirnames, filenames in os.walk(directory):
                        for filename in fnmatch.filter(filenames, video_file_type):
                            file_to_delete = os.path.join(year_root, filename)
                            dir_video_file_size += os.path.getsize(file_to_delete)
                            print "        Deleting duplicate video file: " + file_to_delete
                            os.remove(file_to_delete)
                print "        Deleted " + str(dir_video_file_size/1024/1024) + " Mbytes of video from src_dir"
                total_video_file_size += dir_video_file_size

                # - iterate through all photo_file_types,
                dir_photo_file_size = 0
                for photo_file_type in photo_file_types:
                    #   - delete photo files from target_dir
                    for year_root, dirnames, filenames in os.walk(target_dir):
                        for filename in fnmatch.filter(filenames, photo_file_type):
                            file_to_delete = os.path.join(year_root, filename)
                            dir_photo_file_size += os.path.getsize(file_to_delete)
                            print "        Deleting photo file: " + file_to_delete
                            os.remove(file_to_delete)
                print "        Deleted " + str(dir_photo_file_size/1024/1024) + " Mbytes of photos from target_dir"
                total_photo_file_size += dir_photo_file_size

        # go back up one level once done with this year_dir
        os.chdir("..")

# Calculate stats here in GB:
total_video_file_size = total_video_file_size / 1024 / 1024 / 1024;
total_photo_file_size = total_photo_file_size / 1024 / 1024 / 1024;



print "\n\n\n"
print "### STATS ###"
print "Moved " + str(total_video_file_size) + " GB of video to scratch25tb"
print "Saved " + str(total_photo_file_size) + " GB of photo back in /all/pics"
print "END: " + str(datetime.now())
print "Elapsed Time: " + str(datetime.now() - startTime)
print "### STATS ###"
print "\n\n\n"

