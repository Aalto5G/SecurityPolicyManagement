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


from django.shortcuts import render
from django.contrib.auth.models import User
from uploader.models import host_ids, firewall_policies, host_policies, ces_policies, bootstrap
from uploader.form import UserForm, bootstrapForm, host_idsForm, firewall_policiesForm, host_policiesForm, ces_policiesForm, firewall_policies_userForm, host_policies_userForm

import httplib2
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.db import connection
from django.views.decorators.csrf import csrf_protect
from django.apps import apps
from django.contrib.auth import authenticate
import urllib.request
import json, requests
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


table_mapping = {'bootstrap':'bootstrap', 'ID':'host_ids', 'FIREWALL':'firewall_policies', 'HOST_POLICY_IDENTITY':'host_policy_identity',
                 'HOST_POLICIES':'host_policies', 'CES_POLICY_IDENTITY':'ces_policy_identity', 'CES_POLICIES':'ces_policies'}

registered_users_state={}

sample_policy ={}
sample_policy['bootstrap'] = "IPTABLES","PACKET_MARKING","requires","{'table': 'mangle', 'chain': 'PREROUTING', 'create': false, 'flush': true}"
sample_policy['ID'] = "something.domain","0145321546504","1.1.1.1","name1"
sample_policy['FIREWALL'] = 'FIREWALL_ADMIN','{"priority": 0,   "direction": "EGRESS", "protocol": "17", "udp":{"dport": "53"}, "target": "REJECT", "hashlimit": {"hashlimit-above":"5/sec", "hashlimit-burst":"50", "hashlimit-name":"DnsLanHosts", "hashlimit-mode":"srcip", "hashlimit-htable-expire":"1001"}, "comment":{"comment":"Host DNS limit"}}'
sample_policy['HOST_POLICIES'] = 'request','{ "ope":"query", "group": "id", "code": "fqdn" }'
sample_policy['CES_POLICIES'] = 'request','{ "ope":"query", "group": "ces", "code": "cesid", "value":["cesb.lte.", "cesc.lte.", "cesd.lte.", "cese.lte."]}'


################################################################################################
################################################################################################
################################################################################################
# Controller Functions


@csrf_protect
@login_required
def view_table(request, database_specified, table_specified):
    message_to_show = ''
    if request.user.is_staff == 1:
        if database_specified == 'ces':
            if request.method == "POST" and len(request.POST.getlist('items')) > 0:
                items = request.POST.getlist('items')
                try:
                    message_to_show, data_status = delete_table_data(table_specified, items)
                except urllib.error.HTTPError as e:
                    data_status = e.code
            data_status, columns, data, list_of_ids = get_table_data(table_specified)
            data = zip(data, list_of_ids)
        elif database_specified == 'bootstrap':
            if request.method == "POST" and len(request.POST.getlist('items')) > 0:
                items = request.POST.getlist('items')
                items = ",".join(items)
                try:
                    uri = "http://127.0.0.1" + '/API/bootstrap_policies/' + items
                    data = requests.delete(uri)
                    data_status = data.status_code
                    message_to_show = data.content.decode("utf-8")
                except urllib.error.HTTPError as e:
                    data_status = e.code
            data = requests.get("http://127.0.0.1/API/bootstrap_policies")
            columns = ['id', 'name', 'types', 'subtype', 'data']
            data_status = data.status_code
            data = json.loads(data.content.decode("utf-8"))
            list_of_ids=[]
            for d in data:
                list_of_ids.append(d[0])
            data = zip(data, list_of_ids)
        if data_status == 200:
            paginator = Paginator(list(data), 25)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, 'tables_view.html', {'table_columns': columns, 'table_data': data,
                                                        'table_name': table_specified, 'message': message_to_show})
        else:
            return render(request, 'tables_view.html',
                          {'table_columns': '', 'table_data': '', 'table_name': '', 'message': message_to_show})
    elif request.user.is_staff == 0:
        if request.method == "POST" and len(request.POST.getlist('items')) > 0:
            items = request.POST.getlist('items')
            try:
                message_to_show, data_status = delete_table_data(table_specified, items)
            except urllib.error.HTTPError as e:
                data_status = e.code
        data_status, columns, data, list_of_ids = get_table_data_user(table_specified, request.user)
        if data_status == 200:
            data = zip(data, list_of_ids)
            paginator = Paginator(list(data), 25)
            page = request.GET.get('page')
            try:
                data = paginator.page(page)
            except PageNotAnInteger:
                data = paginator.page(1)
            except EmptyPage:
                data = paginator.page(paginator.num_pages)
            return render(request, 'tables_view.html', {'table_columns': columns, 'table_data': data,
                                                        'table_name': table_specified, 'message': message_to_show})
        else:
            message_to_show=data
            return render(request, 'tables_view.html',
                          {'table_columns': '', 'table_data': '', 'table_name': '', 'message': message_to_show})



