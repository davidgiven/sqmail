# Preference setting abstraction.
# $Source: /cvsroot/sqmail/sqmail/src/sqmail/gui/preferences.py,v $
# $State: Exp $

import os
import sqmail.preferences
import sqmail.gui.reader
import sqmail.utils
import sqmail.db
import sqmail.picons
import cPickle
import getpass
import tempfile
import gtk
import GdkImlib
import string

instance = None
class SQmaiLPreferences:
	def __init__(self, reader):
		global instance

		if instance:
			return
		instance = self

		self.reader = reader
		preferenceswin = reader.readglade("preferenceswin", self)
		self.widget = sqmail.gui.utils.WidgetStore(preferenceswin)

		# Transport

		p = sqmail.preferences.get_incomingprotocol()
		if (p == "IMAP"):
			self.widget.imapbutton.set_active(1)
		elif (p == "POP"):
			self.widget.popbutton.set_active(1)
		elif (p == "Spool"):
			self.widget.spoolbutton.set_active(1)

		self.widget.incomingserver.set_text(sqmail.preferences.get_incomingserver())

		self.widget.incomingport.set_text(str(sqmail.preferences.get_incomingport()))

		self.widget.incomingusername.set_text(sqmail.preferences.get_incomingusername())

		self.widget.incomingpassword.set_text(sqmail.preferences.get_incomingpassword())

		self.widget.incomingpath.set_text(sqmail.preferences.get_incomingpath())

		self.widget.deleteremotebutton.set_active(sqmail.preferences.get_deleteremote())

		self.widget.fromaddress.set_text(sqmail.preferences.get_fromaddress())

		self.widget.outgoingserver.set_text(sqmail.preferences.get_outgoingserver())

		self.widget.outgoingport.set_text(str(sqmail.preferences.get_outgoingport()))

		self.widget.smtpdebug.set_active(sqmail.preferences.get_smtpdebuglevel())

		self.widget.defaultdomain.set_text(sqmail.preferences.get_defaultdomain())

		self.widget.sendxface.set_active(sqmail.preferences.get_sendxface())

		sqmail.gui.utils.set_face(self.widget.outgoingxfaceicon, sqmail.preferences.get_outgoingxfaceicon())

		# Appearances

		self.widget.textmessagefont.set_font_name(sqmail.preferences.get_textmessagefont())

		self.widget.composefont.set_font_name(sqmail.preferences.get_composefont())

		self.widget.vfolderfont.set_font_name(sqmail.preferences.get_vfolderfont())
		apply(self.widget.vfolderfg.set_i16, sqmail.preferences.get_vfolderfg())
		apply(self.widget.vfolderbg.set_i16, sqmail.preferences.get_vfolderbg())

		self.widget.vfolderunreadfont.set_font_name(sqmail.preferences.get_vfolderunreadfont())
		apply(self.widget.vfolderunreadfg.set_i16, sqmail.preferences.get_vfolderunreadfg())
		apply(self.widget.vfolderunreadbg.set_i16, sqmail.preferences.get_vfolderunreadbg())

		self.widget.vfolderpendingfont.set_font_name(sqmail.preferences.get_vfolderpendingfont())
		apply(self.widget.vfolderpendingfg.set_i16, sqmail.preferences.get_vfolderpendingfg())
		apply(self.widget.vfolderpendingbg.set_i16, sqmail.preferences.get_vfolderpendingbg())

		self.widget.msglistfont.set_font_name(sqmail.preferences.get_msglistfont())

		self.widget.unreadmsglistfont.set_font_name(sqmail.preferences.get_unreadmsglistfont())

		self.widget.pendingmsglistfont.set_font_name(sqmail.preferences.get_pendingmsglistfont())
		
		# Spamcop

		self.widget.deletespam.set_active(sqmail.preferences.get_deletespam())

		self.widget.deletespamreply.set_active(sqmail.preferences.get_deletespamreply())

		self.widget.spamaddress.set_text(sqmail.preferences.get_spamaddress())

		self.widget.spamreplyfrom.set_text(sqmail.preferences.get_spamreplyfrom())

		p = sqmail.preferences.get_spamcopmember()
		if p:
			self.widget.spamcopmemberyes.set_active(1)
		else:
			self.widget.spamcopmemberno.set_active(1)
		
		# Mail icons

		self.widget.usexfaces.set_active(sqmail.preferences.get_usexfaces())

		self.widget.xfacedecoder.set_text(sqmail.preferences.get_xfacedecoder())

		self.widget.xfaceencoder.set_text(sqmail.preferences.get_xfaceencoder())

		self.widget.usepicons.set_active(sqmail.preferences.get_usepicons())

		self.widget.usepiconsproxy.set_active(sqmail.preferences.get_usepiconsproxy())

		self.widget.omitpiconsuser.set_active(sqmail.preferences.get_omitpiconsuser())

		self.widget.piconsserver.set_text(sqmail.preferences.get_piconsserver())

		self.widget.piconsproxyserver.set_text(sqmail.preferences.get_piconsproxyserver())

		self.widget.piconsproxyport.set_text("%d" % sqmail.preferences.get_piconsproxyport())

		self.on_update_piconsstatus(None)
		
		# Miscellaneous

		self.widget.quoteprefix.set_text(sqmail.preferences.get_quoteprefix())
	
		#self.widget.spamcommand.set_text(get_spamcommand())

	# Signal handlers.

	def on_deactivate(self, obj):
		global instance
		self.widget.preferenceswin.destroy()
		instance = None

	def on_apply(self, obj, a):
		if (a == 1):
			return
		
		# Transport

		if (self.widget.imapbutton.get_active()):
			p = "IMAP"
		elif (self.widget.popbutton.get_active()):
			p = "POP"
		elif (self.widget.spoolbutton.get_active()):
			p = "Spool"
		sqmail.utils.setsetting("incomingprotocol", p)

		sqmail.utils.setsetting("incomingserver", \
			self.widget.incomingserver.get_text())

		sqmail.utils.setsetting("incomingport", \
			int(self.widget.incomingport.get_text()))

		sqmail.utils.setsetting("incomingusername", \
			self.widget.incomingusername.get_text())

		sqmail.utils.setsetting("incomingpassword", \
			self.widget.incomingpassword.get_text())

		sqmail.utils.setsetting("incomingpath", \
			self.widget.incomingpath.get_text())

		sqmail.utils.setsetting("deleteremote", \
			self.widget.deleteremotebutton.get_active())

		sqmail.utils.setsetting("fromaddress", \
			self.widget.fromaddress.get_text())

		sqmail.utils.setsetting("outgoingserver", \
			self.widget.outgoingserver.get_text())

		sqmail.utils.setsetting("outgoingport", \
			int(self.widget.outgoingport.get_text()))

		sqmail.utils.setsetting("smtpdebuglevel", \
			self.widget.smtpdebug.get_active())

		sqmail.utils.setsetting("defaultdomain", \
			self.widget.defaultdomain.get_text())

		sqmail.utils.setsetting("sendxface", \
			self.widget.sendxface.get_active())

		sqmail.utils.setsetting("outgoingxfaceicon", \
			self.widget.outgoingxfaceicon.get_data("face"))

		# Appearances
	
		sqmail.utils.setsetting("textmessagefont", \
			self.widget.textmessagefont.get_font_name())

		sqmail.utils.setsetting("composefont", \
			self.widget.composefont.get_font_name())

		sqmail.utils.setsetting("vfolderfont", \
			self.widget.vfolderfont.get_font_name())
		sqmail.utils.setsetting("vfolderfg", \
			self.widget.vfolderfg.get_i16())
		sqmail.utils.setsetting("vfolderbg", \
			self.widget.vfolderbg.get_i16())

		sqmail.utils.setsetting("vfolderunreadfont", \
			self.widget.vfolderunreadfont.get_font_name())
		sqmail.utils.setsetting("vfolderunreadfg", \
			self.widget.vfolderunreadfg.get_i16())
		sqmail.utils.setsetting("vfolderunreadbg", \
			self.widget.vfolderunreadbg.get_i16())

		sqmail.utils.setsetting("vfolderpendingfont", \
			self.widget.vfolderpendingfont.get_font_name())
		sqmail.utils.setsetting("vfolderpendingfg", \
			self.widget.vfolderpendingfg.get_i16())
		sqmail.utils.setsetting("vfolderpendingbg", \
			self.widget.vfolderpendingbg.get_i16())

		sqmail.utils.setsetting("msglistfont", \
			self.widget.msglistfont.get_font_name())

		sqmail.utils.setsetting("unreadmsglistfont", \
			self.widget.unreadmsglistfont.get_font_name())

		sqmail.utils.setsetting("pendingmsglistfont", \
			self.widget.pendingmsglistfont.get_font_name())

		# Spamcop

		sqmail.utils.setsetting("deletespam", \
			self.widget.deletespam.get_active())

		sqmail.utils.setsetting("deletespamreply", \
			self.widget.deletespamreply.get_active())

		sqmail.utils.setsetting("spamaddress", \
			self.widget.spamaddress.get_text())

		sqmail.utils.setsetting("spamreplyfrom", \
			self.widget.spamreplyfrom.get_text())

		sqmail.utils.setsetting("spamcopmember", \
			self.widget.spamcopmemberyes.get_active())
		
		# Mail icons

		sqmail.utils.setsetting("usexfaces", \
			self.widget.usexfaces.get_active())

		sqmail.utils.setsetting("xfaceencoder", \
			self.widget.xfaceencoder.get_text())

		sqmail.utils.setsetting("xfacedecoder", \
			self.widget.xfacedecoder.get_text())
	
		sqmail.utils.setsetting("usepicons", \
			self.widget.usepicons.get_active())

		sqmail.utils.setsetting("usepiconsproxy", \
			self.widget.usepiconsproxy.get_active())

		sqmail.utils.setsetting("omitpiconsuser", \
			self.widget.omitpiconsuser.get_active())

		sqmail.utils.setsetting("piconsserver", \
			self.widget.piconsserver.get_text())

		sqmail.utils.setsetting("piconsproxyserver", \
			self.widget.piconsproxyserver.get_text())

		sqmail.utils.setsetting("piconsproxyport", \
			int(self.widget.piconsproxyport.get_text()))

		# Miscellaneous

		sqmail.utils.setsetting("quoteprefix", \
			self.widget.quoteprefix.get_text())

		#sqmail.utils.setsetting("spamcommand", \
		#	self.widget.spamcommand.get_text())

	def on_changed(self, *args):
		self.widget.preferenceswin.set_modified(1)
	
	# Loads a new face into the specified object.

	def on_load_bitmap(self, obj):
		sqmail.gui.utils.FileSelector("Select new X-Face", "", self.on_load_bitmap_done, obj)
	
	def on_load_bitmap_done(self, filename, obj):
		if not sqmail.preferences.get_usexfaces():
			sqmail.gui.utils.errorbox("You don't have X-Faces enabled, so I'm unable to load a new face.")
			return
		if ((len(filename) < 4) or (filename[-4:] != ".xbm")):
			sqmail.gui.utils.errorbox("X-Faces must be 48x48 XBM files.")
			return

		encoder = sqmail.preferences.get_xfaceencoder()
		pipefp = os.popen(encoder % filename)
		f = string.join(pipefp.readlines(), "")
		if (f == ""):
			sqmail.gui.utils.errorbox("I was enable to encode the X-Face. See the error message on the console.")
			return

		sqmail.gui.utils.set_face(self.widget.outgoingxfaceicon, f)
		self.widget.preferenceswin.set_modified(1)

	# Flush the picons cache.

	def on_flushpicons(self, obj):
		sqmail.picons.flush()
		self.on_update_piconsstatus(None)

	# Update the picons status widget.

	def on_update_piconsstatus(self, obj):
		self.widget.piconsstatus.set_text("%d picons in cache" % sqmail.picons.get_picon_stats())

