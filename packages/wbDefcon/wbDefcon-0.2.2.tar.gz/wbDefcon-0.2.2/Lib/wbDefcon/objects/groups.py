"""
groups
===============================================================================
"""
import defcon

def sortedGroupNamesFactory(groups):
    groupNames = list(groups.keys())
    groupNames.sort()
    return groupNames

class Groups(defcon.Groups):

    @property
    def sortedGroupNames(self):
        return self.getRepresentation("sortedGroupNames")

    @classmethod
    def fromUFOlib2_Groups(cls, font, ufolib2_groups):
        groups = cls(font)
        groups.disableNotifications()
        groups.update(ufolib2_groups)
        groups.enableNotifications()
        return groups

defcon.registerRepresentationFactory(
    Groups,
    "sortedGroupNames",
    sortedGroupNamesFactory,
    destructiveNotifications=("Groups.Changed", ),
)