@login_required
@csrf_protect
def add_table_page(request, database_specified, table_specified):
    message_to_show = ''
    if request.user.is_staff == 1:
        if database_specified=='ces':
            table_specified_form = table_mapping[table_specified] + 'Form'
            form = eval(table_specified_form)()
            if request.method=="POST":
                form = eval(table_specified_form)(request.POST, request.FILES)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    data, status_code = add_entry_policy(table_specified, cleaned_data)
                    if status_code==200:
                        return render(request, 'add_entry.html',{'form': form, 'table_name': table_specified, 'message': 'Entry Successfully Added in Database', 'sample_policy':sample_policy[table_specified]})
                    else:
                        message_to_show = data
                        return render(request, 'add_entry.html', {'form': form, 'table_name': table_specified, 'message': message_to_show, 'sample_policy':sample_policy[table_specified]})
                else:
                    return render(request, 'add_entry.html', {'form':form, 'table_name':table_specified, 'sample_policy':sample_policy[table_specified]})
        elif database_specified=='bootstrap':
            table_specified_form = table_mapping[table_specified] + 'Form'
            form = eval(table_specified_form)()
            message_to_show=''
            if request.method=="POST":
                form = eval(table_specified_form)(request.POST, request.FILES)
                if form.is_valid():
                    img = form.cleaned_data
                    data = requests.post("http://127.0.0.1/API/bootstrap_policies", data=json.dumps([img]))
                    if data.status_code==200:
                        return render(request, 'add_entry.html', {'form': form, 'table_name': table_specified,'message': 'Entry Successfully Added in Database', 'sample_policy':sample_policy[table_specified]})
                    else:
                        message_to_show = json.loads(data.content.decode("utf-8"))
                        return render(request, 'add_entry.html', {'form': form, 'table_name': table_specified, 'message': message_to_show, 'sample_policy':sample_policy[table_specified]})
                else:
                    return render(request, 'add_entry.html', {'form':form, 'table_name':table_specified, 'sample_policy':sample_policy[table_specified]})
        else:
            return ('Wrong URL. Contact Administrator')
        return render(request, 'add_entry.html', {'form':form, 'table_name':table_specified, 'sample_policy':sample_policy[table_specified]})
    elif request.user.is_staff == 0:
        table_specified_form = table_mapping[table_specified] + '_userForm'
        form = eval(table_specified_form)()
        print (form)
        if request.method == "POST":
            form = eval(table_specified_form)(request.POST, request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                get_fqdn, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID?username={}'.format(request.user))
                cleaned_data['fqdn']=get_fqdn[0][2]
                cleaned_data['local_fqdn'] =get_fqdn[0][2]
                data, status_code = add_entry_policy(table_specified, cleaned_data)
                if status_code == 200:
                    return render(request, 'add_entry.html', {'form': form, 'table_name': table_specified,
                                                              'message': 'Entry Successfully Added in Database', 'sample_policy':sample_policy[table_specified]})
                else:
                    message_to_show = data
                    return render(request, 'add_entry.html',
                                  {'form': form, 'table_name': table_specified, 'message': message_to_show, 'sample_policy':sample_policy[table_specified]})
            else:
                return render(request, 'add_entry.html', {'form': form, 'table_name': table_specified, 'sample_policy':sample_policy[table_specified]})
        return render(request, 'add_entry.html', {'form':form, 'table_name':table_specified, 'sample_policy':sample_policy[table_specified]})


@login_required
@csrf_protect
def edit_entry(request, database_specified, table_specified, id):
    message_to_show = ''
    if request.user.is_staff == 1:
        if database_specified == 'ces':
            model_selected = apps.get_model(app_label='uploader', model_name=table_mapping[table_specified])
            table_specified_form = table_mapping[table_specified] + 'Form'
            if request.method == "POST":
                form = eval(table_specified_form)(request.POST, request.FILES)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    data, status_code = edit_entry_policy(table_specified, cleaned_data, id)
                    if status_code == 200:
                        url = 'table_view/' + table_specified + '/'
                        return redirect('../../../' + url)
                    else:
                        message_to_show = data
            response, status_code = edit_entry_host_policies_form(table_specified, id)
            if status_code == 200:
                instance = model_selected
                for key in response:
                    setattr(instance, key, response[key])
                form = eval(table_specified_form)(instance=instance)
            else:
                return redirect('main')
        elif database_specified == 'bootstrap':
            model_selected = apps.get_model(app_label='uploader', model_name='bootstrap')
            table_specified_form = 'bootstrapForm'
            message_to_show = ''
            if request.method == "POST":
                form = eval(table_specified_form)(request.POST, request.FILES)
                if form.is_valid():
                    cleaned_data = form.cleaned_data
                    data = requests.put("http://127.0.0.1/API/bootstrap_policies/" + id,
                                        data=json.dumps(cleaned_data))
                    if data.status_code == 200:
                        url = 'table_view/' + table_specified + '/'
                        return redirect('../../../' + url)
                    else:
                        message_to_show = json.loads(data.content.decode("utf-8"))
            data = requests.get("http://127.0.0.1/API/bootstrap_policies/" + id)
            data_content = json.loads(data.content.decode("utf-8"))[0]
            columns = ['id', 'name', 'types', 'subtype', 'data']
            response = dict(zip(columns, data_content))
            if data.status_code == 200:
                instance = model_selected
                for key in response:
                    if key == 'Active' or 'key' == 'Valid' or key == 'Updated':
                        if response[key] == 1:
                            response[key] = True
                        else:
                            response[key] = False
                    setattr(instance, key, response[key])
                form = eval(table_specified_form)(instance=instance)
            else:
                return redirect('main')
        return render(request, 'edit_entry.html',
                      {'form': form, 'table_name': table_specified, 'message': message_to_show, 'sample_policy':sample_policy[table_specified]})
    elif request.user.is_staff == 0:
        message_to_show = ''
        model_selected = apps.get_model(app_label='uploader', model_name=table_mapping[table_specified])
        table_specified_form = table_mapping[table_specified] + '_userForm'
        if request.method == "POST":
            form = eval(table_specified_form)(request.POST, request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                get_fqdn, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID?username={}'.format(request.user))
                cleaned_data['fqdn']=get_fqdn[0][2]
                cleaned_data['local_fqdn'] =get_fqdn[0][2]
                data, status_code = edit_entry_policy(table_specified, cleaned_data, id)
                if status_code == 200:
                    url = 'table_view/' + table_specified + '/'
                    return redirect('../../../' + url)
                else:
                    message_to_show = data
            else:
                return render(request, 'edit_entry.html',
                              {'form': form, 'table_name': table_specified, 'message': message_to_show})
        response, status_code = edit_entry_host_policies_form(table_specified, id)
        if status_code == 200:
            instance = model_selected
            for key in response:
                setattr(instance, key, response[key])
            form = eval(table_specified_form)(instance=instance)
        else:
            return redirect('main')
        return render(request, 'edit_entry.html',
                      {'form': form, 'table_name': table_specified, 'message': message_to_show, 'sample_policy':sample_policy[table_specified]})
    else:
        return HttpResponseRedirect(reverse('main'))



@csrf_protect
def captive_portal(request):
    print('\n\n\nRegistered Users = ', registered_users_state)
    message_on_page = ''
    ip_address = get_user_ip_address(request)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        action = request.POST['action']  # activate or deactivate
        if action == 'activate':
            # defining TTL for the DNS update message and also adding username and IP address in dictionary to save state of user
            ttl = 3600
            message_on_page = 'Successfully Registered'
            registered_users_state[ip_address] = username
            value = 'value=' + registered_users_state[ip_address]
        else:
            # Send TTL 0 to DNS update message as the user has deactivated and also removing user details from dictionary of saved users
            ttl = 0
            message_on_page = 'Successfully Unregistered'
            if ip_address in registered_users_state:
                del (registered_users_state[ip_address])
            value = ''
        data = requests.post(
            "http://127.0.0.1/API/user_registration/?username={}&password={}&ip={}&ttl={}".format(username,
                                                                                                  password,
                                                                                                  ip_address, ttl))
        return render(request, 'captive_portal.html', {'message': message_on_page, 'value': value})
    elif ip_address in registered_users_state:
        message_on_page = 'Welcome Back old User. Your registered Username is ' + registered_users_state[ip_address]
        return render(request, 'captive_portal.html',
                      {'message': message_on_page, 'value': 'value=' + registered_users_state[ip_address]})
    return render(request, 'captive_portal.html', {'message': message_on_page})


@csrf_protect
def user_registration(request):
    if request.user.is_authenticated():
        return redirect('main')
    error_onpage=''
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user_authentication = authenticate(username=username, password=password)
        if user_authentication is not None:
            login(request, user_authentication)
            if request.user.is_staff == 1:
                return HttpResponseRedirect(reverse('main'))
            elif request.user.is_staff == 0:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                fqdn = user_fqdn.objects.values('fqdn').filter(user=request.user.id)[0]
                data = requests.post("http://127.0.0.1/API/user_registration/?fqdn={}&ip={}".format(fqdn['fqdn'],ip))
                if data.status_code==200:
                    return HttpResponseRedirect(reverse('view_table_user'))
                else:
                    logout(request)
            return render('main')
        else:
            error_onpage = 'Username or Password Incorrect'
    return render(request, 'user_registration.html', {'message': error_onpage})




@csrf_protect
def add_user(request):
    form = UserForm()
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            is_staff = form.cleaned_data['is_staff']
            if is_staff == True:
                if request.POST['admin_key'] == 'take5':
                    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, is_staff=is_staff)
                    message = 'Account created Successfully'
                else:
                    return render(request, 'admin_key_error.html', {'form':form})
            elif is_staff== False:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                                last_name=last_name, is_staff=is_staff)
                user.save()
                message = 'Account created Successfully'
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'add_user.html', {'form':form})


