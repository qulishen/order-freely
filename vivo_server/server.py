from flask import Flask, request
from PIL import Image
import base64
from io import BytesIO
from vivo import ocr_test
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload():
    # 获取Base64编码的图片数据
    data = request.get_json()
    image_data = data['image']

    # 解码Base64编码的图片数据
    image_bytes = base64.b64decode(image_data)
    image = Image.open(BytesIO(image_bytes))

    # 在此处添加图像处理代码
    # 例如，将图像保存到服务器
    image_path = 'uploaded_image.jpg'
    image.save(image_path)

    # 返回处理后的结果
    res = "处理成功"
    res = ocr_test('./uploaded_image.jpg')
    print(res)
    return res


if __name__ == '__main__':
    app.run()
