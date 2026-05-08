import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue

#-------------FILe HANDLING-------------------
def read_file(filename):
    try:
        with open(filename,"r") as f:
            return json.load(f)
    except:
        return []

def write_file(filename,data):
    with open(filename,"w") as f:
        json.dump(data,f,indent = 4)

#------------------Reporter API---------------
@csrf_exempt
def reporters(request):
    if request.method == "POST":
        data = json.loads(request.body)

        reporter = Reporter(**data)
        reporter.validate()

        all_reporters = read_file("reporters.json")
        all_reporters.append(reporter.to_dict())

        write_file("reporters.json",all_reporters)

        return JsonResponse(reporter.to_dict(),status = 201)

    elif request.method == "GET":
        all_reporters = read_file("reporters.json")
        reporter_id = request.GET.get("id")

        if reporter_id:
            for r in all_reporters:
                if str(r["id"]) == reporter_id:
                    return JsonResponse(r)
        
        return JsonResponse(all_reporters,safe = False)

#-------------------ISSUE API--------------------------
@csrf_exempt
def issues(request):

    if request.method == "POST":
        data = json.loads(request.body)

        #subclass logic
        if data["priority"] == "critical":
            issue = CriticalIssue(**data)
        elif data["priority"] == "low":
            issue = LowPriorityIssue(**data)
        else:
            issue = Issue(**data)

        try:
            issue.validate()

        except ValueError as e:
            return JsonResponse({"error" : str(e)}, status = 400)

        all_issues = read_file("issues.json")
        all_issues.append(issue.to_dict())

        write_file("issues.json",all_issues)

        response_data = issue.to_dict()
        response_data["message"] = issue.describe()

        return JsonResponse(response_data,status = 201)

    elif request.method == "GET":
        all_issues = read_file("issues.json")

        issue_id = request.GET.get("id")
        status = request.GET.get("status")

        if issue_id:
            for i in all_issues:
                if str(i["id"] == issue_id):
                    return JsonResponse(i)

            return JsonResponse({"error":"message not found"}, status = 404)

        if status:
            filtered = [i for i in all_issues if i["status"] == status]
            return JsonResponse(filtered, safe = False)


        return JsonResponse(all_issues, safe = False)

