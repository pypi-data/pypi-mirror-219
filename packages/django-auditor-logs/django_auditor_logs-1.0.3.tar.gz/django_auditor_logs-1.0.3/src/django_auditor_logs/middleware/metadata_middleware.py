'''
Middleware to set user metadata and request metadata in the MetadataManager
'''
from django_auditor_logs.metadata import MetadataManager

class MetadataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        request_metadata = {
            'ip':request.META.get('REMOTE_ADDR'),
            'user_agent':request.META.get('HTTP_USER_AGENT'),
            'method':request.META.get('REQUEST_METHOD'),
            'path':request.META.get('PATH_INFO'),
            'query_string':request.META.get('QUERY_STRING'),
            'content_type':request.META.get('CONTENT_TYPE'),
            'content_length':request.META.get('CONTENT_LENGTH'),
        }
        MetadataManager.set_request_metadata(request_metadata)
        response = self.get_response(request)
        if 'Authorization' in request.headers:
            user_metadata = {
                'Authorization':request.headers['Authorization'],
            }
            MetadataManager.set_user_metadata(user_metadata)
        elif hasattr(request, 'user') and request.user.is_authenticated:
            user_metadata = {
                'username':request.user.username,
                'email':request.user.email,
                'first_name':request.user.first_name,
                'last_name':request.user.last_name,
            }
            MetadataManager.set_user_metadata(user_metadata)
        # Code to be executed for each request/response after
        # the view is called.
        return response