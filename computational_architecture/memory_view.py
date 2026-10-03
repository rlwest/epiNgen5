"""Reusable dot access with copying at selected locations or a whole chunk level.

A NOTE ON RETRIEVAL AND UTILITY WHEN STORING CHUNKS
EpiEngine's exact and partial retrieval functions intentionally leave the
'utility' slot out of the returned chunk. This is not lost data or a copying
error: utility is treated as subsymbolic information used by the retrieval
mechanism, not as symbolic content made available to productions in the
retrieved buffer. The stored source chunk retains its utility.

Consequently, copying a retrieved or edited buffer chunk back into declarative
memory does not restore its original utility. The model's storage operation
must explicitly choose and attach the utility for the stored chunk, according
to the architecture's policy. Do this as part of storage, rather than exposing
utility as a slot in the retrieved buffer. Do not assume copying automatically
strengthens a chunk, merges it, or supplies a suitable default utility.

This is a retrieval/storage convention, separate from the memory-view mechanism.
MemoryView itself neither hides utility nor assigns it: it copies the contents
it is given. Directly copying a stored chunk that includes utility would also
copy that slot, so use the retrieval functions for the intended separation.
This reminder is kept here to make the full retrieve-edit-store sequence clear.

WHY THIS TEMPLATE COPIES WHOLE CHUNKS
Ordinary Python dictionary assignment shares an object; it does not make a
copy. For example, with a plain dictionary (not our MemoryView):
    world = {'bread1': {'location': 'counter'}}
    world['bread2'] = world['bread1']
    world['bread1']['location'] = 'plate'
Now BOTH names show location='plate', because they refer to one dictionary.
A production checking bread2 could therefore fire even though no action
explicitly moved bread2. Shared references are useful when two names are
intended to identify one object, but that is not the default intention for
separate chunks or environmental objects in this teaching template.

Our original sandwich examples avoided this issue by constructing each
ingredient with a separate dictionary literal:
    world['bread1'] = {'location': 'counter'}
    world['bread2'] = {'location': 'counter'}
Each literal creates a new dictionary. Later assigning one existing chunk to
another location can introduce sharing again when using plain dictionaries.
Python can also copy explicitly, for example with copy.deepcopy().

The template's whole-chunk copying policy makes independent contents the
default, including when assigning an existing chunk. It applies through BOTH
dots and brackets: the behavior comes from MemoryView's configured policy,
not from the punctuation. Ordinary slot edits still change the current chunk.

This is consistent with ACT-R's buffer-copying principle: a buffer receives a
copy of a chunk, and edits to that buffer's chunk leave the original unchanged.
It supports the cognitive interpretation of retrieving information and working
on a local copy. Our use of deep copies and extension of
the same rule to environmental objects are EpiEngine design choices, not a
complete implementation of ACT-R's copying or memory-learning mechanisms.
Source: ACT-R reference manual, Buffers section:
https://act-r.psy.cmu.edu/actr7.x/reference-manual.pdf#page=60

A NOTE FOR STUDENTS: THE DICTIONARY, THE VIEW, AND THE COPY
A dictionary holds the model's information. A view is a separate Python object
that points to that dictionary and lets you access it with dots or brackets.
Reading through a view does not copy the dictionary. Editing a slot through
that view changes the dictionary it points to.

Whole-chunk assignment is different. In our dot-enabled God Mode template,
all chunks at the buffer/object level are configured to copy on assignment:
    environment.bread2 = environment.bread1
This makes an independent dictionary for bread2, initially with the same
contents as bread1. It is a different object even before any values change.
The copy includes nested dictionaries and lists, so editing the copy leaves
its source unchanged. Accessing bread2 through dots gives you a view of that
new dictionary:
    environment.bread2.location = 'plate'
This edits a slot in bread2; it does not move bread1 or copy bread2 again.

In contrast, saving a view in an ordinary Python variable does not copy:
    selected = environment.bread1
    selected.location = 'plate'
Here selected points to a view of bread1, so the edit changes bread1 itself.
The copying rule belongs to assignment into a configured memory location,
not to dot notation alone. Other architectures can choose different policies.

Python distinguishes identity (which object?) from equality (same contents?).
A copied dictionary has its own identity. The view also has an identity of its
own; id(view) identifies the wrapper, not the dictionary it points to. You do
not need either identifier to work with memories: use their model paths.

This computational mechanism does not choose a cognitive architecture. It
creates no global memories, registers no buffers automatically, and prints
nothing on import. An architecture template chooses the structure and copying locations.
It neither enforces access permissions nor separates symbolic/subsymbolic
processes, merges chunks, or changes activation.

Example for an architecture author:
    memories = MemoryView({'perception': {'buffers': {}}, 'environment': {}})
    register_buffer(memories.perception.buffers, 'visual', {'state': 'empty'})
    memories.perception.buffers.visual = {'state': 'seen'}  # copy whole chunk
    memories.perception.buffers.visual.state = 'attended'  # edit one slot

An architecture can instead apply one rule to every chunk, without registering
names individually:
    memories = MemoryView({'working_memory': {}, 'environment': {}},
                          copy_chunk_depth=2)
    memories.environment.bread1 = {'location': 'counter'}
    memories.environment.bread2 = memories.environment.bread1  # independent copy

Depth counts dictionary keys from the root: memory source is depth 1, and a
buffer/object/chunk is depth 2. New memory sources inherit the same rule.
Initial contents and whole memory-source assignments are prepared chunk by
chunk, so two locations supplied with the same source get independent copies.
Slot edits below the selected depth retain normal assignment behavior.

register_buffer takes the VIEW OF THE CONTAINING LOCATION and a buffer name.
The location may be the root or any nested dictionary view. Patterns remain
ordinary dictionaries; actions may use dots or brackets over the same data.

This is a MutableMapping view, not a dict subclass. Code requiring an actual
plain dict may need adaptation. Dictionary keys that are not Python attribute
names, that begin with '_', or that collide with methods (items, update, copy)
require brackets. Nested dictionaries get views when read through the mapping;
list elements are ordinary Python objects, not automatically wrapped views.

With no copy_chunk_depth, copying applies only at explicitly registered buffers.
With a depth selected, assignment at that depth copies each whole chunk;
assignment above it prepares the incoming structure using the same policy.
Both dots and brackets (including update()) follow these rules. Direct edits
to raw dictionaries bypass the view's policy: this is not access control.
Explicit registrations deeper than the selected level still apply when those
locations are assigned directly, not when an ancestor is replaced.
A view saved before replacement still refers to the old dictionary; obtain a
fresh view through the parent to access its replacement.
"""

