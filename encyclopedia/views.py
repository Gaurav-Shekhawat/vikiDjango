from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.template import RequestContext
from django.urls import reverse
import markdown
import os

from . import util

class SearchWikiForm(forms.Form):
    pagetitle = forms.CharField(label = "")


class newPageForm(forms.Form):
    pageTitle = forms.CharField(label = "Title")
    pageContent = forms.CharField(widget=forms.Textarea)


def index(request):

    if request.method == "POST":
        form = SearchWikiForm(request.POST)

        if form.is_valid():
            pagetitle = form.cleaned_data["pagetitle"]

            if pagetitle in util.list_entries():
                return HttpResponseRedirect(f"/wiki/{pagetitle}");
            else:
                displayTitles = []
                for title in util.list_entries():
                    if(title.lower().count(pagetitle.lower())>0):
                        displayTitles += [title]
                
                return render(request, "encyclopedia/search.html", {
                    "displayTitles": displayTitles,
                    "form": SearchWikiForm() 
                })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":SearchWikiForm()
    })

def entry(request, pagetitle):
    if pagetitle in util.list_entries():      
        with open(f"entries/{pagetitle}.md", 'r') as f:
            text = f.read()
            html = markdown.markdown(text)  
            return render(request, "encyclopedia/entry.html", {
                "bodyContent": html,
                "pagetitle": pagetitle,
                "form":SearchWikiForm()
            })
    else:
        return render(request, "encyclopedia/404.html");


def newPage(request):
    if request.method == "POST":
        form = newPageForm(request.POST)

        if form.is_valid():
            newPageTitle = form.cleaned_data["pageTitle"]
            if "name" not in form.cleaned_data:
                if newPageTitle in util.list_entries():
                    return HttpResponse("Error: Blog already exists")
            newPageBody = form.cleaned_data["pageContent"]
            finalPath = os.path.join("entries", f"{newPageTitle}.md");
            file1 = open(finalPath, "w");
            file1.write(newPageBody)
            file1.close()
            return HttpResponseRedirect("/")
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form":form
            })



    return render(request, "encyclopedia/newPage.html", {
        "form": newPageForm()
    })


def edit(request, pagetitle):
    with open(f"entries/{pagetitle}.md", 'r') as f:
        text = f.read()
        diction = {
            "pageTitle":pagetitle, 
            "pageContent":text
            }
        form = newPageForm(diction)
        f.close()
        return render(request, "encyclopedia/edit.html", {
            "pagetitle": f"edit:{pagetitle}",
            "editForm":form, 
            "form": SearchWikiForm()
        })

def editpage(request):
    if request.method == "POST":
        form = newPageForm(request.POST)

        if form.is_valid():
            edittedPageTitle = form.cleaned_data["pageTitle"]
            edittedPageBody = form.cleaned_data["pageContent"]
            finalPath = os.path.join("entries", f"{edittedPageTitle}.md");
            file1 = open(finalPath, "w");
            file1.write(edittedPageBody)
            file1.close()
            return HttpResponseRedirect(f"/wiki/{edittedPageTitle}")
        else:
            return render(request, "encyclopedia/edit.html", {
                "form":form
            })
    else:
        return HttpResponse("inside the else statement, you fucked up mister")