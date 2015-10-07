# -*- coding: utf-8 -*-
#
# Copyright © 2008-2015  Red Hat, Inc. All rights reserved.
# Copyright © 2008-2015  Luke Macken <lmacken@redhat.com>
# Copyright © 2008  Kushal Das <kushal@fedoraproject.org>
# Copyright © 2015  Sam Parkinson <sam@sam.today>
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA. Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Author(s): Luke Macken <lmacken@redhat.com>
#            Kushal Das <kushal@fedoraproject.org>

"""
A cross-platform graphical interface for the LiveUSBCreator
"""

import os
import sys
import logging
import urlparse
import json
from urllib2 import urlopen
import traceback

from time import sleep, time
from datetime import datetime
from PyQt4 import QtCore, QtGui

from sugarstick import LiveUSBCreator, LiveUSBError, LiveUSBInterface, _
if sys.platform == 'win32':
    from sugarstick.urlgrabber.grabber import URLGrabber, URLGrabError
    from sugarstick.urlgrabber.progress import BaseMeter
else:
    from urlgrabber.grabber import URLGrabber, URLGrabError
    from urlgrabber.progress import BaseMeter

try:
    import dbus.mainloop.qt
    dbus.mainloop.qt.DBusQtMainLoop(set_as_default=True)
except:
    pass

MAX_FAT16 = 2047
MAX_FAT32 = 3999
MAX_EXT = 2097152

if sys.platform == 'win32':
    IS_64BITS = True  # FIXME
else:
    IS_64BITS = sys.maxsize > 2**32
ARCH = 'x86_64' if IS_64BITS else 'i686'
if IS_64BITS:
    DOWNLOAD = 'https://download.fedoraproject.org/pub/fedora/linux/releases/test/23_Beta/Live/x86_64/Fedora-Live-SoaS-x86_64-23_Beta-1.iso'
else:
    DOWNLOAD = 'https://download.fedoraproject.org/pub/fedora/linux/releases/test/23_Beta/Live/i386/Fedora-Live-SoaS-i686-23_Beta-1.iso'

LOGGER_URL = 'http://sugarstick-creator.sam.today/log'
if len(sys.argv) == 2:
    UID = sys.argv[1]
else:
    UID = None
    for i in os.listdir(os.getcwd()):
        if i[0] == 'E' or i[0] == 'S':
            UID = i.split('.')[0]
            break
    if UID is None:
        from uuid import uuid4
        UID = 'C' + str(uuid4())
START_T = time()


class LiveUSBApp(QtGui.QApplication):
    """ Main application class """
    def __init__(self, opts, args):
        if sys.platform[:5] == 'linux':
            QtGui.QApplication.setGraphicsSystem('native')

        QtGui.QApplication.__init__(self, args)
        self.mywindow = LiveUSBWindow(opts, args)
        self.mywindow.show()
        try:
            self.exec_()
        finally:
            self.mywindow.terminate()


class ReleaseDownloader(QtCore.QThread):

    def __init__(self, progress, proxies):
        QtCore.QThread.__init__(self)
        self.progress = progress
        self.proxies = proxies
        self.url = DOWNLOAD

    def run(self):
        self.emit(QtCore.SIGNAL("status(PyQt_PyObject)"),
                  _("Downloading %s..." % os.path.basename(self.url)))
        grabber = URLGrabber(progress_obj=self.progress, proxies=self.proxies)
        home = os.getenv('HOME', 'USERPROFILE')
        filename = os.path.basename(urlparse.urlparse(self.url).path)
        for folder in ('Downloads', 'My Documents'):
            if os.path.isdir(os.path.join(home, folder)):
                filename = os.path.join(home, folder, filename)
                break

        if os.path.isfile(filename):
            self.emit(QtCore.SIGNAL("dlcomplete(PyQt_PyObject)"), filename)
            return


        try:
            iso = grabber.urlgrab(self.url, reget='simple')
        except URLGrabError, e:
            self.emit(QtCore.SIGNAL("dlcomplete(PyQt_PyObject)"), e.strerror)
        else:
            self.emit(QtCore.SIGNAL("dlcomplete(PyQt_PyObject)"), iso)


_LMS = []
def log_message(message):
    t = LoggingMessage(message)
    _LMS.append(t)
    t.start()