@login_required
@csrf_protect
def main(request):
    message_on_page=''
    if request.user.is_staff==1:
        ces_tables = ['ID', 'FIREWALL', 'HOST_POLICIES', 'CES_POLICIES']
        bootstrap = ['bootstrap']
    else:
        get_fqdn, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID?username={}'.format(request.user))
        if get_fqdn:
            ces_tables = ['FIREWALL', 'HOST_POLICIES']
        else:
            ces_tables = []
            message_on_page = 'No user Exists in API with Username = {}'.format(request.user)
        bootstrap = ''
    return render(request,'tables.html', {'ces_tables':ces_tables,'bootstrap_tables':bootstrap, 'firewall':'CES Tables', 'bootstrap':'Bootstrap Table','message':message_on_page})
    #elif request.user.is_authenticated() and user_type != 'admin':
    #    return HttpResponseRedirect(reverse('view_table_user'))
    #return HttpResponseRedirect(reverse('login'))



@csrf_protect
def login(request):
    try:
        if request.user.is_authenticated():
            return redirect('main')
        else:
            error_onpage = ''
            if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                user_authentication = authenticate(username=username, password=password)
                if user_authentication is not None:
                    auth_login(request, user_authentication)
                    return render('main')
                else:
                    error_onpage = 'Username or Password Incorrect'
            return render(request, 'login.html', {'message': error_onpage})
    except:
        return HttpResponseRedirect(reverse('login'))


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return HttpResponseRedirect(reverse('main'))



