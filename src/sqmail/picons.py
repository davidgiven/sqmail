import os
import sqmail.utils
import sqmail.db
import sqmail.preferences
import urllib
import string
import cPickle
import cStringIO

# Return the picon for a particular email address, fetching it off the net if
# need be.

def get_picon_xpm(email):
	cursor = sqmail.db.cursor()

	# Is the email address in the database?

	cursor.execute("SELECT image FROM picons WHERE email='%s'" \
		% sqmail.db.escape(email))
	i = cursor.fetchone()
	if (i != None):
		fp = cStringIO.StringIO(i[0])
		return cPickle.load(fp)

	# No. Need to query the remote server. First set the proxy.

	if (sqmail.preferences.get_usepiconsproxy()):
		os.environ["http_proxy"] = "http://%s:%d" % \
			(sqmail.preferences.get_piconsproxyserver(), \
			sqmail.preferences.get_piconsproxyport())
		print os.environ["http_proxy"]
	else:
		try:
			del os.environ["http_proxy"]
		except KeyError:
			pass

	# Now open the HTTP connection and read in the image.

	i = string.find(email, "@")
	user = email[:i]
	host = email[i+1:]
	i = sqmail.preferences.get_piconsserver() + \
		"/" + host + "/" + user + \
		"/users+usenix+misc+domains+unknown/up/single/xpm"
	print "Picons: Fetching", i
	try:
		fp = urllib.urlopen(i)
	except IOError, e:
		print "Picons: I/O error:", e
		return None
	image = sqmail.utils.load_xpm(fp)
	if not image:
		print "Picons: I/O error: didn't understand reply from server"
		return None

	# Cache the image.

	fp = cStringIO.StringIO()
	cPickle.dump(image, fp)
	cursor.execute("INSERT INTO picons (email, image) VALUES ('%s', '%s')" \
		% (sqmail.db.escape(email), sqmail.db.escape(fp.getvalue())))
	return image

# Return statistics on the picon cache.

def get_picon_stats():
	cursor = sqmail.db.cursor()
	cursor.execute("SELECT COUNT(*) FROM picons")
	return int(cursor.fetchone()[0])

# Purge the cache.

def flush():
	cursor = sqmail.db.cursor()
	print "Flushing picons cache..."
	cursor.execute("TRUNCATE picons")
	print "Done."

