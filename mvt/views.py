from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from mvt.models import CareSeeker
from mvt.models import CareTaker
from mvt.models import Request
from mvt.models import FundTransferRecord
from mvt.models import Review
from mvt.forms import FundForm
from mvt.forms import ApproveFrom
from mvt.forms import ReviewForm
from mvt.mixins import FundRequiredMixin
from mvt.mixins import CareSeekerCountMixin
from mvt.mixins import ApprovalCheckMixin
from django.urls import reverse_lazy
from django.contrib import messages
from datetime import date
from mvt.mixins import AdminMixin
from django.contrib import messages


# Create your views here.
#  def index(request,*args,**kwargs):

#      published_post = post.objects.filter(status="p")
#      category = Catogary.objects.all()
#      return render(request,"blog/index.html",context={"posts":published_post,"category":category})

def index(request,*args,**kwargs):

    return render(request,"mvt/index.html")




class CareSeekerList(LoginRequiredMixin,PermissionRequiredMixin,ListView):

    login_url = 'login'
    model = CareSeeker
    queryset = CareSeeker.objects.filter(is_available = True)
    template_name = 'mvt/care_seeker_list.html'
    context_object_name = 'care_seekers'
    permission_required = 'mvt.view_careseeker'
 
    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(**kwargs)
        care_taker = CareTaker.objects.get(care_taker = self.request.user)
        context['requested_cs'] = care_taker.care_seeker_duplication()
        return context


class CareSeekerDetail(LoginRequiredMixin,PermissionRequiredMixin,CareSeekerCountMixin,DetailView):

    model = CareSeeker
    template_name = 'mvt/CareSeekerDetail.html'
    login_url = 'login'
    permission_required = 'mvt.view_careseeker'
    context_object_name = 'care_seeker'

    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        care_taker = CareTaker.objects.get(care_taker = self.request.user)
        context['review'] = self.request.user.check_review(self.object,care_taker)
        request = care_taker.get_care_seeker(self.object)
        if request:
            status = request.get_status()
            if status == "completed":
                context['status'] = None
            else:
                context['status'] = status
        return context
    
    def get_queryset(self,*args,**kwargs):

        cs = get_object_or_404(CareSeeker,pk=self.kwargs['pk'])
        if len(self.kwargs)==2:
            ct = get_object_or_404(CareTaker,care_taker=self.request.user)
            if ct.check_request(cs):
                request = Request(care_seeker=cs,care_taker=ct,status='PE')
                request.save()
                request.auto_rejection()
            else:
                messages.warning(self.request, f'You have alredy sent request once.')

        return CareSeeker.objects.filter(pk=self.kwargs['pk'])
            


class CareSeekersRequestStatus(LoginRequiredMixin,PermissionRequiredMixin,ListView):

    login_url = 'login'
    model = Request
    permission_required = 'mvt.view_request'
    context_object_name = 'requests'
    template_name = 'mvt/request_status.html'

    def get_queryset(self):

        ct = get_object_or_404(CareTaker,care_taker=self.request.user)
        return ct.get_care_seekers()


class CareTakersRequests(LoginRequiredMixin,PermissionRequiredMixin,ListView):

    login_url = 'login'
    permission_required = ('mvt.view_request','mvt.view_caretaker')
    model = Request
    template_name = 'mvt/caretaker_request.html'
    context_object_name = 'caretaker_request'

    def get_queryset(self,*args,**kwargs):

        cs = get_object_or_404(CareSeeker,care_seeker=self.request.user)
        request = cs.get_request()
        return request

class CareTakerDetail(LoginRequiredMixin,PermissionRequiredMixin,DetailView):

    login_url = 'login'
    permission_required = 'mvt.view_caretaker'
    model = CareTaker
    template_name = 'mvt/caretaker.html'
    context_object_name = 'ct'

    def get_context_data(self,*args,**kwargs):

        context = super().get_context_data(*args,**kwargs)
        cs = get_object_or_404(CareSeeker,care_seeker=self.request.user)
        context['status'] = cs.get_care_taker_status(self.object)
        context['review'] = self.request.user.check_review(cs,context['ct'])
        return context