##########################################################################################
##########################################################################################
##########################################################################################
# Helping Functions

def removing_id_uuid_from_id_table(data, elements_to_delete):
    list_of_ids=[]
    for d in data:
        list_of_ids.append('0'+str(d[0]))
        del d[0:elements_to_delete]
    return data, list_of_ids


def link_maker_decoder_get(link):
    data = requests.get(link)
    return json.loads(data.content.decode("utf-8")), data.status_code


def link_maker_decoder_delete(link):
    data = requests.delete(link)
    return json.loads(data.content.decode("utf-8")), data.status_code


def link_maker_decoder_put(link, data):
    data = requests.put(link, data=json.dumps(data))
    return json.loads(data.content.decode("utf-8")), data.status_code


def link_maker_decoder_post(link, data):
    data = requests.post(link, data=json.dumps(data))
    return json.loads(data.content.decode("utf-8")), data.status_code


def uuid_to_fqdn_replacer(data):
    get_uuid_fqdn_dict = make_id_fqdn_dictionary()
    data, list_of_ids = removing_id_uuid_from_id_table(data,1)
    try:
        for d in data:
            d[0]=get_uuid_fqdn_dict[d[0]]
    except:
        pass
    return data, list_of_ids


def make_id_fqdn_dictionary():
    data, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID')
    uuid_fqdn_mapping={}
    for d in data:
        uuid_fqdn_mapping[d[1]]=d[2]
    return uuid_fqdn_mapping


