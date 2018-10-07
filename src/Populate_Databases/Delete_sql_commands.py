
delete from ces_policies         ;
delete from ces_policy_identity  ;
delete from host_policies        ;
delete from host_policy_identity ;
delete from host_ids             ;
delete from firewall_policies    ;
delete from host_policy_ts       ;


ALTER TABLE ces_policies          AUTO_INCREMENT = 1;
ALTER TABLE ces_policy_identity   AUTO_INCREMENT = 1;
ALTER TABLE host_policies         AUTO_INCREMENT = 1;
ALTER TABLE host_policy_identity  AUTO_INCREMENT = 1;
ALTER TABLE host_ids              AUTO_INCREMENT = 1;
ALTER TABLE firewall_policies     AUTO_INCREMENT = 1;
ALTER TABLE host_policy_ts        AUTO_INCREMENT = 1;




use ces_bootstrap;
delete from bootstrap;
ALTER TABLE bootstrap AUTO_INCREMENT = 1;