# WHY AN ACCESS LAYER?
# EpiEngine already reads state using dictionary operations. We want students
# to write dots in actions without rewriting the engine or its pattern matcher.
# A "view" is an object that provides another way to access existing data;
# reading a nested view does not duplicate that data. The dictionaries remain the
# storage, while MemoryView translates access operations, not production rules.
# This is a mapping object, not a dict subclass: it supports dictionary-style
# operations, but isinstance(view, dict) would be False.
#
# MutableMapping is a Python base class for editable dictionary-like objects.
# After we supply the five basic methods below, it supplies methods such as
# get(), update(), keys(), items(), and values(). In particular, update() calls
# our __setitem__, so it follows the same buffer-copy rule as assignment.
# Leading underscores identify implementation helpers rather than student API.
from collections.abc import MutableMapping as _MutableMapping
from copy import deepcopy as _deepcopy

__all__ = ['MemoryView', 'register_buffer']


class MemoryView(_MutableMapping):
    """Connect dot notation and dictionary operations to one stored state.

    Python calls special methods (the double-underscore or "dunder" methods)
    in response to ordinary syntax. For example, view[key] calls __getitem__.
    self is the particular view receiving the operation.

    Each view remembers a dictionary, the shared set of registered buffer
    paths, and its own path from the outer memories dictionary. Paths identify
    where copying is required; they do not restrict which data can be accessed.
    """

    def __init__(self, data, *, copy_chunk_depth=None, _buffers=None, _path=()):
        """Create a view with an optional automatic copying level.

        MemoryView(data) keeps the original dictionary and needs explicit
        buffer registration for copying. copy_chunk_depth=2 creates independent
        initial chunks and applies that policy to future writes at the same
        level. Use a positive integer depth, or None for explicit registration.
        Internal arguments connect child views to the root's policy and paths.
        """
        if not isinstance(data, dict):
            raise TypeError('MemoryView requires a dictionary.')
        if copy_chunk_depth is not None:
            if (isinstance(copy_chunk_depth, bool) or
                    not isinstance(copy_chunk_depth, int) or copy_chunk_depth < 1):
                raise ValueError('copy_chunk_depth must be a positive integer or None.')
        if _buffers is None:
            _buffers = set()
        if not _path and copy_chunk_depth is not None:
            data = _copy_to_depth(data, copy_chunk_depth)
        # These are the view's own bookkeeping attributes, not model slots.
        # Calling object.__setattr__ directly bypasses our custom __setattr__;
        # otherwise initialization would be treated as a model-state update.
        object.__setattr__(self, '_data', data)
        object.__setattr__(self, '_buffers', _buffers)
        object.__setattr__(self, '_path', _path)
        object.__setattr__(self, '_copy_chunk_depth', copy_chunk_depth)

    # DICTIONARY OPERATIONS: the common foundation for the engine and dots.
    def __getitem__(self, key):
        """Handle view[key], returning a nested view or the stored slot value."""
        value = self._data[key]
        if isinstance(value, dict):
            # Wrap on access, so dictionaries students add later also get dots.
            # (key,) is a one-element tuple; adding it extends this view's path.
            # For example: () -> ('working_memory',) ->
            # ('working_memory', 'focusbuffer'). All these views share data.
            return MemoryView(value, copy_chunk_depth=self._copy_chunk_depth,
                              _buffers=self._buffers,
                              _path=self._path + (key,))
        return value

    def __setitem__(self, key, value):
        """Assign an entry using the selected chunk level or explicit buffer rule."""
        # A source chunk might itself be a view, such as retrievalbuffer.
        # Unwrap it so we store its dictionary rather than its access wrapper.
        if isinstance(value, MemoryView):
            value = value._data
        # Assigning a chunk differs from editing a slot within that chunk.
        # For depth 2, working_memory.focusbuffer and environment.bread1 are
        # equivalent copying locations. No individual registration is needed.
        target_path = self._path + (key,)
        if self._copy_chunk_depth is not None and len(target_path) <= self._copy_chunk_depth:
            value = _copy_to_depth(value, self._copy_chunk_depth - len(target_path))
        elif target_path in self._buffers:
            if not isinstance(value, dict):
                raise TypeError('A registered buffer must contain a dictionary chunk.')
            # Deep copying also separates nested dictionaries and lists.
            # Editing the loaded chunk will not change those in its source.
            # This operation does not merge chunks or change their activation.
            value = _deepcopy(value)
        # Assigning here replaces just this entry. For whole-buffer replacement,
        # old slots disappear; for a slot edit, the other slots remain intact.
        self._data[key] = value

    def __delitem__(self, key):
        """Handle del view[key]; absent entries raise the usual KeyError."""
        # Deleting a buffer's contents entry does not unregister its name.
        # A later assignment to that registered path will still copy.
        del self._data[key]

    def __iter__(self):
        """Let 'for key in view' visit dictionary keys without copying them."""
        return iter(self._data)

    def __len__(self):
        """Let len(view) count its entries (also used for empty/nonempty checks)."""
        return len(self._data)

    # DOT OPERATIONS: delegate to the dictionary methods above so the two
    # spellings cannot accidentally update separate versions of model state.
    def __getattr__(self, name):
        """Resolve view.name when Python finds no ordinary attribute named name."""
        # Existing methods, such as items and update, are found before this
        # function runs. A model key with one of those names needs brackets.
        if name.startswith('_'):
            raise AttributeError(name)
        try:
            return self[name]
        except KeyError:
            # Dots conventionally report AttributeError, brackets KeyError.
            # Do not silently create missing data: a typo should be visible.
            # !r quotes the name; 'from None' hides the internal KeyError trace.
            raise AttributeError(f'No memory, buffer, or slot named {name!r}.') from None

    def __setattr__(self, name, value):
        """Handle view.name = value by using the same rules as view[name] = value."""
        # Reserve bookkeeping and method names. Brackets still allow those
        # names as dictionary keys without replacing the view's own machinery.
        if name.startswith('_') or hasattr(type(self), name):
            raise AttributeError(f'Use brackets for the reserved name {name!r}.')
        self[name] = value

    def __delattr__(self, name):
        """Handle del view.name, protecting methods and reporting missing names."""
        if name.startswith('_') or hasattr(type(self), name):
            raise AttributeError(f'Use brackets for the reserved name {name!r}.')
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name) from None

    # DISPLAY AND COPYING: keep views useful with familiar Python tools.
    def __repr__(self):
        """Display the stored dictionary when printing or inspecting a view."""
        return repr(self._data)

    def copy(self):
        """Return a shallow dictionary copy, like dict.copy().

        The outer dictionary is new, but nested mutable contents remain shared.
        This differs from the deep copy used when loading a registered buffer.
        """
        return self._data.copy()

    def __deepcopy__(self, memo):
        """Make deepcopy(view) return independent data, not a copied wrapper."""
        # Python supplies memo to track objects it has already copied. Passing
        # it along preserves internal shared relationships and handles cycles.
        return _deepcopy(self._data, memo)


