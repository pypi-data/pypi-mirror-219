from client import Client
import time


class YJPaintingSDK:
    def __init__(self, apiKey, apiSecret):
        self.client = Client(apiKey=apiKey, apiSecret=apiSecret)

    def put_task(self, prompt="孙悟空", ratio=0, style='', guidance_scale='7.5', engine='stable_diffusion', callback_url='http://47.111.11.42:8082/painting-open-api/site/callback_task',
                 callback_type='end', enable_face_enhance='', is_last_layer_skip='', init_image='https://app.yjai.art:30108/yijian-painting/upload_user_image/10000/d9ad4f63-572b-4797-8330-73e79c8966b8.jpg',
                 init_strength=50, steps_mode=0):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/put_task'
        task_params = {
            'prompt': prompt,
            'ratio': ratio,
            'style': style,
            'guidence_scale': guidance_scale,
            'engine': engine,
            'callback_url': callback_url,
            'callback_type': callback_type,
            'enable_face_enhance': enable_face_enhance,
            'is_last_layer_skip': is_last_layer_skip,
            'init_image': init_image,
            'init_strength': init_strength,
            'steps_mode': steps_mode
        }
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

    def show_task_detail(self, uuid):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/show_task_detail'
        task_params = {
            "uuid": uuid
        }
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

    def show_task_detail_batch(self, uuids):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/show_task_detail_batch'
        task_params = {
            "uuid": uuids
        }
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

    def show_complete_tasks(self, page=1, page_size=10):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/show_complete_tasks'
        task_params = {
            "page": page,
            "page_size": page_size
        }
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

    def cancel_task(self, uuid):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/cancel_task'
        task_params = {
            "uuid": uuid
        }
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

    def get_draw_selector(self):
        request_url = 'http://api.yjai.art:8080/painting-open-api/site/get_draw_selector4'
        task_params = {}
        response, error = self.client.post_open_api(request_url, task_params)
        if error is not None:
            return None, error
        else:
            return response, None

