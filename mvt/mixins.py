from django import dispatch
from mvt.models import CareSeeker
from mvt.models import CareTaker
from mvt.models import Review
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404


class FundRequiredMixin:

    def dispatch(self,request,*args,**kwargs):
        if request.POST:
            cs = get_object_or_404(CareSeeker,care_seeker=request.user)
            bill = cs.calculatefund(request.POST)
            if cs.check_balance() < bill:
                messages.info(request, f'You dont have sufficient amount in your wallet.minimu fund needs to be in your account is '+str(bill)+'Rupees')
                return redirect(self.get_url())
        return super().dispatch(request,*args,**kwargs)

class ApprovalCheckMixin:

    def dispatch(self,request,*args,**kwargs):
        cs = get_object_or_404(CareSeeker,care_seeker=request.user)
        req = cs.requests.filter(status="AP")
        if req:
            messages.warning(request, f'You can approve only one request')
            return redirect("index")
        return super().dispatch(request,*args,**kwargs)


class CareSeekerCountMixin:

    def dispatch(self,request,*args,**kwargs):
        ct = get_object_or_404(CareTaker,care_taker=request.user)
        if ct.active_caretaker_count >= 4:
            messages.info(request, f'Your care taker count has been exceeded.you cannot send request now')
            return redirect("index")
        return super().dispatch(request,*args,**kwargs)

class AdminMixin:

    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request,*args,**kwargs)