def _copy_to_depth(value, remaining):
    """Prepare incoming dictionaries, copying each chunk independently.

    remaining counts levels before the chosen chunk boundary. At that boundary
    deepcopy separates nested dictionaries and lists from the source. Above
    it, build a dictionary entry by entry: one deepcopy of the entire memory
    would preserve shared references BETWEEN chunks, which we want to separate.
    This function does not mutate the source, so invalid input leaves state
    unchanged. A view source is unwrapped to copy its underlying dictionary.
    """
    if isinstance(value, MemoryView):
        value = value._data
    if not isinstance(value, dict):
        raise TypeError('Memory sources and whole chunks must be dictionaries.')
    if remaining == 0:
        return _deepcopy(value)
    return {key: _copy_to_depth(child, remaining - 1)
            for key, child in value.items()}


# REGISTERING A COPYING POLICY
# Registration belongs to this reusable mechanism, but the caller chooses the
# location. Nothing here assumes a name such as working_memory or focusbuffer.
def register_buffer(location, name, chunk=None):
    """Register a buffer under location and load an independent copy of a chunk.

    location must be a MemoryView of the containing dictionary. name is the
    new or existing buffer key. With chunk=None, use the current contents, or
    an empty dictionary if the buffer does not exist. Return its buffer view.
    Re-registering a buffer copies its contents again without adding duplicates.

    Example: register_buffer(memories.agent.buffers, 'goal', {'state': 'start'})
    Subsequent assignment to memories.agent.buffers.goal copies a whole chunk.
    Other locations, even with the same buffer name, are unaffected.
    """
    if not isinstance(location, MemoryView):
        raise TypeError('The buffer location must be a MemoryView.')
    if not isinstance(name, str) or not name:
        raise ValueError('A buffer name must be a nonempty string.')
    if chunk is None:
        chunk = location.get(name, {})
    if isinstance(chunk, MemoryView):
        chunk = chunk._data
    if not isinstance(chunk, dict):
        raise TypeError('A buffer must contain a dictionary chunk.')
    # Prepare the independent contents before changing either state or policy.
    # If copying fails, registration leaves the original location untouched.
    copied_chunk = _deepcopy(chunk)
    location._buffers.add(location._path + (name,))
    # The copy is already prepared; store directly to avoid copying it twice.
    location._data[name] = copied_chunk
    return location[name]
