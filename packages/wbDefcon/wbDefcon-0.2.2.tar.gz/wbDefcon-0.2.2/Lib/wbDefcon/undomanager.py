"""
undomanager
===============================================================================
"""
import logging

log = logging.getLogger(__name__)


class UndoManager:
    def __init__(self, parent):
        self.parent = parent
        self.destroyRepresentations = []
        self._undoStack = []
        self._redoStack = []
        self._do = False

    def __repr__(self):
        return "<UndoManager for %r>" % self.parent

    def saveState(self):
        data = self.parent.serialize()
        if not self._undoStack or data != self._undoStack[-1]:
            self._undoStack.append(data)

    def canUndo(self):
        return len(self._undoStack) > 0

    def undo(self):
        self._do = True
        self._redoStack.append(self.parent.serialize())
        self.parent.deserialize(self._undoStack.pop())
        for representation in self.destroyRepresentations:
            self.parent.destroyRepresentation(representation)
        self._do = False

    def canRedo(self):
        return len(self._redoStack) > 0

    def redo(self):
        self._do = True
        self._undoStack.append(self.parent.serialize())
        self.parent.deserialize(self._redoStack.pop())
        for representation in self.destroyRepresentations:
            self.parent.destroyRepresentation(representation)
        self._do = False

    def clear(self):
        self._undoStack = []
        self._redoStack = []

    def handleNotification(self, notification):
        if not self._do:
            if "WillBe" in notification.name or "WillChange" in notification.name:
                self.saveState()
                log.debug("UndoManager.handleNotification(%r)", notification)

