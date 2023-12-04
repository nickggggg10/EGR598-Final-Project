#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nickgiusti
Final Project
Gui for meal planning
"""

import PySimpleGUI as psg
import json
import random
import pandas as pd

# Load associations file as a dictionary
with open('mealAssociations.json', 'r') as jsonfile:
    data = json.load(jsonfile)

# Create pandas dataframe with the loaded associations
df = pd.DataFrame(data).T

# color theme
psg.theme('Kayak')

# lists of options for each meal category used in the dropdowns
mainList = ['Grilled chicken','Chicken tenders','Steak','Pork chops','Carne asada',
            'Meatballs','Salmon','Sausage','Shrimp','Tofu']

carbList = ['Mashed Potatoes','Mac and cheese','Pasta (red sauce)','Pasta (Alfredo)',
            'White rice','Brown rice','French fries','Black beans','Baked beans']

veggList = ['Mixed veggies','Salad','Broccoli','Mushrooms','Brussel sprouts','Asparagus',
            'Green beans','Peas','Grilled peppers']

# layout of the visual aspect of the GUI
layout = [
            # welcome text and instructions
            [psg.Text('Welcome to the Meal Planner Application', font = ('Arial',25))],
            [psg.Text('For each category, either select from the dropdown or check "Choose for me"', font = ('Arial',18))],
            
            # dropdowwn menus and check boxes for 'Choose for me' for each meal category
            [psg.Text('What would you like for your main course?', size=(35, 1)),
            psg.DropDown(mainList, size=(30, len(mainList))), psg.Checkbox('Choose for me', key='checkMain')],
    
            [psg.Text('What would you like for your carbs?', size=(35, 1)),
             psg.DropDown(carbList, size=(30, len(carbList))), psg.Checkbox('Choose for me', key='checkCarb')],
    
            [psg.Text('What would you like for your veggies?', size=(35, 1)),
             psg.DropDown(veggList, size=(30, len(veggList))), psg.Checkbox('Choose for me', key='checkVegg')],
    
            # generatemeal event button
            [psg.Text('Press below to generate meal', font = ('Arial',12))],

            [psg.Button('Generate Meal')],
            
            [psg.Text('Press again to regenerate meal', font = ('Arial',12))],
            
            # output back to user after generating meal combination
            [psg.Text('                      ', key='mainKey', size=(40, 1), font = ('Arial',18), justification='center')],
            [psg.Text('Results will show here', key='carbKey', size=(40, 1), font = ('Arial',18), justification='center')],
            [psg.Text('                      ', key='veggKey', size=(40, 1), font = ('Arial',18), justification='center')],
            
            # close the program
            [psg.Button('Close')]

        ]

# creating the window based off of the layout
window = psg.Window('Meal Planning', layout, element_justification='center')

# while loop for processing user events in the GUI window
while True:
    event, values = window.read()
    
    # if user closes window, stop running program loop
    if event == psg.WIN_CLOSED or event == 'Close':
        break
    
    # when user presses generate, interpret their inputs for each meal category
    if event == 'Generate Meal':
        
        # if user checks 'Choose for me', that is their selection, otherwise it follows the dropdown input
        selectedMain = 'Choose for me' if values['checkMain'] else values[0]
        selectedMain = 'Not selected' if selectedMain == '' else selectedMain
    
        selectedCarb = 'Choose for me' if values['checkCarb'] else values[1]
        selectedCarb = 'Not selected' if selectedCarb == '' else selectedCarb

        selectedVegg = 'Choose for me' if values['checkVegg'] else values[2]
        selectedVegg = 'Not selected' if selectedVegg == '' else selectedVegg
        
        # if user wants to generate the main course, make random choice from dataframe options
        if selectedMain == 'Choose for me':
            selectedMain = random.choice(list(df.index))
            
            # if user chose carb or veggie, update dataframe to only include meal combos that are associated with selections
            # inclusive of both selections, or solo selection, whatever the user inputted
            if selectedCarb != 'Choose for me' or selectedVegg != 'Choose for me':
                filteredDF = df[
                    (df['carbs'].apply(lambda x: selectedCarb in x)) | 
                    (df['veggies'].apply(lambda x: selectedVegg in x))
                ]
                
                # reselect the main course option randomly based on the updated filtered dataframe
                if not filteredDF.empty:
                    selectedMain = random.choice(filteredDF.index)
        
        # generate remaining carb and veggie options (randomly) based off of main course selection
        if selectedMain in df.index:
            associatedCarb = random.choice(df.loc[selectedMain, 'carbs']) if not df.loc[selectedMain, 'carbs'] == 'Not selected' else 'Not selected'
            associatedVegg = random.choice(df.loc[selectedMain, 'veggies']) if not df.loc[selectedMain, 'veggies'] == 'Not selected' else 'Not selected'
        else:
            pass
        
        # output text telling the user the suggested/user-defined meal combination options
        mainText = f"Suggested Main Course: {selectedMain}" if selectedMain == 'Choose for me' else f"Main Course: {selectedMain}"
        carbText = f"Suggested Carbs: {associatedCarb}" if selectedCarb == 'Choose for me' else f"Carbs: {selectedCarb}"
        veggText = f"Suggested Veggies: {associatedVegg}" if selectedVegg == 'Choose for me' else f"Veggies: {selectedVegg}"
        
        # update the window to display the text generated in previous block
        window['mainKey'].update(mainText)
        window['carbKey'].update(carbText)
        window['veggKey'].update(veggText)
        
# close window when program loop stops running
window.close()