class LoggingMessage(QtCore.QThread):

    def __init__(self, message):
        QtCore.QThread.__init__(self)
        message['from'] = UID
        message['timedelta'] = int(time() - START_T)
        self._message = message

    def run(self):
        body = json.dumps({'uid': UID, 'dump': self._message})
        print 'Sending %s to logger' % body

        f = urlopen(LOGGER_URL, body)
        print 'Url response:', f.read()


class DownloadProgress(QtCore.QObject, BaseMeter):
    """ A QObject urlgrabber BaseMeter class.

    This class is called automatically by urlgrabber with our download details.
    This class then sends signals to our main dialog window to update the
    progress bar.
    """
    def start(self, filename=None, url=None, basename=None, size=None,
              now=None, text=None):
        self.emit(QtCore.SIGNAL("maxprogress(int)"), size)

    def update(self, amount_read, now=None):
        """ Update our download progressbar.

        :read: the number of bytes read so far
        """
        self.emit(QtCore.SIGNAL("progress(int)"), amount_read)

    def end(self, amount_read):
        self.update(amount_read)


class ProgressThread(QtCore.QThread):
    """ A thread that monitors the progress of Live USB creation.

    This thread periodically checks the amount of free space left on the
    given drive and sends a signal to our main dialog window to update the
    progress bar.
    """
    totalsize = 0
    orig_free = 0
    drive = None
    get_free_bytes = None
    alive = True

    def set_data(self, size, drive, freebytes):
        self.totalsize = size / 1024
        self.drive = drive
        self.get_free_bytes = freebytes
        self.orig_free = self.get_free_bytes()
        self.emit(QtCore.SIGNAL("maxprogress(int)"), self.totalsize)

    def run(self):
        while self.alive:
            free = self.get_free_bytes()
            value = (self.orig_free - free) / 1024
            self.emit(QtCore.SIGNAL("progress(int)"), value)
            if value >= self.totalsize:
                break
            sleep(3)

    def stop(self):
        self.alive = False

    def terminate(self):
        self.emit(QtCore.SIGNAL("progress(int)"), self.totalsize)
        QtCore.QThread.terminate(self)