# Revision History
# $Log: preferences.py,v $
# Revision 1.12  2001/04/19 14:56:53  dtrg
# Added support for using domain names only for picons. This means that all
# hotmail users share the same picon, for example; this reduces the number
# of lookups, but means you don't get personalised picons.
#
# Revision 1.11  2001/03/12 14:28:38  dtrg
# Added the ability to disable X-Faces completely, as they weren't working
# for some people (even with the code to detect if the decoding was
# failing). Still needs a bit of cosmetic work --- it would be nice to grey
# out preferences GUI elements that aren't valid when they're disabled ---
# but it works.
#
# Revision 1.10  2001/03/09 20:36:19  dtrg
# First draft picons support.
#
# Revision 1.9  2001/03/07 12:21:21  dtrg
# Now tests for the X-Face encoder and decoder commands failing, and no
# longer seg faults.
#
# Revision 1.8  2001/03/05 20:44:41  dtrg
# Lots of changes.
# * Added outgoing X-Face support (relies on netppm and compface).
# * Rearrange the FileSelector code now I understand about bound and unbound
# method calls.
# * Put in a workaround for the MimeReader bug, so that when given a message
# that triggers it, it fails cleanly and presents the user with the
# undecoded message rather than eating all the core and locking the system.
# * Put some sanity checking in VFolder so that attempts to access unknown
# vfolders are trapped cleanly, rather than triggering the
# create-new-vfolder code and falling over in a heap.
#
# Revision 1.7  2001/02/20 17:22:36  dtrg
# Moved the bulk of the preference system out of the gui directory, where it
# doesn't belong. sqmail.gui.preferences still exists but it just contains
# the preferences editor. sqmail.preferences now contains the access
# functions and load/save functions.
#
# Revision 1.6  2001/02/20 15:46:00  dtrg
# Fixed a bug where the To: line on outgoing messages was, if mail aliases
# were being used, set to the unexpanded value (which would cause replies to
# the messages to be sent to bogus addresses).
#
# Revision 1.5  2001/02/02 20:03:01  dtrg
# Added mail alias and default domain support.
# Saves the size of the main window, but as yet doesn't set the size on
# startup.
#
# Revision 1.4  2001/01/25 20:55:06  dtrg
# Woohoo! Vfolder styling now works (mostly, except backgrounds). Also added
# background vfolder counting to avoid that nasty delay on startup or
# whenever you fetch new mail.
#
# Revision 1.3  2001/01/22 18:31:55  dtrg
# Assorted changes, comprising:
#
# * Added a new pane to the notebook display containing the entire, un
# MIMEified message. I was originally going to display just the headers and
# then optionally the body when the user pressed a button, but it seems to
# be decently fast without it.
# * The first half of the Spamcop support. Now, pressing the Spam button
# causes a compose window to appear all ready to send. The second half, that
# will deal automatically with the automated replies from Spamcop, has yet
# to be done.
# * Yet another rehash of the vfolder colour code. Still doesn't work.
#
# Revision 1.2  2001/01/18 19:27:07  dtrg
# Now saves the colours for read and unread vfolders.
#
# Revision 1.1  2001/01/05 17:27:48  dtrg
# Initial version.
#


