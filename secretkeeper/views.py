from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from secretkeeper.models import Secret, increment_positive_count
from django.views.decorators.csrf import ensure_csrf_cookie
@ensure_csrf_cookie




def index(request, page=None):
    top_secrets = Secret.objects.order_by('-share_count')[:10]
    all_secrets = Secret.objects.all().order_by('-share_count')
    
    paginator = Paginator(all_secrets, 10)

    # page = request.GET.get('page')

    try:
        secrets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        secrets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        secrets = paginator.page(paginator.num_pages)


    template = loader.get_template('index.html')
    context = RequestContext(request, {
        'secrets': secrets,
    })
    return HttpResponse(template.render(context))

def vote(request):
    if request.method == 'POST':
        secret_id = request.POST.get('id')
        increment_positive_count(secret_id)
        return HttpResponse("success!")
    else:
        context = RequestContext(request, {
        'failed': ['failed'],
        })
        return redirect('/')