def host_policy_data_procesing(data_host_policies, data_host_identity, columns_host_policies, columns_host_identity):
    data=[]
    list_of_ids=[]
    for identity in data_host_identity:
        a = True
        del identity[2:4]
        for policy in data_host_policies:
            if identity[3]==policy[1]:
                list_of_ids.append(policy[0])
                data.append(identity[1:3]+policy[2:4])
                a=False
        if a:
            list_of_ids.append('0'+ str(identity[0]))
            data.append(identity[1:3] + ['',''])
    del columns_host_identity[5]
    del columns_host_identity[2:4]
    del columns_host_identity[0]
    del columns_host_policies[0:2]
    return data, list_of_ids, columns_host_identity+columns_host_policies


def ces_policy_data_procesing(data_ces_policies, data_ces_identity, columns_ces_policies, columns_ces_identity):
    data=[]
    list_of_ids=[]
    for identity in data_ces_identity:
        a = True
        for policy in data_ces_policies:
            if identity[3]==policy[1]:
                list_of_ids.append(policy[0])
                data.append(identity[1:3]+policy[2:4])
                a=False
        if a:
            list_of_ids.append('0'+ str(identity[0]))
            data.append(identity[1:3] + ['',''])
    del columns_ces_identity[3]
    del columns_ces_identity[0]
    del columns_ces_policies[0:2]
    return data, list_of_ids, columns_ces_identity+columns_ces_policies


def get_id_table_data_column():
    columns, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/ID')
    data, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID')
    columns = [''.join(x) for x in columns]
    del columns[0:2]
    data, list_of_ids = removing_id_uuid_from_id_table(data, 2)
    return data_status, columns, data, list_of_ids


def get_firewall_table_data_column():
    columns, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/FIREWALL')
    data, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/FIREWALL')
    columns = [''.join(x) for x in columns]
    del columns[0]
    columns[0]='fqdn'
    data, list_of_ids = uuid_to_fqdn_replacer(data)
    return data_status, columns, data, list_of_ids


def get_firewall_table_data_column_user(username):
    columns, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/FIREWALL')
    data, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy_user/username/{}?format=False'.format(username))
    list_of_ids = []
    if data_status==200:
        columns = [''.join(x) for x in columns]
        del columns[0:2]
        data, list_of_ids = uuid_to_fqdn_replacer(data)
    return data_status, columns, data, list_of_ids

def get_host_policies_table_data_column():
    data_host_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICIES')
    data_host_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY')
    columns_host_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICIES')
    columns_host_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICY_IDENTITY')
    columns_host_policies = [''.join(x) for x in columns_host_policies]
    columns_host_identity = [''.join(x) for x in columns_host_identity]
    data, list_of_ids, columns = host_policy_data_procesing(data_host_policies, data_host_identity, columns_host_policies, columns_host_identity)
    return data_status, columns, data, list_of_ids


def get_host_policies_table_data_column_user(username):
    get_fqdn, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID?username={}'.format(username))
    data_host_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICIES')
    data_host_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?local_fqdn={}'.format(get_fqdn[0][2]))
    columns_host_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICIES')
    columns_host_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICY_IDENTITY')
    columns_host_policies = [''.join(x) for x in columns_host_policies]
    columns_host_identity = [''.join(x) for x in columns_host_identity]
    data, list_of_ids, columns = host_policy_data_procesing(data_host_policies, data_host_identity, columns_host_policies, columns_host_identity)
    return data_status, columns, data, list_of_ids


def get_ces_policies_table_data_column():
    data_ces_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICIES')
    data_ces_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY')
    columns_ces_policies, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/CES_POLICIES')
    columns_ces_identity, data_status = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/CES_POLICY_IDENTITY')
    columns_ces_policies = [''.join(x) for x in columns_ces_policies]
    columns_ces_identity = [''.join(x) for x in columns_ces_identity]
    data, list_of_ids, columns = ces_policy_data_procesing(data_ces_policies, data_ces_identity, columns_ces_policies, columns_ces_identity)
    return data_status, columns, data, list_of_ids


def get_table_data(table_specified):
    get_function = table_get_data_mapping[table_specified.upper()]
    data_status, columns, data, list_of_ids = get_function()
    return data_status, columns, data, list_of_ids


