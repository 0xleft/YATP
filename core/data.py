import base64
import copy
import os

import json
from requests import post
from docx import Document
from docx.shared import Pt

from core.util import downscale_image
import eel

# TODO REDO THIS ENTIRE THING ITS DAMN UGLY
class ProblemImage:
    def __init__(self, image_path, description):
        self.image_path = image_path
        self.description = description

    def __str__(self):
        return f'Image path: {self.image_path}\nDescription: {self.description}'


# the converter class that holds references to all images and converts them later into a nice table in word
def make_images_smaller(path):
    try:
        os.mkdir(path + "/small")
    except FileExistsError:
        pass

    for file in os.listdir(path):
        if file.endswith(".jpg") or file.endswith(".png"):
            downscale_image(path + "/" + file, path + "/small/small_" + file, 700)


class Converter:
    def __init__(self):
        self.doc = Document()
        self.images = []


    def load_images(self, path):
        self.images = []
        for file in os.listdir(path):
            if file.endswith(".jpg") or file.endswith(".png"):
                try:
                    self.images.append(ProblemImage(path + "/" + file, ''))
                except Exception as e:
                    eel.show_notification(f"Error loading image {file}: {e}")

        print(self.images)

    def get_image_src(self, index):
        with open(self.images[index].image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        image_format = "png"
        if self.images[index].image_path.endswith(".jpg"):
            image_format = "jpeg"
        return f"data:image/{image_format};base64,{encoded_string}"

    def open(self):
        self.doc.save('FILE_GENERATED_BY_YATP.docx')
        os.system('start FILE_GENERATED_BY_YATP.docx')

    def make_executive_summary(self, api_key):
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
                        headers={"Authorization": f"{api_key}", "Content-Type": "application/json"})

        if response.status_code != 200:
            eel.show_notification("Error", "Something went wrong while generating the executive summary. " + response.text)
            print(response.text)
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

    def convert_and_make_executive_summary(self, api_key):
        self.convert()
        self.make_executive_summary(api_key)

    def convert(self):
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
            eel.show_notification("Error", "Please close the file FILE_GENERATED_BY_YATP.docx")
            return

        self.doc = Document()

        to_remove = []
        for image in local_images:
            if image.description == '':
                print(f'No description for {image.image_path}')
                to_remove.append(image)

        # this is so it doesnt remove the   images while iterating
        for image in to_remove:
            local_images.remove(image)

        if len(local_images) == 0:
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
    def save_doc(self, path):
        self.convert()
        self.doc.save(path + '/FILE_GENERATED_BY_YATP.docx')

    # update description of the image
    def update_description(self, image_id, new_description):
        self.images[image_id].description = new_description
        print(self.images[image_id].description)
