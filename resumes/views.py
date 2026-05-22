from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Resume, Template, Announcement
from .forms import EducationFormSet, ExperienceFormSet, ResumeForm, SkillFormSet

def home(request):
    templates = Template.objects.filter(is_active=True)[:3]
    announcements = Announcement.objects.filter(is_published=True).order_by('-created_at')[:3]
    return render(request, 'home.html', {
        'templates': templates,
        'announcements': announcements,
    })

@login_required
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'resumes/resume_list.html', {'resumes': resumes})

@login_required
def resume_create(request):
    resume = Resume(user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        education_formset = EducationFormSet(request.POST, instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(request.POST, instance=resume, prefix='experience')
        skill_formset = SkillFormSet(request.POST, instance=resume, prefix='skills')
        if (
            form.is_valid()
            and education_formset.is_valid()
            and experience_formset.is_valid()
            and skill_formset.is_valid()
        ):
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            education_formset.instance = resume
            experience_formset.instance = resume
            skill_formset.instance = resume
            education_formset.save()
            experience_formset.save()
            skill_formset.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
        education_formset = EducationFormSet(instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(instance=resume, prefix='experience')
        skill_formset = SkillFormSet(instance=resume, prefix='skills')
    return render(request, 'resumes/resume_form.html', {
        'form': form,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'page_title': 'Створити резюме',
    })


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES, instance=resume)
        education_formset = EducationFormSet(request.POST, instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(request.POST, instance=resume, prefix='experience')
        skill_formset = SkillFormSet(request.POST, instance=resume, prefix='skills')
        if (
            form.is_valid()
            and education_formset.is_valid()
            and experience_formset.is_valid()
            and skill_formset.is_valid()
        ):
            form.save()
            education_formset.save()
            experience_formset.save()
            skill_formset.save()
            return redirect('resume_detail', pk=resume.pk)
    else:
        form = ResumeForm(instance=resume)
        education_formset = EducationFormSet(instance=resume, prefix='education')
        experience_formset = ExperienceFormSet(instance=resume, prefix='experience')
        skill_formset = SkillFormSet(instance=resume, prefix='skills')
    return render(request, 'resumes/resume_form.html', {
        'form': form,
        'resume': resume,
        'education_formset': education_formset,
        'experience_formset': experience_formset,
        'skill_formset': skill_formset,
        'page_title': 'Редагувати резюме',
    })

@login_required
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    return render(request, 'resumes/resume_detail.html', {'resume': resume})

@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == 'POST':
        resume.delete()
        return redirect('resume_list')
    return render(request, 'resumes/resume_confirm_delete.html', {'resume': resume})
