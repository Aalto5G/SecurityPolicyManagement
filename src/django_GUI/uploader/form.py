"""
BSD 3-Clause License
Copyright (c) 2018, Muhammad Hassaan Bin Mohsin, Aalto University, Finland
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from django import forms
from uploader.models import host_ids, firewall_policies, host_policies, ces_policies, bootstrap
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django.core.exceptions import ValidationError
import json
import urllib.request


def get_users_list():
    data = urllib.request.urlopen("http://127.0.0.1/API/firewall_policy/ID").read().decode("utf-8")
    show_users=[]
    for d in json.loads(data):
        show_users.append((d[1], d[2]))
    return show_users

def get_ces_uid_list():
    # id, trans_protocol, link_alias, dest_ces, reputation, direction, uid
    data = urllib.request.urlopen("http://127.0.0.1/API/firewall_policy/ces_policy_identity").read().decode("utf-8")
    show_users=[]
    for d in json.loads(data):
        show_users.append((d[3], d[1]+'-'+d[2]))
    return show_users

def get_cetp_uid_list():
    #id, local_fqdn, remote_fqdn, reputation, direction, uid
    data = urllib.request.urlopen("http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY").read().decode("utf-8")
    show_users=[]
    for d in json.loads(data):
        show_users.append((d[5], str(d[1])+'-'+str(d[2])+'-'+str(d[3])+'-'+str(d[4])))
    return show_users

def get_users_list_fqdn():
    data = urllib.request.urlopen("http://127.0.0.1/API/firewall_policy/ID").read().decode("utf-8")
    show_users=[]
    for d in json.loads(data):
        show_users.append((d[2], d[2]))
    return show_users



##################################################################################################
##################################################################################################
##################################################################################################
#     HOST FIREWALL Policies FORM


class UserForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'name': 'name', 'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last Name', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'name': 'name', 'placeholder': 'Last Name'}))
    username = forms.CharField(min_length=6, label='Username', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'name': 'username', 'placeholder': 'Username'}))
    email = forms.EmailField(label='Email', max_length=64, widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'name': 'email', 'placeholder': 'Email'}))
    password = forms.CharField(min_length=6, label='Password', max_length=32, widget=forms.TextInput(attrs={'class': 'form-control input-lg', 'name': 'password', 'placeholder': 'Password', 'type': 'password'}))
    is_staff = forms.BooleanField(label='Check if Admin', required=False)
    error_messages = {'duplicate_username': 'Username Already Exists'}
    class Meta:
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'is_staff']

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        #if self.instance.username == username:
        #    return username
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'], code='duplicate_username', )



class host_idsForm(forms.ModelForm):
    class Meta:
        model = host_ids
        fields = ['fqdn', 'msisdn', 'ipv4', 'username']


class firewall_policiesForm(forms.ModelForm):
    #fqdn = forms.ChoiceField(choices=get_users_list_fqdn())
    types = forms.ChoiceField(choices=[('GROUP', 'GROUP'), ('CIRCULARPOOL', 'CIRCULARPOOL'), ('CARRIERGRADE', 'CARRIERGRADE'), ('SFQDN', 'SFQDN'), ('FIREWALL', 'FIREWALL')])
    sub_type = forms.ChoiceField(choices=[('FIREWALL_ADMIN', 'FIREWALL_ADMIN')])
    def __init__(self, *args, **kwargs):
        super(firewall_policiesForm, self).__init__(*args, **kwargs)
        #self.fqdn = forms.ChoiceField(choices=get_users_list_fqdn())
        self.fields['fqdn'] = forms.ChoiceField(choices=get_users_list_fqdn())
    class Meta:
        model = firewall_policies
        fields = '__all__'

class firewall_policies_userForm(forms.ModelForm):
    types = forms.ChoiceField(choices=[('GROUP', 'GROUP'), ('CIRCULARPOOL', 'CIRCULARPOOL'), ('CARRIERGRADE', 'CARRIERGRADE'), ('SFQDN', 'SFQDN'), ('FIREWALL', 'FIREWALL')])
    sub_type = forms.ChoiceField(choices=[('FIREWALL_USER', 'FIREWALL_USER')])
    class Meta:
        model = firewall_policies
        fields = ['types', 'sub_type', 'policy_element']


class host_policiesForm(forms.ModelForm):
    #local_fqdn = forms.ChoiceField(choices=get_users_list_fqdn()) #.append(('','Both'))
    direction = forms.ChoiceField(choices=[('EGRESS', 'EGRESS'), ('INGRESS', 'INGRESS'), ('*', 'BOTH')])
    types = forms.ChoiceField(choices=[('available', 'available'), ('offer', 'offer'), ('request', 'request')])
    def __init__(self, *args, **kwargs):
        super(host_policiesForm, self).__init__(*args, **kwargs)
        self.fields['local_fqdn'] = forms.ChoiceField(choices=get_users_list_fqdn())
    class Meta:
        model = host_policies
        fields = '__all__'


class host_policies_userForm(forms.ModelForm):
    direction = forms.ChoiceField(choices=[('EGRESS', 'EGRESS'), ('INGRESS', 'INGRESS'), ('*', 'BOTH')])
    types = forms.ChoiceField(choices=[('available', 'available'), ('offer', 'offer'), ('request', 'request')])
    class Meta:
        model = host_policies
        fields = ['direction', 'types', 'policy_element']


class ces_policiesForm(forms.ModelForm):
    #uuid = forms.ChoiceField(choices=get_ces_uid_list())
    types = forms.ChoiceField(choices=[('available', 'available'), ('offer', 'offer'), ('request', 'request')])
    def __init__(self, *args, **kwargs):
        super(ces_policiesForm, self).__init__(*args, **kwargs)
        #self.uuid = forms.ChoiceField(choices=get_ces_uid_list())

    class Meta:
        model = ces_policies
        fields = '__all__'



##################################################################################################
##################################################################################################
##################################################################################################




class bootstrapForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[('IPSET', 'IPSET'), ('IPTABLES','IPTABLES'), ('CIRCULARPOOL','CIRCULARPOOL')])
    sub_type = forms.ChoiceField(choices=[('rules', 'rules'), ('requires','requires')])
    class Meta:
        model = bootstrap
        fields = '__all__'







'''

class host_firewallForm(forms.ModelForm):
    fqdn = forms.ChoiceField(choices=get_users_list_fqdn())
    type = forms.ChoiceField(choices=[('FIREWALL_ADMIN', 'FIREWALL_ADMIN'), ('FIREWALL_USER', 'FIREWALL_USER')])
    direction = forms.ChoiceField(choices=[('EGRESS', 'EGRESS'), ('INGRESS','INGRESS'), ('*','BOTH')])
    target = forms.ChoiceField(choices=[('DROP', 'DROP'), ('ALLOW','ALLOW')])
    protocol = forms.ChoiceField(choices=[('17', 'UDP'), ('6', 'TCP'), ('1', 'ICMP'), ('2', 'IGMP')])
    priority = forms.ChoiceField(choices=[('1', '1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'), ('10','10')])
    #schedule_start = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3 ))
    #schedule_end = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))

    def __init__(self, *args, **kwargs):
        super(host_firewallForm, self).__init__(*args, **kwargs)
        self.fields['fqdn'] = forms.ChoiceField(choices=get_users_list_fqdn())
    class Meta:
        model = host_firewall
        fields = '__all__'




class host_firewalluserForm(forms.ModelForm):
    type = forms.ChoiceField(choices=[('FIREWALL_ADMIN', 'FIREWALL_ADMIN'), ('FIREWALL_USER', 'FIREWALL_USER')])
    direction = forms.ChoiceField(choices=[('EGRESS', 'EGRESS'), ('INGRESS', 'INGRESS'), ('*', 'BOTH')])
    target = forms.ChoiceField(choices=[('DROP', 'DROP'), ('ALLOW', 'ALLOW')])
    protocol = forms.ChoiceField(choices=[('17', 'UDP'), ('6', 'TCP'), ('1', 'ICMP'), ('2', 'IGMP')])
    priority = forms.ChoiceField(
        choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                 ('9', '9'), ('10', '10')])

    # schedule_start = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3 ))
    # schedule_end = forms.DateTimeField(widget=DateTimeWidget(usel10n=True, bootstrap_version=3))
    class Meta:
        model = host_firewall
        fields = ['type', 'active', 'priority', 'direction', 'src', 'dst', 'sport', 'dport', 'protocol', 'target', 'comment', 'raw_data']
'''