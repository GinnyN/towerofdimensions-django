@login_required 
def openid_form (request): 
    class OpenIDManipulator (formfields.Manipulator): 
        def __init__ (self): 
            self.fields = (formfields.TextField (field_name="url", length=30, maxlength=50, is_required=True),) 
    manipulator = OpenIDManipulator () 
    errors = dict () 
    if request.method == 'POST':
        new_data = request.POST.copy () 
        openid_url = request.POST['url'] 
 
        if not openid_url: 
            errors['url'] = ['You must enter an OpenID URL.'] 
 
        if len (errors) == 0: 
            status, info = OID_CONSUMER.beginAuth (openid_url) 
 
            if status == openid.consumer.consumer.HTTP_FAILURE: 
                fmt = 'Failed to retrieve <q>%s</q>' + ': %s' % status 
                errors['url'] = fmt % (cgi.escape (openid_url),) 
            elif status == openid.consumer.consumer.PARSE_ERROR: 
                fmt = 'Could not find OpenID information in <q>%s</q>' 
                errors['url'] = fmt % (cgi.escape (openid_url),) 
            elif status == openid.consumer.consumer.SUCCESS: 
                return_to = SITE_TOP_URL + '/openid/process/%s' % info.token 
                redirect_url = OID_CONSUMER.constructRedirect (info, return_to, trust_root=SITE_TOP_URL) 
                return HttpResponseRedirect (redirect_url) 
            else: 
                errors['url'] = ["Shouldn't happen"] 
    else: 
        new_data = {} 
        errors = new_data = {} 
    form = formfields.FormWrapper (manipulator, new_data, errors) 
    return render_to_response ('openid/openid', {'form': form})

@login_required
def process (request, token=None):
    status, info = OID_CONSUMER.completeAuth (token, request.GET)

    if status == openid.consumer.consumer.FAILURE and info:
        message = 'Verification of "%s" failed.' % cgi.escape (info)
    elif status == openid.consumer.consumer.SUCCESS:
        if info:
            message = 'Successfully verified "%s".' % cgi.escape (info)
        else:
            message = 'Verification cancelled.'
    else:
        message = 'Verification failed.'

    request.user.add_message (message)
    return HttpResponseRedirect ('/') 