from flask import Flask, request, send_file, abort
import boto3
import io

app = Flask(__name__)

s3 = boto3.client('s3')

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello, world!"

@app.route('/files', methods=['GET'])
def list_files():
    
    print("Listing objects...")
    
    response = s3.list_objects_v2(Bucket='relatorios-vault')
    files = response['Contents']
    #print(files)
    
    return files

@app.route('/download/file', methods=['GET'])
def download():
    try:
        nome = request.args.get('nome')
        response = s3.get_object(Bucket='relatorios-vault', Key=nome)
        file_content = response['Body'].read()
    except Exception as e:
        abort(404, "Arquivo não existe")
    
    return send_file(io.BytesIO(file_content), as_attachment=True, download_name=nome)

if __name__ == '__main__':
    app.run(debug=True)