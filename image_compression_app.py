'''
Dyanmic  compressed image served through pyramid app.

Run 'python image_compression_app.py'.

Now go to terminal and view any image of PNG/JPG/JPEG and many more, 
present in the same directory as this app with using URL :
	localhost:8080/images/{imageName}?compressed=true if compression is required.
	localhost:8080/images/{imageName}?compressed=true?res=50 compress by 50%.

'''

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
import traceback
import tempfile
from PIL import Image
from cStringIO import StringIO

from pyramid.response import FileResponse


def serve_image(request):
	'''
	/images/{imageName}
	'''
    try:
        if request.params.get('compressed') == 'true':
            img = Image.open('images/' + request.matchdict['imageName'])
            tmp = StringIO()
            img.save(tmp, 'JPEG', quality=int(
                request.params.get('res'), 80))
            tmp.seek(0)
            output_data = tmp.getvalue()

            tmp.close()
            x = tempfile.NamedTemporaryFile()
            x.write(output_data)
            x.seek(0)
            response = FileResponse(
                x.name,
                request=request,
                content_type='image/jpeg'
            )
        else:
            response = FileResponse(
                'images/' + request.matchdict['imageName'],
                request=request,
                content_type='image/jpeg'
            )
        return response

    except Exception as e:
        traceback.print_exc()
        print e.message

if __name__ == '__main__':
    config = Configurator()
    config.add_route('image', '/images/{imageId}')
    config.add_view(serve_image, route_name='image')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
