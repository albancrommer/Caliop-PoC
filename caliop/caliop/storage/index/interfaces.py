from zope.interface import Interface, Attribute


class _IIndexed(Interface):
    """Base interface for indexed objects"""

    type = Attribute("String that represent the type. "
                     "Must be unique per indexed type")
    columns = Attribute("List of columns to index")

    def __init__(self, data):
        """ Prepare data to be indexed """

    #@classmethod
    def get(cls, user_id, uid):
        """
        Retrieve the indexed object for the given object that have the given
        identifier.
        """

    def refresh(self):
        """
        Reload the object from the index
        """

    def update(self, query):
        """
        Update the object in the index
        """

    #@classmethod
    def create(cls, user_id, id, data):
        """
        Create the object in the index, dict format
        """

    #@classmethod
    def create_index(cls, user_id, id, idx_object):
        """
        Create the object in the index, object format
        """

    #@classmethod
    def filter(cls, user_id, params, order=None, limit=None):
        """
        Return a list of indexed object that match the given parameter
        """

    def to_dict(self):
        """
        Export indexed object as a dict
        """


class IUserIndex(_IIndexed):
    """Only here to manage user index globally (create, delete)"""

    #@classmethod
    def create(cls, user):
        """
         Create an index for the user
        """


class IMailIndexMessage(_IIndexed):
    """Get a user message object, and parse it to make an index"""

    def __init__(self, message, thread_id, message_id, answer_to, offset):
        """
         Create the main index message from the given id
        """


class _ITagMixin(_IIndexed):

    def add_tag(self, tag):
        """
        Add the given tag to self
        """

    def remove_tag(self, tag):
        """
        Remove the given tag to self
        """

    def set_tags(self, tags):
        """
        Replace the given list of tag to self
        """


class IIndexedMessage(_IIndexed):
    """Message from index server with helpers methods"""


class IIndexedContact(_IIndexed):
    """Contact from index server with helpers methods"""

    def __init__(self, data):
        """

        """

class IIndexedThread(_IIndexed):
    """Thread from index server"""
