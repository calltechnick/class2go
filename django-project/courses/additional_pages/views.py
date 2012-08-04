from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.template import RequestContext
from c2g.models import *
from courses.course_materials import get_course_materials
from courses.common_page_data import get_common_page_data
import re

def manage_nav_menu(request, course_prefix, course_suffix):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
    except:
        raise Http404
        
    if not common_page_data['is_course_admin']:
        redirect('courses.views.main', course_prefix, course_suffix)
    
    return render_to_response('additional_pages/manage_nav_menu.html', {'common_page_data':common_page_data}, context_instance=RequestContext(request))
    
def main(request, course_prefix, course_suffix, slug):
    try:
        common_page_data = get_common_page_data(request, course_prefix, course_suffix)
        page = AdditionalPage.objects.get(course=common_page_data['course'], slug=slug)
    except:
        raise Http404
    
    if common_page_data['is_course_admin'] and common_page_data['course_mode'] == 'staging' and common_page_data['view_mode'] == 'edit':
        template = 'additional_pages/edit.html'
    else:
        template = 'additional_pages/view.html'
        
    return render_to_response(template,{'common_page_data': common_page_data, 'page':page},context_instance=RequestContext(request))