def get_table_data_user(table_specified, username):
    get_function = table_get_data_mapping_user[table_specified.upper()]
    data_status, columns, data, list_of_ids = get_function(username)
    return data_status, columns, data, list_of_ids


def delete_id_form_creation(items):
    items = ",".join(items)
    uri = 'http://127.0.0.1/API/firewall_policy/ID/'+ items
    message_to_show, data_status = link_maker_decoder_delete(uri)
    return message_to_show, data_status


def delete_firewall_policies_form_creation(items):
    items = ",".join(items)
    uri = 'http://127.0.0.1/API/firewall_policy/FIREWALL/' + items
    message_to_show, data_status = link_maker_decoder_delete(uri)
    return message_to_show, data_status


def delete_host_policies_form_creation(items):
    list_ids_host_identity=[]
    message_to_show=''
    data_status=''
    for i in items:
        if i[0]=='0':
            list_ids_host_identity.append(i[1:])
    for i in range (len(items)-1,-1,-1):
        if items[i][0]=='0':
            del items[i]
    if items:
        items = ",".join(items)
        uri = 'http://127.0.0.1/API/firewall_policy/HOST_POLICIES/' + items
        message_to_show, data_status = link_maker_decoder_delete(uri)
    if list_ids_host_identity:
        list_ids_host_identity = ",".join(list_ids_host_identity)
        uri = 'http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY/' + list_ids_host_identity
        message_to_show, data_status = link_maker_decoder_delete(uri)
    return message_to_show, data_status


def delete_ces_policies_form_creation(items):
    list_ids_ces_identity=[]
    message_to_show=''
    data_status=''
    for i in items:
        if i[0]=='0':
            list_ids_ces_identity.append(i[1:])
    for i in range (len(items)-1,-1,-1):
        if items[i][0]=='0':
            del items[i]
    if items:
        items = ",".join(items)
        uri = 'http://127.0.0.1/API/firewall_policy/CES_POLICIES/' + items
        message_to_show, data_status = link_maker_decoder_delete(uri)
    if list_ids_ces_identity:
        list_ids_host_identity = ",".join(list_ids_ces_identity)
        uri = 'http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY/' + list_ids_host_identity
        message_to_show, data_status = link_maker_decoder_delete(uri)
    return message_to_show, data_status


def delete_table_data(table_specified, items):
    get_function = table_delete_data_mapping[table_specified.upper()]
    message_to_show, data_status = get_function(items)
    return message_to_show, data_status


def edit_id_form_creation(id):
    data, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/ID/' + id)
    columns, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/ID')
    columns = [''.join(x) for x in columns]
    return data[0],columns,status_code


def edit_firewall_policies_form_creation(id):
    data, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/FIREWALL/' + id)
    columns, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/FIREWALL')
    columns = [''.join(x) for x in columns]
    get_uuid_fqdn_dict = make_id_fqdn_dictionary()
    data[0][1] = get_uuid_fqdn_dict[data[0][1]]
    columns[1]='fqdn'
    return data[0], columns, status_code


def edit_host_policies_form_creation(id):
    data, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICIES/' + id)
    columns, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICIES')
    data1, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?uuid=' + data[0][1])
    columns1, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/HOST_POLICY_IDENTITY')
    columns = [''.join(x) for x in columns]
    columns1 = [''.join(x) for x in columns1]
    return data[0]+data1[0], columns+columns1, status_code


def edit_ces_policies_form_creation(id):
    data, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICIES/' + id)
    columns, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/CES_POLICIES')
    data1, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY?uuid=' + data[0][1])
    columns1, status_code = link_maker_decoder_get('http://127.0.0.1/API/tables_get_columns/CES_POLICY_IDENTITY')
    columns = [''.join(x) for x in columns]
    columns1 = [''.join(x) for x in columns1]
    return data[0]+data1[0], columns+columns1, status_code


def edit_entry_host_policies_form(table_specified, id):
    get_function = table_update_data_mapping[table_specified.upper()]
    data,columns,status_code = get_function(id)
    response = dict(zip(columns, data))
    return response, status_code


def edit_id_entry(data, id):
    data, status_code = link_maker_decoder_put("http://127.0.0.1/API/firewall_policy/ID/" + id,data)
    return data, status_code


def edit_firewall_policies_entry(data, id):
    data, status_code = link_maker_decoder_put("http://127.0.0.1/API/firewall_policy/FIREWALL/" + id,data)
    return data, status_code


