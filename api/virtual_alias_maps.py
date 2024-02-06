from pydantic import BaseModel
import utils.storage as storage
import postfix


#########################################################################################
# Models
#########################################################################################
class VirtualAliasMaps(BaseModel):
    source: str
    destination: str
    
    def to_string(self):
        return "{source} {destination}".format(
            source = self.source,
            destination = self.destination
        )

#########################################################################################
# Utilities
#########################################################################################
def _store_virtual_alias_maps():
    '''
    Writes the virtual alias map into the file, then regenerates the hash map and
    reloads the postfix
    '''
    with open(storage.get_virtual_alias_maps_path(), 'w') as virtual_alias_maps_file:
        for virtual_alias_map in virtual_alias_maps_file:
            virtual_alias_maps_file.write(virtual_alias_map.to_string())
            virtual_alias_maps_file.write('\n')
    postfix.postmap(storage.get_virtual_alias_maps_path())
    postfix.restart()
    return True
    
def _load_virtual_alias_maps():
    '''
    Loads the list of virtual alias maps from the file
    '''
    result = []
    with open(storage.get_virtual_alias_maps_path()) as virtual_alias_maps_file:
        for line in virtual_alias_maps_file:
            if len(line):
                items = line.split()
                result.append(VirtualAliasMaps(
                    source = items[0],
                    destination = items[1]
                    ))
    return result


#########################################################################################
# API
#########################################################################################
def get_virtual_alias_maps():
    return _load_virtual_alias_maps()

def add_virtual_alias_map(virtual_alias_map):
    virtual_alias_maps = _load_virtual_alias_maps()
    virtual_alias_maps.append(virtual_alias_map)
    return _store_virtual_alias_maps(virtual_alias_maps)

def remove_virtual_alias_map(virtual_alias_map):
    virtual_alias_maps = _load_virtual_alias_maps()
    virtual_alias_maps.remove(virtual_alias_map)
    return _store_virtual_alias_maps(virtual_alias_maps)
