import logging
from mailbox import Message as Rfc2822

from caliop.helpers.format import clean_email_address
from caliop.core.user import User


log = logging.getLogger(__name__)


class MdaMessage(object):

    recipient_headers = ['To', 'Cc', 'Bcc', 'X-Original-To']

    def __init__(self, raw):
        try:
            self.mail = Rfc2822(raw)
        except Exception, exc:
            log.error('Parse message failed %s' % exc)
            raise
        # Get recipients
        addrs = []
        for header in self.recipient_headers:
            if self.mail.get(header):
                if ',' in self.mail.get(header):
                    addrs.extend(self.mail.get(header).split(','))
                else:
                    addrs.append(self.mail.get(header))
        self.recipients = [clean_email_address(x) for x in addrs]
        self.from_ = clean_email_address(self.mail.get('From'))
        self.users = self._resolve_users()
        if self.users:
            self.parts = self._extract_parts()
        else:
            self.parts = []

    def all_recipients(self):
        return self.recipients + [self.from_]

    def _resolve_users(self):
        """Find all users involved in this mail"""
        find_users = []
        for addr in self.recipients:
            try:
                user = User.get(addr)
                if not user in find_users:
                    find_users.append(user)
            except:
                # XXX handle NotFound only
                pass
        return find_users

    def _extract_parts(self):
        """Multipart message, extract parts"""
        if not self.mail.is_multipart():
            return []
        parts = []
        for p in self.mail.walk():
            if not p.is_multipart():
                parts.append(p)
        return parts
