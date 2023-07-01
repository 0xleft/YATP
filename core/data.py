import copy
import os

import json
from requests import post
from docx import Document
from docx.shared import Pt

def test_api_key(api_key):
    response = post("http://pageup.lt:8700/pleasegivetomeyes", data=json.dumps({
        "model": "gpt-3.5-turbo"
        , "messages": [{"role": "system", "content": "say something"}]}),
                    headers={"Authorization": f"{api_key}", "Content-Type": "application/json"})

    print(response.text)
    if 'error' in response.text:
        return False
    return True

class ProblemImage:
    def __init__(self, image_path, description):
        self.image_path = image_path
        self.description = description
        self.waiting_for_answer = False

    def __str__(self):
        return f'Image path: {self.image_path}\nDescription: {self.description}'


# the converter class that holds references to all images and converts them later into a nice table in word
class Converter:
    def __init__(self, images: list[ProblemImage], api_key=None):
        self.images = images
        self.api_key = api_key
        if api_key is not None:
            if api_key != 'skip':
                try:
                    if open('API_KEY').read().strip() != api_key:
                        open('API_KEY', 'w').write(api_key)
                except FileNotFoundError:
                    open('API_KEY', 'w').write(api_key)
        self.doc = Document()

    def open(self):
        self.doc.save('FILE_GENERATED_BY_YATP.docx')
        os.system('start FILE_GENERATED_BY_YATP.docx')

    def convert_and_open(self, gui):
        self.convert(gui)
        self.open()

    def make_executive_summary(self, gui):
        if self.api_key is None:
            gui.show_notification('No api key found', 1000)
            return

        photos = ""
        i = 0
        for image in self.images:
            i += 1
            if image.description == '':
                continue
            photos += f"P{i}: {image.description} \n"

        print(photos)

        response = post("http://pageup.lt:8700/pleasegivetomeyes", data=json.dumps({
            "model": "gpt-3.5-turbo"
            , "messages": [{"role": "system", "content": "You need to make an executive summary in english "
                                                         "referencing all the photos. The executive summary is about "
                                                         "a building site and what is wrong with the building site. "
                                                         "The what is wrong part is more important. After the summary "
                                                         "you need to make a list of things that were bad, "
                                                         "referencing the photos. You should only mention one issue "
                                                         "that is summary of a few photos and if the issue is not "
                                                         "associated with other issues you should mention it "
                                                         "differently. Just keep in mind that Idem means 'the same as "
                                                         "the last one'.  Do not use italian words. An executive "
                                                         "summary should be only  a short paragraph. Try to be as "
                                                         "concise as possible. DO NOT INCLUDE ANY DISCLAIMERS. Do not "
                                                         "say P1, P2 say Photo 1, Photo 2. Try to talk about issues "
                                                         "very shortly. Ok means good. Do not forget to list the "
                                                         "issues at the bottom. Smoking is not permitted on a "
                                                         "building site and should be treated as a separate issue. DO "
                                                         "NOT mention photos in the executive summary you should only "
                                                         "summarize the descriptions. Only the part where you list "
                                                         "should mention photos. If there are good things you should "
                                                         "also mention them in the summary. MENTION PHOTOS ONLY IN "
                                                         "THE LIST AND NOT IN THE PARAGRAPH. If one photo is idem "
                                                         "group it up the the last one. DO NOT MENTION PHOTOS THAT DO NOT EXIST."},
                           {"role": "user",
                            "content": f"Give executive summary "
                                       f"for the "
                                       f"following: "
                                       f"{photos}"}]}),
                        headers={"Authorization": f"{self.api_key}", "Content-Type": "application/json"})

        if response.status_code != 200:
            print(response.text)
            gui.show_notification('Error with api' + str(response.text), 5000)
            return

        response = response.json()
        print(response)
        response = response['choices'][0]['message']['content']
        self.doc.add_paragraph('')
        self.doc.add_paragraph('')
        self.doc.add_paragraph('')
        self.doc.add_paragraph('')
        self.doc.add_paragraph('')
        self.doc.add_paragraph('Recommended executive summary: ')
        self.doc.add_paragraph(response)
        self.doc.add_paragraph('')
        self.doc.add_paragraph('')

    def convert_and_make_executive_summary(self, gui):
        self.convert(gui)
        self.make_executive_summary(gui)
        self.open()

    def convert(self, gui):

        def add_cell_data(cell, index, image_path, description):
            paragraph = cell.paragraphs[0]
            run = paragraph.add_run()
            run.add_picture(image_path, width=Pt(300))

            cell_paragraph = cell.add_paragraph()
            cell_paragraph.add_run(f"Foto {index + 1}: {description}").bold = True

            cell_paragraph.style.font.size = Pt(12)

        local_images = copy.deepcopy(self.images)

        try:
            os.remove('FILE_GENERATED_BY_YATP.docx')
        except FileNotFoundError:
            pass
        except PermissionError:
            gui.show_notification('Please close the file before generating a new one.', 1000)
            return

        self.doc = Document()

        to_remove = []
        for image in local_images:
            if image.waiting_for_answer:
                gui.show_notification('Request has gone to the api wait for answer', 1000)
                return
            if image.description == '':
                print(f'No description for {image.image_path}')
                to_remove.append(image)

        # this is so it doesnt remove the   images while iterating
        for image in to_remove:
            local_images.remove(image)

        if len(local_images) == 0:
            gui.show_notification('No images have a description :/', 1000)
            return

        print(len(local_images))
        for i in range(0, len(local_images), 2):

            table = self.doc.add_table(rows=0, cols=2)
            table.style = 'Table Grid'

            try:
                row_data = local_images[i], local_images[i + 1]
            except IndexError:
                row_data = local_images[i], None
            row = table.add_row().cells

            add_cell_data(row[0], i, row_data[0].image_path, row_data[0].description)
            if row_data[1] is not None:
                add_cell_data(row[1], i + 1, row_data[1].image_path, row_data[1].description)

    # save document to the folder that we are curently taking images from
    def save_doc(self, path, gui):
        self.convert(gui)
        self.doc.save(path + '/FILE_GENERATED_BY_YATP.docx')
        gui.show_notification('File saved', 1000)

    # update description of the image
    def update_description(self, image_id, new_description):
        print(len(self.images))
        if self.images[image_id].waiting_for_answer:
            print('Waiting for answer')
            return
        self.images[image_id].description = new_description
        print(self.images[image_id].description)
