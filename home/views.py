from django.shortcuts import render, redirect


# Create your views here.

def test_html(request):

    return render(request, "home/test.html")


class home:

    @staticmethod
    def org_home(request):
        if not request.session.get("orgname") or not request.session.get("org_id"):
            return redirect('org_login')
        return render(request, "home/org_home.html")
    
    @staticmethod
    def user_home(request):
        if not request.session.get("username") or not request.session.get("user_id"):
            return redirect('user_login')
        return render(request, "home/user_home.html")


def domain(request):

    if request.method == "POST":
        domain = request.POST.get("domain")

        if domain not in ["user", "org"]:
            return redirect("domain")

        request.session["login_domain"] = domain
        request.session.modified = True

        if domain == "user":
            return redirect("user_login")
        else:
            return redirect("org_login")
        
    request.session.flush()
    return render(request, "home/select_domain.html")

def underMaintance(request):
    return render(request, "home/undermaintance.html")