class LiveUSBThread(QtCore.QThread):

    def __init__(self, live, progress, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.progress = progress
        self.parent = parent
        self.live = live

    def status(self, text):
        self.emit(QtCore.SIGNAL("status(PyQt_PyObject)"), text)

    def run(self):
        handler = LiveUSBLogHandler(self.status)
        self.live.log.addHandler(handler)
        now = datetime.now()
        try:
            #if self.parent.opts.format:
            #    self.live.unmount_device()
            #    self.live.format_device()

            # Initialize zip-drive-compatible geometry
            #if self.parent.opts.zip:
            #    self.live.dest = self.live.drive['mount']
            #    self.live.drive['unmount'] = True
            #    self.live.unmount_device()
            #    self.live.initialize_zip_geometry()
            #    self.live.drive = self.parent.get_selected_drive()
            #    self.live.dest = self.live.drive['mount']
            #    self.live.drive['unmount'] = True
            #    self.live.unmount_device()
            #    self.live.format_device()

            # If we're going to dd the image
            if self.parent.destructiveButton.isChecked():
                log_message({'type': 'start', 'dd': True})
                self.parent.progressBar.setRange(0, 0)
                self.live.dd_image()
                self.live.log.removeHandler(handler)
                duration = str(datetime.now() - now).split('.')[0]
                self.status(_("Complete! (%s)") % duration)
                log_message({'type': 'finish', 'dd': True, 'duration': duration})
                self.parent.progressBar.setRange(0, 1)
                return

            log_message({'type': 'start', 'dd': False})

            self.live.verify_filesystem()
            if not self.live.drive['uuid'] and not self.live.label:
                self.status(_("Error: Cannot set the label or obtain "
                              "the UUID of your device.  Unable to continue."))
                log_message({'type': 'failafterverifyfs'})
                self.live.log.removeHandler(handler)
                return

            self.live.check_free_space()

            if not self.parent.opts.noverify:
                # Verify the MD5 checksum inside of the ISO image
                if not self.live.verify_iso_md5():
                    self.live.log.removeHandler(handler)
                    return

                # If we know about this ISO, and it's SHA1 -- verify it
                release = self.live.get_release_from_iso()
                if release and ('sha1' in release or 'sha256' in release):
                    if not self.live.verify_iso_sha1(progress=self):
                        self.live.log.removeHandler(handler)
                        return


            # Setup the progress bar
            self.progress.set_data(size=self.live.totalsize,
                                   drive=self.live.drive['device'],
                                   freebytes=self.live.get_free_bytes)
            self.progress.start()

            log_message({'type': 'startextraction', 'dd': False})
            self.live.extract_iso()
            self.live.create_persistent_overlay()
            self.live.update_configs()
            self.live.install_bootloader()
            self.live.bootable_partition()
            log_message({'type': 'finishextraction', 'dd': False})

            if self.parent.opts.device_checksum:
                self.live.calculate_device_checksum(progress=self)
            if self.parent.opts.liveos_checksum:
                self.live.calculate_liveos_checksum()

            self.progress.stop()

            # Flush all filesystem buffers and unmount
            self.live.flush_buffers()
            self.live.unmount_device()

            duration = str(datetime.now() - now).split('.')[0]
            log_message({'type': 'finish', 'dd': False, 'duration': duration})
            self.status(_("Complete! (%s)" % duration))

        except Exception, e:
            self.status(e.args[0])
            tb = traceback.format_tb(e)
            self.status(_("LiveUSB creation failed!"))
            self.live.log.exception(tb)
            log_message({'type': 'fail', 'tb': tb})

        self.live.log.removeHandler(handler)
        self.progress.terminate()

    def set_max_progress(self, maximum):
        self.emit(QtCore.SIGNAL("maxprogress(int)"), maximum)

    def update_progress(self, value):
        self.emit(QtCore.SIGNAL("progress(int)"), value)

    def __del__(self):
        self.wait()


class LiveUSBLogHandler(logging.Handler):

    def __init__(self, cb):
        logging.Handler.__init__(self)
        self.cb = cb

    def emit(self, record):
        if record.levelname in ('INFO', 'ERROR', 'WARN'):
            self.cb(record.msg)


class LiveUSBWindow(QtGui.QMainWindow, LiveUSBInterface):
    """ Our main dialog class """

    def __init__(self, opts, args):
        log_message({'type': 'launch', 'platform': sys.platform, 'arch': ARCH}) 
        self.in_process = False
        QtGui.QMainWindow.__init__(self)
        LiveUSBInterface.__init__(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.opts = opts
        self.args = args
        self.setupUi(self)
        self.live = LiveUSBCreator(opts=opts)
        self.populate_devices()
        self.downloader = None
        self.progress_thread = ProgressThread()
        self.download_progress = DownloadProgress()
        self.live_thread = LiveUSBThread(live=self.live,
                                         progress=self.progress_thread,
                                         parent=self)
        self.connect_slots()
        self.confirmed = False
        self.mbr_reset_confirmed = False

        if sys.platform == 'win32':
            self.destructiveButton.setEnabled(False)  # FIXME
        elif self.opts.destructive:
            self.destructiveButton.setChecked(True)

        # Intercept all sugarstick INFO log messages, and display them in the gui
        self.handler = LiveUSBLogHandler(lambda x: self.textEdit.append(x))
        self.live.log.addHandler(self.handler)
        if not self.opts.verbose:
            self.live.log.removeHandler(self.live.handler)

        # If an ISO was specified on the command line, use it.
        if args:
            for arg in self.args:
                if arg.lower().endswith('.iso') and os.path.exists(arg):
                    self.selectfile(arg)

        # Determine if we have admin rights
        if not self.live.is_admin():
            self.live.log.error(_('Warning: This tool needs to be run as an '
                'Administrator. To do this, right click on the icon and open '
                'the Properties. Under the Compatibility tab, check the "Run '
                'this program as an administrator" box.'))
        self.live.log.error('Args are %r' % sys.argv)

    def populate_devices(self, *args, **kw):
        if self.in_process:
            return
        self.driveBox.clear()
        #self.textEdit.clear()

        def add_devices():
            if not len(self.live.drives):
                self.textEdit.setPlainText(_("Unable to find any USB drives"))
                self.startButton.setEnabled(False)
                return
            for device, info in self.live.drives.items():
                if info['label']:
                    self.driveBox.addItem("%s (%s)" % (device, info['label']))
                else:
                    self.driveBox.addItem(device)
            self.startButton.setEnabled(True)

        try:
            self.live.detect_removable_drives(callback=add_devices)
        except LiveUSBError, e:
            self.textEdit.setPlainText(e.args[0])
            self.startButton.setEnabled(False)

    def connect_slots(self):
        self.connect(self, QtCore.SIGNAL('triggered()'), self.terminate)
        self.connect(self.startButton, QtCore.SIGNAL("clicked()"), self.begin)
        self.connect(self.live_thread, QtCore.SIGNAL("status(PyQt_PyObject)"),
                     self.status)
        self.connect(self.live_thread, QtCore.SIGNAL("finished()"),
                     lambda: self.enable_widgets(True))
        self.connect(self.live_thread, QtCore.SIGNAL("terminated()"),
                     lambda: self.enable_widgets(True))
        self.connect(self.live_thread, QtCore.SIGNAL("progress(int)"),
                     self.progress)
        self.connect(self.live_thread, QtCore.SIGNAL("maxprogress(int)"),
                     self.maxprogress)
        self.connect(self.progress_thread, QtCore.SIGNAL("progress(int)"),
                     self.progress)
        self.connect(self.progress_thread, QtCore.SIGNAL("maxprogress(int)"),
                     self.maxprogress)
        self.connect(self.download_progress, QtCore.SIGNAL("maxprogress(int)"),
                     self.maxprogress)
        self.connect(self.download_progress, QtCore.SIGNAL("progress(int)"),
                     self.progress)
        if hasattr(self, 'refreshDevicesButton'):
            self.connect(self.refreshDevicesButton, QtCore.SIGNAL("clicked()"),
                         self.populate_devices)

        # If we have access to HAL & DBus, intercept some useful signals
        if hasattr(self.live, 'udisks'):
            self.live.udisks.connect_to_signal('DeviceAdded',
                                            self.populate_devices)
            self.live.udisks.connect_to_signal('DeviceRemoved',
                                            self.populate_devices)

    def get_max_freespace(self, drive=None):
        """
        Returns the amount of free space
        on the device and the ISO size.
        """
        if not drive:
            drive = self.get_selected_drive()
            if not drive:
                return

        device = self.live.drives[drive]
        freespace = device['free']
        device_size = device['size'] / 1024**2

        if device['fsversion'] == 'FAT32':
            self.live.log.debug(_('Partition is FAT32; Restricting overlay '
                                  'size to 4G'))
            max_space = MAX_FAT32
        elif device['fsversion'] == 'FAT16':
            self.live.log.debug(_('Partition is FAT16; Restricting overlay '
                                  'size to 2G'))
            max_space = MAX_FAT16
        else:
            max_space = MAX_EXT

        if freespace:
            if freespace > device_size:
                freespace = device_size
            if freespace > max_space:
                freespace = max_space

        if not device['mount']:
            self.live.log.warning(_('Device is not yet mounted, so we cannot '
                                    'determine the amount of free space.'))
            if not freespace:
                freespace = device_size
        else:
            if not freespace:
                self.live.log.warning(_('No free space on %s') % drive)
                freespace = 0

        # Subtract the size of the ISO from our maximum overlay size
        if self.live.isosize:
            iso_size = self.live.isosize / 1024**2
            if freespace + iso_size > device['free']:
                freespace -= iso_size

        freespace -= 1 # Don't fill the device 100%

        if freespace < 0:
            freespace = 0

        return freespace

    def progress(self, value):
        self.progressBar.setValue(value)

    def maxprogress(self, value):
        self.progressBar.setMaximum(value)

    def status(self, text):
        if not isinstance(text, basestring):
            text = str(text)
        self.textEdit.append(text)

    def enable_widgets(self, enabled=True):
        self.startButton.setEnabled(enabled)
        self.driveBox.setEnabled(enabled)
        self.destructiveButton.setEnabled(enabled and sys.platform != 'win32')  # FIXME
        self.nonDestructiveButton.setEnabled(enabled)
        if hasattr(self, 'refreshDevicesButton'):
            self.refreshDevicesButton.setEnabled(enabled)
        self.in_process = not enabled

    def get_selected_drive(self):
        text = self.live._to_unicode(self.driveBox.currentText()).split()
        if text:
            return text[0]

    def begin(self):
        """ Begin the sugarstick creation process.

        This method is called when the "Create LiveUSB" button is clicked.
        """
        self.enable_widgets(False)
        self.live.drive = self.get_selected_drive()

        # Unmount the device and check the MBR
        if self.nonDestructiveButton.isChecked():
            if self.live.blank_mbr():
                if not self.mbr_reset_confirmed:
                    self.status(_("The Master Boot Record on your device is blank. "
                                  "Pressing 'Create Create Sugar on a Stick' again will reset the "
                                  "MBR on this device."))
                    self.mbr_reset_confirmed = True
                    self.enable_widgets(True)
                    return
                if self.live.drive['mount']:
                    self.live.dest = self.live.drive['mount']
                    self.live.unmount_device()
                self.live.reset_mbr()
            elif not self.live.mbr_matches_syslinux_bin():
                if self.opts.reset_mbr:
                    self.live.reset_mbr()
                else:
                    self.live.log.warn(_("Warning: The Master Boot Record on your device "
                                  "does not match your system's syslinux MBR.  If you "
                                  "have trouble booting this stick, try running the "
                                  "sugarstick-creator with the --reset-mbr option."))

            try:
                self.live.mount_device()
            except LiveUSBError, e:
                self.status(e.args[0])
                self.enable_widgets(True)
                return
            except OSError, e:
                self.status(_('Unable to mount device'))
                self.enable_widgets(True)
                return

            if self.live.existing_liveos():
                if not self.confirmed:
                    self.status(_("Your device already contains Sugar on a Stick.\nIf you "
                                  "continue, this will be overwritten."))
                    if self.live.existing_overlay() and self.live.overlay > 0:
                        self.status(_("Warning: Creating a new persistent overlay "
                                      "will delete your existing one."))
                    self.status(_("Press 'Create Create Sugar on a Stick' again if you wish to "
                                  "continue."))
                    self.confirmed = True
                    #self.live.unmount_device()
                    self.enable_widgets(True)
                    return
                else:
                    # The user has confirmed that they wish to overwrite their
                    # existing Live OS.  Here we delete it first, in order to
                    # accurately calculate progress.
                    self.confirmed = False
                    try:
                        self.live.delete_liveos()
                    except LiveUSBError, e:
                        self.status(e.args[0])
                        #self.live.unmount_device()
                        self.enable_widgets(True)
                        return
        else:
            # Require confirmation for destructive installs
            if not self.confirmed:
                self.status(_("WARNING: You are about to perform a destructive install. This will destroy all data and partitions on your USB drive. Press 'Create Sugar on a Stick' again to continue."))
                self.confirmed = True
                self.enable_widgets(True)
                return

        # Remove the log handler, because our live thread will register its own
        self.live.log.removeHandler(self.handler)

        # If the user has selected an ISO, use it.  If not, download one.
        log_message({'type': 'dlstart'})
        self._start_dl_time = time()
        self.downloader = ReleaseDownloader(
                progress=self.download_progress,
                proxies=self.live.get_proxies())
        self.connect(self.downloader,
                     QtCore.SIGNAL("dlcomplete(PyQt_PyObject)"),
                     self.download_complete)
        self.connect(self.downloader,
                     QtCore.SIGNAL("status(PyQt_PyObject)"),
                     self.status)
        self.downloader.start()

    def download_complete(self, iso):
        """ Called by our ReleaseDownloader thread upon completion.

        Upon success, the thread passes in the filename of the downloaded
        release.  If the 'iso' argument is not an existing file, then
        it is assumed that the download failed and 'iso' should contain
        the error message.
        """
        dl_time = time() - self._start_dl_time
        if os.path.exists(iso):
            log_message({'type': 'dlfinish', 'timetaken': dl_time})
            self.status(_("Download complete!"))
            self.live.set_iso(iso)
            self.live.overlay = self.get_max_freespace()
            self.live_thread.start()
        else:
            log_message({'type': 'dlfail'})
            self.status(_("Download failed: " + iso))
            self.status(_("You can try again to resume your download"))
            self.enable_widgets(True)

    def terminate(self):
        """ Terminate any processes that we have spawned """
        self.live.terminate()

    def closeEvent(self, event):
        log_message({'type': 'close'})
        event.accept()
