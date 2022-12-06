from random import choice
from typing import Any
import PySimpleGUI as sg
import requests, io
from PIL import Image 

sg.theme('BluePurple')

layout = [
    [sg.Text("card"), sg.InputText(key='-CARD-')],
    [sg.Text(key='-NAME-'),sg.Text(key="-ATTRIBUTE-")],
    [sg.Text(key='-LEVEL-')],
    [sg.Image(size=((300,300)), key='-IMAGE-')],
    [sg.Text(key='-RACE-'),sg.Text(key="-ARCH-")],
    [sg.Text(key='-DESCRIPTION-', auto_size_text=True)],
    [sg.Text(text="ATK" , key='-ATK-'), sg.Text(text="DEF" ,key='-DEF-')],
    [sg.Button("get card info", key='-SUBMIT-')],
]
 # no need to remove the name cause this will only be use once
URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php?name="

window = sg.Window("something", layout, size=(600,600))

def update_fields(data:Any):
    """updates the fields with the data gotten from the api

    Args:
        data (Any): de jsonified data

    """
    window['-NAME-'].update(value=data.get('name'))
    window['-ATTRIBUTE-'].update(value=data.get('attribute'))
    window['-LEVEL-'].update(value=data.get('level'))
    window['-RACE-'].update(value=data.get('race'))
    window['-ARCH-'].update(value=data.get('archetype'))

    window['-IMAGE-'].update(f"{data.get('name')}.png")
    window['-DESCRIPTION-'].update(value=data.get('desc'))
    window['-ATK-'].update(value=data.get('atk'))
    window['-DEF-'].update(value=data.get('def'))

def handle_image_operations(data:Any):
    """handles all operations related to images

    Args:
        data (Any): de jsonified data from the api
    """
    random_image= choice( data['card_images'])
    card_image  = requests.get(random_image['image_url'])
    image =Image.open(io.BytesIO(card_image.content)) 
    image.thumbnail((400, 400))
    image.save(f"{data.get('name')}.png")

while True:
    event, values = window.read()

    if event == "-SUBMIT-":
            res = requests.get(f"{URL}{values['-CARD-'].strip()}")
            
            if res.status_code == 200:
                res_json = res.json()
                handle_image_operations(res_json['data'][0])

                update_fields(res_json['data'][0])

            else:
                window['-NAME-'].update(value="Card doesn't exist. . .")

    # run away . . . save ur souuul . . run away .. run forever more~!
    if event == sg.WIN_CLOSED:
        print("farewell~!")
        break

