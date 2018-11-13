'''
Michael Oliver 

Demo of a watcher to move files into place
'''

from time import sleep
from datetime import datetime
import logging
import os
import shutil

def create_folder(f):
    '''
    Check if a folder exists, if not create it
    '''
    if not os.path.exists(f):
        logging.info("Creating Folder: {}".format(f))
        os.makedirs(f)
        return f
    return f

def setupLogging(log_folder='logs'):
    '''
    Setup logging to timestamped log files in a logs directory
    '''
    create_folder(log_folder)
    LOGFILE = os.path.join('logs','{}.log'.format(datetime.now()))
    logging.basicConfig(filename=LOGFILE,level=logging.DEBUG,format='%(asctime)s - %(levelname)s - %(message)s')
    return LOGFILE

def fileisNotBeingWritten(f,wait_time=10):
    '''
    Stats a file every 'wait_time' seconds to see if the file size has changed
    '''
    while True:
        fs1 = os.stat(f).st_size
        sleep(wait_time)
        if (os.stat(f).st_size - fs1 ) == 0:
            return True

def copy(src, dst, copy=False, move=False, overwrite=False):
    '''
    Copy Function.  src should be file, dst a dir
    '''
    dst_filename = os.path.join(dst,os.path.split(src)[1])

    if not os.path.exists(dst):
        os.makedirs(dst)
    
    if overwrite and os.path.exists(dst_filename):
        logging.info("File Exists and Overwrite Enabled. Removing: {}".format(dst_filename))
        os.remove(dst_filename)
    
    if copy == True:
        logging.info("Copying {} --> {}".format(src,dst_filename))
        shutil.copy2(src, dst)
    
    elif move == True:
        logging.info("Moving {} --> {}".format(src,dst_filename))
        shutil.move(src, dst)


def moveQuicktimes(src_folder, wait_time=10):
    '''
    Scans the _submit folder within the src_folder and copies and moves 
    the quicktimes to _approvals and output

    After complete will wait for wait_time duration in seconds

    Seqence is first two chars
    Shot is subsequent 4 chars
    '''
    while True:
        src_submit = create_folder(os.path.join(src_folder,'_submit'))
        files = [os.path.join(src_submit,f) for f in os.listdir(src_submit) if f.endswith('.mov')]
        for f in files:
            if fileisNotBeingWritten(f):
                filename    = os.path.split(f)[1]
                seq         = filename[:2]
                shot        = filename[2:6]
                todays_date = datetime.now().strftime("%Y%m%d")
                dst_date    = os.path.join(src_folder,seq,'_approvals',todays_date)
                dst_output  = os.path.join(src_folder,seq,shot,'output')

                copy(src=f, dst=dst_date, copy=True, overwrite=True)
                copy(src=f, dst=dst_output, move=True, overwrite=True)

        sleep(wait_time)

print ("Logging to %s" % setupLogging())
logging.info("Move Tool Started")

src_folder = r'/Users/moliver/Desktop/personal/test'
moveQuicktimes(src_folder, wait_time=10)

