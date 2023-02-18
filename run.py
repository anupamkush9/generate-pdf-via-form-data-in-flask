from flask import Flask, request, current_app
import os
from weasyprint import HTML
app = Flask(__name__)
from jinja2 import Template



app.config["STATIC_FILE_PATH"] = "static"


@app.route("/", methods =["POST"])
def hello_world():
    if request.method == "POST":
        request_data = request.get_json()
        context = {}
        first_name = request_data.get("first_name")
        last_name = request_data.get("last_name")
        DOB = request_data.get("DOB")
        Gender = request_data.get("Gender")
        skills = request_data.get("skills")
        context["first_name"] = first_name
        context["last_name"] = last_name
        context["DOB"] = DOB
        context["Gender"] = Gender
        context["skills"] = skills


        #logic for pdf conversion
        with open(os.getcwd()+"/templates/converter.html") as file:
            template = Template(file.read())

            html_output = template.render(context)
            file_name = f'{context.get("first_name")}-{context.get("last_name")}'\
                        f'-{context.get("DOB")}-{context.get("Gender")}.pdf'
            pdf_data = HTML(string=html_output)
            pdf_data_str = pdf_data.write_pdf()

            # Storing PDF to Local storage
            local_pdf_url = current_app.config['STATIC_FILE_PATH'] + '/' + file_name
            file = open(local_pdf_url, 'wb')
            file.write(pdf_data_str)
            file.close()
            print("PDF uploaded to local file : ", local_pdf_url)
    return {"PDF uploaded to local file" : local_pdf_url.split("/")[1]}

if __name__ == "__main__":
	app.run(debug = True)
    