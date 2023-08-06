class EntityStorageException(Exception):
	"""docstring for EntityStorageException"""
	def __init__(self, *args, **kwargs):
		super(EntityStorageException, self).__init__(*args, **kwargs)

class EntitySnapshotException(Exception):
	"""docstring for EntitySnapshotException"""
	def __init__(self, *args, **kwargs):
		super(EntitySnapshotException, self).__init__(*args, **kwargs)

class EntityQueringException(Exception):
	"""docstring for EntityQueringException"""
	def __init__(self, *args, **kwargs):
		super(EntityQueringException, self).__init__(*args, **kwargs)

class EntityRelationException(Exception):
	"""docstring for EntityRelationException"""
	def __init__(self, *args, **kwargs):
		super(EntityRelationException, self).__init__(*args, **kwargs)