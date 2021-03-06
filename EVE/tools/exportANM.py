'''
Export CHARACTER animation data from animation scene

Currently only builds cache network for  ROMA character. Need to run file caching manually
'''

import hou
from EVE.dna import dna
reload(dna)

characterName = 'ROMA'
CHARACTERS = hou.node('/obj/{0}'.format(dna.charactersContainer))

def getRenderNode(container):
    '''
    Get and return node with render flag inside <container> node
    :param container:
    :return:
    '''

    for node in container.children():
        if node.isRenderFlagSet() == 1:
            return node

def createCacheNetwork():
    '''
    Create output character nodes for exporting cache from animation scene

    :return:
    '''
    renderNode = getRenderNode(CHARACTERS)

    # Create Cache node
    cache = CHARACTERS.createNode('filecache', 'CACHE_{}'.format(characterName))

    # Build path to a file cache
    pathCache = dna.buildFliePath('001',
                                   dna.fileTypes['cacheAnim'],
                                   scenePath=hou.hipFile.path(),
                                   characterName=characterName)

    # Setup FileCacheSOP and other nodes
    cache.parm('file').set(pathCache)
    cache.parm('loadfromdisk').set(1)
    null = CHARACTERS.createNode('null', 'OUT_{}'.format(characterName))
    cache.setInput(0, renderNode)
    null.setInput(0, cache)
    null.setDisplayFlag(1)
    null.setRenderFlag(1)
    CHARACTERS.layoutChildren()

def run():
    createCacheNetwork()