class AproveRequest(LoginRequiredMixin,PermissionRequiredMixin,FundRequiredMixin,ApprovalCheckMixin,UpdateView):

    model = CareTaker
    form_class = ApproveFrom
    template_name = 'mvt/caretaker_approve.html'
    login_url = 'login'
    permission_required = 'mvt.change_request'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('caretaker',kwargs = {'pk':pk})

    def get_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('update_fund',kwargs = {'pk':pk})
    
    def post(self,request,*args,**kwargs):
        ct = get_object_or_404(CareTaker,pk=self.kwargs['pk'])
        cs = get_object_or_404(CareSeeker,care_seeker = request.user)
        cs.approve_request(ct,request.POST)
        messages.success(request, f'Your request has been approved')
        return super(AproveRequest,self).post(request,*args,**kwargs)



class UpdateFund(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):

    model = CareSeeker
    form_class = FundForm
    login_url = 'login'
    permission_required = 'mvt.change_careseeker'
    template_name = 'mvt/fundform.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('approve_request',kwargs = {'pk':pk})

    def post(self,request,*args,**kwargs):
        cs = get_object_or_404(CareSeeker,care_seeker=request.user)
        cs.add_fund(request.POST['wallet'])
        messages.success(request, f'fund has been succefully allocated')
        return super(UpdateFund,self).post(request,*args,**kwargs)


class StartService(LoginRequiredMixin,PermissionRequiredMixin,AdminMixin,ListView):

    login_url = 'login'
    permission_required = ('mvt.view_request','mvt.change_request')
    template_name = "mvt/start_service.html"
    model = Request
    context_object_name = 'requests'

    def get_queryset(self,*args,**kwargs):
        if self.kwargs:
            request_ob = get_object_or_404(Request,pk=self.kwargs['pk'])
            request_ob.start_service()
        request = Request.objects.filter(status = 'AP').filter(start_date=date.today())
        return request
    


class StopService(LoginRequiredMixin,PermissionRequiredMixin,AdminMixin,ListView):

    login_url = 'login'
    permission_required = ('mvt.view_request','mvt.change_request')
    template_name = 'mvt/end_service.html'
    model = Request
    context_object_name = 'requests'

    def get_queryset(self,*args,**kwargs):
        if self.kwargs:
            request_ob = get_object_or_404(Request,pk=self.kwargs['pk'])
            bill = request_ob.end_service()
            request_ob.care_seeker.end_service(bill)
            request_ob.care_taker.end_service(bill)
            FundTransferRecord.objects.create(payer=request_ob.care_seeker,reciver=request_ob.care_taker,ammount=bill)
        request = Request.objects.filter(status = 'AC').filter(end_date=date.today())
        return request


class RejectService(LoginRequiredMixin,PermissionRequiredMixin,AdminMixin,ListView):

    login_url = 'login'
    permission_required = ('mvt.view_request','mvt.change_request')
    template_name = 'mvt/reject_request.html'
    model = Request
    context_object_name = 'requests'

    def get_queryset(self,*args,**kwargs):
        if self.kwargs:
            request_ob = get_object_or_404(Request,pk=self.kwargs['pk'])
            request_ob.reject_request()
        request = Request.objects.filter(status = 'PE').filter(end_date=date.today())
        return request


class ReviewView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):

    login_url = "login"
    permission_required = 'mvt.add_review'
    form_class = ReviewForm
    template_name = "mvt/review.html"
    
    def get_success_url(self):
        return reverse_lazy("index")


    def post(self,request,*args,**kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid():
            if self.kwargs['slug'] == 'cs':
                to_user = get_object_or_404(CareSeeker,pk=self.kwargs['pk'])
                obj = to_user
                to_user = to_user.care_seeker
                from_user = get_object_or_404(CareTaker,care_taker=request.user)
            else:
                to_user = get_object_or_404(CareTaker,pk=self.kwargs['pk'])
                obj = to_user
                to_user = to_user.care_taker
                from_user = get_object_or_404(CareSeeker,care_seeker=request.user)
            request_ob = from_user.get_request_object(obj)
            if request.user.check_review1(request_ob):
                Review.objects.create(from_user = request.user,to_user=to_user,request_ob=request_ob,msg=request.POST['msg'],rating=request.POST['rating'])
                messages.success(request, f'thank you.your review has been submitted')
                return redirect("index")
            else:
                messages.success(request, f'Review has been already provided')
                return redirect("index")

        return render(request, "mvt/review.html", {'form': form})
       
        

        
