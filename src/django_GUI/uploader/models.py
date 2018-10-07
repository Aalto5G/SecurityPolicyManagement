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


from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import validate_comma_separated_integer_list



class user_fqdn(models.Model):
    user = models.CharField(max_length=32)
    fqdn = models.CharField(max_length=256)
    class Meta:
        db_table='user_fqdn'


class CustomBooleanField(models.BooleanField):
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return int(value) # return 0/1

##############################################################
# Database Models:

class host_ids(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. From 9 to 15 digits allowed.")

    uuid = models.CharField(max_length=32, db_column="uuid", blank=True)
    fqdn = models.CharField(max_length=256, db_column="fqdn")
    msisdn = models.CharField(validators=[phone_regex], max_length=16, db_column="msisdn")
    ipv4 = models.GenericIPAddressField(db_column="ipv4")
    username = models.CharField(max_length=64, db_column="username")
    class Meta:
        db_table='host_ids'


class firewall_policies(models.Model):
    fqdn = models.CharField(max_length=256, db_column="fqdn", blank=True)
    types = models.CharField(max_length=32, db_column="types")
    sub_type = models.CharField(max_length=32, db_column="sub_type", null=True, blank=True)
    policy_element = models.CharField(max_length=2048, db_column="policy_element")
    class Meta:
        db_table='firewall_policies'


class host_policies(models.Model):
    local_fqdn = models.CharField(max_length=256, db_column="local_fqdn", blank=True, null=True)
    #remote_fqdn = models.CharField(max_length=256, db_column="remote_fqdn", blank=True)
    #reputation = models.CharField(max_length=48, db_column="reputation", blank=True)
    direction = models.CharField(max_length=16, db_column="direction", blank=True)
    types =models.CharField(max_length=16, db_column="types")
    policy_element =models.CharField(max_length=2048, db_column="policy_element")
    class Meta:
        db_table='host_policies'


class ces_policies(models.Model):
    host_ces_id =models.CharField(max_length=256, db_column="host_ces_id")
    protocol =models.CharField(max_length=256, db_column="protocol")
    types =models.CharField(max_length=16, db_column="types")
    policy_element =models.CharField(max_length=2048, db_column="policy_element")
    class Meta:
        db_table='ces_policies'


class bootstrap(models.Model):
    name = models.CharField(max_length=128, db_column="name")
    types = models.CharField(max_length=128, db_column="types", blank=True)
    sub_type = models.CharField(max_length=128, blank=False, default=None, db_column="sub_type")
    data = models.CharField(max_length=512, db_column="data")
    class Meta:
        db_table = 'bootstrap'



#################################




class CES_Reputation_Table(models.Model):
    CES_FQDN =models.CharField(max_length=128, db_column="CES_FQDN")
    Reputation =models.CharField(max_length=48, db_column="Reputation")
    class Meta:
        db_table='CES_Reputation_Table'

class Host_Reputation_Table(models.Model):
    Host_FQDN =models.CharField(max_length=128, db_column="Host_FQDN")
    Reputation =models.CharField(max_length=48, db_column="Reputation")
    class Meta:
        db_table='Host_Reputation_Table'

class firewall_user_policies(models.Model):
    fqdn = models.CharField(max_length=256, db_column="fqdn")
    cessapp_id = models.IntegerField(db_column="cessapp_id", blank=True)
    type = models.CharField(max_length=16, db_column="type")
    active = CustomBooleanField(db_column="active")
    priority = models.IntegerField(db_column="priority")
    direction = models.CharField(max_length=32, db_column="direction")
    src = models.GenericIPAddressField(max_length=128, db_column="src", blank=True, null=True)
    dst = models.GenericIPAddressField(max_length=128, db_column="dst", blank=True, null=True)
    sport = models.CharField(validators=[validate_comma_separated_integer_list], max_length=128, db_column="sport", blank=True)
    dport = models.CharField(validators=[validate_comma_separated_integer_list], max_length=128, db_column="dport", blank=True)
    protocol = models.PositiveSmallIntegerField(db_column="protocol")
    target = models.CharField(max_length=16, db_column="target")
    comment = models.CharField(max_length=256, db_column="comment", blank=True)
    raw_data = models.CharField(max_length=512, db_column="raw_data", blank=True)
    #schedule_start = models.DateTimeField(db_column="schedule_start", blank=True, null=True)
    #schedule_end = models.DateTimeField(db_column="schedule_end", blank=True, null=True)
    class Meta:
        db_table='host_firewall'
