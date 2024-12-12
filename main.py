from flask import Flask, request, render_template
from keras.models import load_model
from res import get_class
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'Entorns')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Función para verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Función personalizada para limpiar el nombre de archivo
def clean_filename(filename):
    # Eliminar caracteres especiales y espacios
    import re
    return re.sub(r'[^\w\-]+', '_', filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file and allowed_file(file.filename):
            class_names = ["Mal entorno de aire", "Mal entorno de basura", "deforestación", "sequia", "Mal entorno de agua contaminada", "Regular contaminación del aire", "Regular entorno de basura", "Regular entorno de agua contaminada", "Buen entorno de aire", "Buen entorno de agua", "Buen entorno de suelo"]
            model = load_model('keras_model.h5')
            # Limpiar el nombre de archivo
            filename = clean_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            # Clasificar la imagen usando tu función get_class
            class_name, confidence_score = get_class(model, class_names, filepath)
            if class_name == "Mal entorno de aire":
                consejo = "no quemes resuidos mejor recicla o composta tus residuos para disminuirla"
            if class_name == "Mal entorno de basura":
                consejo = "recuerda puedes reciclar,compostar y hacer mas cosas para evitar estos problemas"
            if class_name == "deforestacion":
                consejo = "este es un problema muy grave para contribuir y evitar este caso puedes plantar arboles y/o te pueduedes unir a una campaña"
            if class_name == "sequia":
                consejo = "Ahorrar agua en el hogar Reparar fugas, usar regaderas eficientes, recolectar agua de lluvia Optimizar el riego en agricultura Utilizar sistemas de riego por goteo, aprovechar el agua de escorrentía."
            if class_name == "Mal entorno de agua contaminada":
                consejo = "Reduce el uso de productos químicos: Evita utilizar productos de limpieza agresivos que puedan contaminar las aguas."
            if class_name == "Regular contaminación del aire":
                consejo = "utiliza una bicicleta para evitar seguir contaminando "
            if class_name == "Regular entorno de basura":
                consejo = "Educa a tus amigos y familiares sobre la importancia de cuidar el medio ambiente y las prácticas de manejo de residuos."
            if class_name == "Regular entorno de agua contaminada":
                consejo = "Ahorra agua Pequeños cambios en tus hábitos de consumo, como duchas más cortas o reparar fugas, pueden hacer una gran diferencia."
            if class_name == "Buen entorno de aire":
                consejo = "Ventilar regularmente: Renovar el aire interior para reducir la concentración de contaminantes."
            if class_name == "Buen entorno de agua":
                consejo = "Participa en limpiezas ayuda a retirar la basura de ríos, lagos y playas."
            if class_name == "Buen entorno de suelo":
                consejo = "Mantén el suelo cubierto con plantas, ya sean cultivos, pastos o árboles. Las raíces ayudan a fijar el suelo y evitan que sea arrastrado por el viento o el agua."
            
            return render_template('resultado.html', class_name=class_name, confidence_score=confidence_score, consejo=consejo)
    return render_template('index.html')


app.run(debug=True)