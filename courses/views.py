from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
from django.db.models import Count
from django.core.cache import cache

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin

from .models import Course, Module, Content, Subject
from .forms import ModuleFormset

from students.forms import CourseEnrollForm

class OwnerMixin(object):
	def get_queryset(self):
		course_query = super(OwnerMixin, self).get_queryset()
		return course_query.filter(owner=self.request.user)


class OwnerEditMixin(object):
	def form_valid(self, form):
		form.instance.owner = self.request.user
		return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
	model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
	fields = ['subject', 'title', 'slug', 'overview']
	success_url = reverse_lazy('manage_course')
	template_name = 'courses/manage/update.html'


class CourseManageListView(OwnerCourseMixin, ListView):
	template_name = "courses/manage/list.html"

class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
	permission_required = "courses.add_course"


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
	permission_required = "courses.change_course"


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
	template_name = 'courses/manage/delete.html'
	success_url = reverse_lazy('manage_course')
	permission_required = "courses.delete_course"


class CourseModuleUpdateView(TemplateResponseMixin, View):
	template_name = "courses/manage/cmformset.html"
	course = None

	def get_formset(self, data=None):
		return ModuleFormset(instance=self.course, data=data)

	def dispatch(self, request, pk):
		self.course = get_object_or_404(Course, id=pk, owner=request.user)
		return super().dispatch(request, pk)

	def get(self, request, *args, **kwargs):
		formset = self.get_formset()
		context = {'course': self.course, 'formset': formset}
		return self.render_to_response(context)

	def post(self, request, *args, **kwargs):
		formset = self.get_formset(data=request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('manage_course')

		context = {'course': self.course, 'formset': formset}
		return self.render_to_response(context)


class ModuleContentUpdateView(TemplateResponseMixin, View):
	module = None
	model = None
	obj = None
	template_name = "courses/manage/module_content.html"

	def get_model(self, model_name):
		if model_name in ['text', 'file', 'image', 'video']:
			return apps.get_model(app_label='courses', model_name=model_name)

		return None

	def get_form(self, model, *args, **kwargs):
		form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
		return form(*args, **kwargs)


	def dispatch(self, request, module_id, model_name, id=None):
		self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
		self.model =  self.get_model(model_name)
		if id:
			self.obj = get_object_or_404(self.model, id=id, owner=request.user)


		return super().dispatch(request, module_id, model_name, id)


	def get(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model,  instance=self.obj)
		context = {'form': form, 'obj':self.obj}
		return self.render_to_response(context)

	def post(self, request, module_id, model_name, id=None):
		form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
		context = {'form': form, 'obj':self.obj}

		if form.is_valid():
			obj = form.save(commit=False)
			obj.owner = request.user
			obj.save()

			if not id:
				Content.objects.create(module=self.module, item=obj)

			return redirect('module_content_list', self.module.id)

		return self.render_to_response(context)


class ContentDeleteView(View):
	def post(self, request, id):
		content = get_object_or_404(Content, id=id, module__course__owner=request.user)
		module = content.module
		content.item.delete()
		content.delete()

		return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
	template_name = "courses/manage/content_list.html"

	def get(self, request, module_id):
		module = get_object_or_404(Module, id=module_id, course__owner=request.user)
		context = {'module':module}
		return self.render_to_response(context)


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Module.objects.filter(id=id, course__owner=request.user).update(order=order)
		return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
	def post(self, request):
		for id, order in self.request_json.items():
			Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)

		return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
	model = Course
	template_name = 'courses/course_list.html'
	def get(self, request, subject_slug=None):
		subjects = cache.get("all_subjects")
		if not subjects:
			subjects = Subject.objects.annotate(total_courses=Count('courses'))
			cache.set("all_subjects", subjects)

		all_courses = Course.objects.annotate(total_modules=Count('modules'))
		subject = None
		
		if subject_slug:
			subject = get_object_or_404(Subject, slug=subject_slug)
			key = f"subject_{subject.id}_courses"
			courses = cache.get(key)
			if not courses:
				courses = all_courses.filter(subject=subject)
				cache.set(key, courses)

		else:
			courses = cache.get("all_courses")
			if not courses:
				courses = all_courses
				cache.set("all_courses", courses)
				
		context = {'subjects': subjects, 'subject': subject, 'courses': courses}
		return self.render_to_response(context)



class CourseDetailView(DetailView):
	model = Course
	template_name = "courses/course_detail.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})

		return context
