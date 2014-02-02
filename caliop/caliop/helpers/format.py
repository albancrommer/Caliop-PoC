from email.utils import parseaddr


def clean_email_address(addr):
    """Clean an email address for user resolve"""
    real_name, email = parseaddr(addr)
    if not email:
        raise Exception('Invalid email address %s' % addr)
    name, domain = email.lower().split('@', 2)
    if '+' in name:
        name, ext = name.split('+', 2)
    # unicode everywhere
    return u'%s@%s' % (name, domain)
