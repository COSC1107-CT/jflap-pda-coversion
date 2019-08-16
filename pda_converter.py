from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

import os
import xml.etree.ElementTree as ET
import argparse


FINAL_STATE_NAME = 'qnf'
FINAL_STATE_ID_INCREMENT = 1
FINAL_STATE_X_INCREMENT = 100
FINAL_STATE_Y_INCREMENT = 100


def get_new_final_state_attr(states):
    highest_id = 0
    highest_x = 0
    highest_y = 0
    for s in states:
        id = int(s.attrib["id"])
        x = float(s.find('x').text)
        y = float(s.find('y').text)
        highest_id = max(id,highest_id)
        highest_x = max(highest_x, x)
        highest_y = max(highest_y, y)

    return (
        highest_id + FINAL_STATE_ID_INCREMENT,
        FINAL_STATE_NAME,
        highest_x + FINAL_STATE_X_INCREMENT,
        highest_y + FINAL_STATE_Y_INCREMENT
    )



"""
Code to convert the PDA.
"""
def convert_pda(pda_in_path, pda_out_path):

    #Load the XML and go into root-->automaton
    tree = ET.parse(pda_in_path)
    root = tree.getroot()
    automaton = root.find('automaton')


    states = automaton.findall('state')

    # Get a list of the ids of the existing final states so that they can be linked
    # To the new final state once it is created.
    old_final_state_ids = [x.attrib['id'] for x in states if x.find('final') is not None]

    # Compute the properties of the new final state
    id, name, x, y = get_new_final_state_attr(states) #The ID of the new final state

    #-----------------------------------------------------------------------------------------
    # MUTATION OF THE IN MEMORY XML TREE STARTS HERE. ALL READ SHOULD BE DONE ABOVE THIS
    #-----------------------------------------------------------------------------------------
    # Mark all old final states as non final.
    for s in states:
        f = s.find('final')
        if f is not None:
            s.remove(f)

    #Create a new final state with the properties computed above
    newState = ET.Element('state')
    newState.set('id', str(id))
    newState.set('name', name)
    ET.SubElement(newState, 'x').text = str(x)
    ET.SubElement(newState, 'y').text = str(y)
    ET.SubElement(newState, 'final')
    automaton.append(newState)

    #For each old final state, create the transition lambda, Z, lambda
    for i in old_final_state_ids:
        transition = ET.Element('transition')
        ET.SubElement(transition, 'from').text = str(i)
        ET.SubElement(transition, 'to').text = str(id)
        ET.SubElement(transition, 'read')
        ET.SubElement(transition, 'pop').text = 'Z'
        ET.SubElement(transition, 'push')
        automaton.append(transition)

    #Output the file to the out path
    tree.write(pda_out_path)

def main():
    parser = argparse.ArgumentParser(
        description= 'Convert a PDA with Final States to a PDA with only one new final state and \n'
                     'additional transitions lambda, Z, lambda from all previous final states to \n'
                     'that new final state.'
                     'Note it does NOT check the encoding of the files or their types (text or JFLAP).'
    )
    parser.add_argument('pda-in',
                        help='.jff file containing the PDA to be converted')
    parser.add_argument('pda-out',
                        help='.jff file this script will output to')

    pda_in_path = vars(parser.parse_args())['pda-in']
    pda_out_path = vars(parser.parse_args())['pda-out']
    if not os.path.isfile(pda_in_path):
        print("\n FILE '{}' NOT FOUND. The file does not seem to exist. Please double check.".format(pda_in_path))
        sys.exit(2)

    convert_pda(pda_in_path, pda_out_path)


if __name__ == "__main__":
    main()