def edit_host_policies_entry(data, id):
    response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?local_fqdn={}&direction={}'.format(data['local_fqdn'],data['direction']))
    if response:
        data['uuid']=response[0][5]
        response, status_code = link_maker_decoder_put("http://127.0.0.1/API/firewall_policy/HOST_POLICIES/{}".format(id), data)
    else:
        response, status_code = link_maker_decoder_post('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY', [data])
        response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?local_fqdn={}&direction={}'.format(data['local_fqdn'], data['direction']))
        data['uuid']=response[0][5]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/HOST_POLICIES", [data])
    return response, status_code


def edit_ces_policies_entry(data, id):
    response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY?host_ces_id={}&protocol={}'.format(data['host_ces_id'],data['protocol']))
    if response:
        data['uuid']=response[0][3]
        response, status_code = link_maker_decoder_put("http://127.0.0.1/API/firewall_policy/CES_POLICIES/{}".format(id), data)
    else:
        response, status_code = link_maker_decoder_post('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY', [data])
        response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY?host_ces_id={}&protocol={}'.format(data['host_ces_id'], data['protocol']))
        data['uuid']=response[0][3]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/CES_POLICIES", [data])
    return response, status_code


def edit_entry_policy(table_specified, data, id):
    get_function = table_update_entry_mapping[table_specified.upper()]
    result, status_code = get_function(data, id)
    return result, status_code


def post_id_entry(data):
    data, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/ID",[data])
    return data, status_code


def post_firewall_policies_entry(data):
    data, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/FIREWALL",[data])
    return data, status_code


def post_host_policies_entry(data):
    response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?local_fqdn={}&direction={}'.format(data['local_fqdn'],data['direction']))
    if response:
        data['uuid']=response[0][5]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/HOST_POLICIES", [data])
    else:
        response, status_code = link_maker_decoder_post('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY', [data])
        response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/HOST_POLICY_IDENTITY?local_fqdn={}&direction={}'.format(data['local_fqdn'], data['direction']))
        data['uuid']=response[0][5]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/HOST_POLICIES", [data])
    return response, status_code


def post_ces_policies_entry(data):
    response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY?host_ces_id={}&protocol={}'.format(data['host_ces_id'],data['protocol']))
    if response:
        data['uuid']=response[0][3]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/CES_POLICIES", [data])
    else:
        response, status_code = link_maker_decoder_post('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY', [data])
        response, status_code = link_maker_decoder_get('http://127.0.0.1/API/firewall_policy/CES_POLICY_IDENTITY?host_ces_id={}&protocol={}'.format(data['host_ces_id'], data['protocol']))
        data['uuid']=response[0][3]
        response, status_code = link_maker_decoder_post("http://127.0.0.1/API/firewall_policy/CES_POLICIES", [data])
    return response, status_code




def add_entry_policy(table_specified, data):
    get_function = table_post_entry_mapping[table_specified.upper()]
    result, status_code = get_function(data)
    return result, status_code



def get_user_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    return ip_address





table_get_data_mapping = {'ID':get_id_table_data_column, 'FIREWALL':get_firewall_table_data_column, 'HOST_POLICIES':get_host_policies_table_data_column,
                          'CES_POLICIES':get_ces_policies_table_data_column}


table_update_data_mapping = {'ID':edit_id_form_creation, 'FIREWALL':edit_firewall_policies_form_creation, 'HOST_POLICIES':edit_host_policies_form_creation,
                          'CES_POLICIES':edit_ces_policies_form_creation}




table_delete_data_mapping = {'ID':delete_id_form_creation, 'FIREWALL':delete_firewall_policies_form_creation, 'HOST_POLICIES':delete_host_policies_form_creation,
                          'CES_POLICIES':delete_ces_policies_form_creation}




table_update_entry_mapping = {'ID':edit_id_entry, 'FIREWALL':edit_firewall_policies_entry, 'HOST_POLICIES':edit_host_policies_entry,
                          'CES_POLICIES':edit_ces_policies_entry}



table_post_entry_mapping = {'ID':post_id_entry, 'FIREWALL':post_firewall_policies_entry, 'HOST_POLICIES':post_host_policies_entry,
                          'CES_POLICIES':post_ces_policies_entry}




table_get_data_mapping_user = {'FIREWALL':get_firewall_table_data_column_user, 'HOST_POLICIES':get_host_policies_table_data_column_user}











