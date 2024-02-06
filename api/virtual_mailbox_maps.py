from pydantic import BaseModel
import utils.storage as storage
import postfix


#########################################################################################
# Models
#########################################################################################
class VirtualMailboxMaps(BaseModel):
    mailbox: str
    location: str
    
    def to_string(self):
        return "{mailbox} {location}".format(
            mailbox = self.mailbox,
            location = self.mailbox[self.mailbox.index("@") + 1:] + '/' + 
            self.mailbox[:self.mailbox.index("@")] + '/'
        )

#########################################################################################
# Utilities
#########################################################################################
def _store_virtual_mailbox_maps(virtual_mailbox_maps):
    '''
    Writes the virtual mailbox map into the file, then regenerates the hash map and
    reloads the postfix
    '''
    with open(storage.get_virtual_mailbox_maps_path(), 'w') as virtual_mailbox_maps_file:
        for virtual_mailbox_map in virtual_mailbox_maps:
            virtual_mailbox_maps_file.write(virtual_mailbox_map.to_string())
            virtual_mailbox_maps_file.write('\n')
    postfix.postmap(storage.get_virtual_mailbox_maps_path())
    postfix.restart()
    return True

def _load_virtual_mailbox_maps():
    '''
    Loads the list of virtual mailbox maps from the file
    '''
    result = []
    with open(storage.get_virtual_mailbox_maps_path()) as virtual_mailbox_maps_file:
        for line in virtual_mailbox_maps_file:
            if len(line):
                items = line.split()
                result.append(VirtualMailboxMaps(
                    mailbox = items[0],
                    location = items[1]
                    ))
    return result


#########################################################################################
# API
#########################################################################################
def get_virtual_mailbox_maps():
    return _load_virtual_mailbox_maps()

def add_virtual_mailbox_map(virtual_mailbox_map):
    virtual_mailbox_maps = _load_virtual_mailbox_maps()
    virtual_mailbox_maps.append(virtual_mailbox_map)
    return _store_virtual_mailbox_maps(virtual_mailbox_maps)

def remove_virtual_mailbox_map(virtual_mailbox_map):
    virtual_mailbox_maps = _load_virtual_mailbox_maps()
    virtual_mailbox_maps.remove(virtual_mailbox_map)
    return _store_virtual_mailbox_maps(virtual_mailbox_maps)
